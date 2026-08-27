# Person B — Optimization Passes + TAC→C Codegen

Status: **merged, then hardened**. Two parallel implementations (`1e66807`,
`965f0a8`) were merged; `965f0a8`'s pass engine + codegen is the base. The
correctness bugs listed in the earlier revision of this file have now been
**fixed in place** (the engine was kept — nothing was rewritten from scratch).

## Engine on `main`

`*_pass(func, global_names=frozenset()) -> func` functions, orchestrated by
`PassManager` / `optimize_program(prog, mask)`; codegen via `CEmitter().emit(prog)`.

| Bit | Pass | Module |
|---|---|---|
| `1` | Constant folding + propagation + whole-function const propagation + algebraic simplification | `optimizer/constant_folding.py` |
| `2` | Dead code elimination (liveness + unreachable blocks + label/alloc cleanup) | `optimizer/dce.py` |
| `4` | Common subexpression elimination (local value numbering + copy propagation) | `optimizer/cse.py` |
| `8` | Loop-invariant code motion | `optimizer/licm.py` |
| `16` | Strength reduction | `optimizer/strength_reduction.py` |
| `32` | Loop unrolling (factor 4, remainder loop) | `optimizer/loop_unroll.py` |

**6 passes -> 64 combos.** Canonical order **CF → CSE → LU → LICM → SR → DCE**,
and the whole sequence is **iterated to a fixed point** (`PassManager.MAX_ROUNDS`)
so LICM/CF/CSE clean up after LU and each other. `combo 0` = untouched baseline.

LU sits before LICM/SR because those introduce loop-carried temporaries and the
unroller only duplicates a body whose temps are iteration-local.  Two latent
bugs surfaced and were fixed while wiring LU in: SR did not require its
induction variable to be written exactly once (an unrolled loop writes it once
per copy), and CF propagated a temp's value across a block boundary assuming
single-assignment (SR's accumulator, now a named `__srN` var, breaks that).
`optimizer/_util.py` holds the shared 32-bit / C-arithmetic helpers and the
"which globals may a call clobber" query.

## Fixes applied on top of `965f0a8`

1. **Strength reduction — pre-header seed.** `_find_biv_init_val` scanned the
   whole function backward and picked up the *in-loop* update of the induction
   variable, seeding `sr_temp` from an undefined temporary. Proven wrong: a loop
   starting at `i = 3` returned 84 instead of 168 for every SR-enabled combo.
   Now the seed is `sr_temp = biv * K` emitted in the pre-header, where `biv`
   still holds its pre-loop value. Identity (`is`) comparisons replace value
   (`==`) comparisons in the splice. 32-bit wrap on the step constant.
2. **LICM — trapping hoists.** `DIV`/`MOD` are hoisted only when the divisor is
   a known non-zero constant (a pre-header runs even on a zero-trip loop).
   Hoisting is now restricted to temporaries — a named variable can be read
   before it is written across iterations, and moving its def to the pre-header
   would change that read. When the loop contains a call, operands that name a
   global are treated as variant.
3. **Constant folding — C integer semantics.** Integer folds wrap to 32-bit
   two's-complement; `/` truncates toward zero; `%` takes the sign of the
   dividend. Float arithmetic is no longer folded (rounding can't then diverge
   from the runtime). Algebraic identities (`x*0`, `x*1`, …) apply to integer
   operands only (they don't hold for NaN/inf).
4. **CSE — globals across calls.** A `CALL` now invalidates cached arithmetic
   expressions that read a global, not just cached loads/field-reads.
5. **DCE — globals at exit.** Globals are live on every function exit and their
   definitions are never deleted.
6. **Codegen — global shadowing (found while testing the above).** `CEmitter`
   was declaring every referenced `Var` — including globals — as a zero-init
   *local* in each function, so a global was never actually shared. A program
   using a global counter returned 10 instead of 20 for all 64 combos. Globals
   are now excluded from per-function local declarations.
7. **Codegen — typedef ordering.** Array/string wrappers were emitted before the
   user structs they may contain (`typedef struct { Pt data[3]; } arr_Pt_3;`
   before `Pt`), and structs were not ordered among themselves. All struct and
   wrapper typedefs are now emitted in dependency (topological) order.

`PassManager.optimize_program` computes the program's global-name set once and
threads it into CSE / LICM / DCE. All pass entry points keep a default empty
`global_names`, so the existing single-arg call sites in `tests/` still work.

## Tests

* `tests/test_optimizer.py` (from `965f0a8`) — 64-combo `gcc -O0` sweeps for the
  canonical program (→83), a 2×2 matrix multiply (→134), a struct particle sim
  (→55).
* `tests/test_pass_regressions.py` (new) — 8 tricky programs, each run under all
  64 combos with **combo 0 as the oracle**: strength reduction from a non-zero
  start, nested-loop SR, LICM over a zero-trip divide, LICM invariant hoist,
  32-bit overflow folding, and three global-variable programs (shared counter,
  "dead-looking" store to a global).
* `tests/test_passes.py`, `tests/test_codegen.py` — per-pass and codegen units.

## Retained from `1e66807`

* `variable_count` feature split → `named_variable_count` + `temp_variable_count`
  (`features/extractor.py`, vector now 19-wide; `965f0a8` didn't touch it).
  Person C's dataset schema should use the two new columns.
* `src/minic/pipeline.py` — `source_to_c(src, combo)`, `compile_and_run(...)`.
* Python 3.13 import fixes (`Any` in `lexer.py`, `Tuple` in `ir/tac.py`).

## Still limited (not bugs — reduced scope, safe)

* CSE stays basic-block-local.
* LICM hoists temporaries only (no dominance analysis for named vars).
* Strength reduction fires only on `i = i ± c` / staged `t = i ± c; i = t`
  induction variables with a literal multiplier.

## Upstream gap flagged for Person A (front end / IR gen — NOT touched here)

`ir_generator._lower_expr` types the temp for every `ArrayAccessExpr` and
`FieldAccessExpr` as `int` regardless of the real element/field type, and an
assignment whose target is a *nested* aggregate lvalue (`a[i].f = v`,
`s.g.h = v`) is lowered as a read into a temporary copy followed by
`SET_FIELD` on that copy — the write never reaches the array element / nested
struct. Consequence: programs with **arrays of structs**, **structs containing
structs**, or **structs containing arrays** do not compile / do not round-trip.
Minimal repros:

```c
struct Pt { int x; int y; };
int main() { struct Pt ps[2]; ps[0].x = 1; return ps[0].x; }   // -> C type error

struct I { int a; }; struct O { struct I lo; };
int main() { struct O o; o.lo.a = 5; return o.lo.a; }          // -> C type error
```

The canonical example and the current benchmark set only use scalar struct
fields and scalar array elements, so this does not affect the 64-combo sweeps —
but Person D's struct-heavy benchmarks may hit it. Fix belongs in
`src/minic/ir/ir_generator.py` (type-carrying `new_temp`, plus a
read-modify-write chain for compound-target assignments).

## Run

```bash
python -m src.minic.driver canonical_example.mc --optimize 63 --run
python -m pytest tests/test_optimizer.py tests/test_pass_regressions.py -q
```
