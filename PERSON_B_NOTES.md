# Person B — Optimization Passes + TAC→C Codegen

Status: **merged**. Two implementations existed after parallel work
(`1e66807` and `965f0a8`); this file records what the merged `main` contains and
what to watch.

## What `main` uses

The **pass engine and codegen are from `965f0a8`** (`*_pass(func) -> func`
functions, `PassManager` / `optimize_program(prog, mask)`, `CEmitter().emit()`):

| Area | Module | Entry point |
|---|---|---|
| Constant folding + propagation + algebraic simplification | `src/minic/optimizer/constant_folding.py` | `constant_folding_pass` |
| Dead code elimination (liveness + unreachable blocks + label/alloc cleanup) | `src/minic/optimizer/dce.py` | `dce_pass` |
| Common subexpression elimination (local value numbering, incl. loads/fields) | `src/minic/optimizer/cse.py` | `cse_pass` |
| Loop-invariant code motion | `src/minic/optimizer/licm.py` | `licm_pass` |
| Strength reduction | `src/minic/optimizer/strength_reduction.py` | `strength_reduction_pass` |
| Pass controller | `src/minic/optimizer/pass_manager.py` | `optimize_program(prog, mask)` |
| TAC→C codegen (wrapper structs, C99 compound literals) | `src/minic/codegen/c_emitter.py` | `CEmitter().emit(prog)` |

Flag bits: `1`=CF, `2`=DCE, `4`=CSE, `8`=LICM, `16`=SR. Canonical order
CF → CSE → LICM → SR → DCE (single pass, not iterated to a fixed point).
`combo 0` is the untouched baseline.

Correctness sweep: `tests/test_optimizer.py` runs all 64 combos through
`gcc -O0` for the canonical program (→83), a 2×2 matrix multiply (→134) and a
struct particle sim (→55). All green.

## Retained from `1e66807`

* **`variable_count` feature split** into `named_variable_count` and
  `temp_variable_count` — `src/minic/features/extractor.py`, feature vector now
  **19 wide**. `965f0a8` did not touch the extractor. Person C's dataset schema
  must use the two new columns instead of `variable_count`.
  Covered by `tests/test_features.py`.
* **`src/minic/pipeline.py`** — `source_to_tac`, `source_to_c(src, combo)`,
  `compile_and_run(...) -> RunResult`. Convenience wrapper for Person C's
  "features → predict → optimize → codegen → compile → run" demo path.
* **Two Part-A import fixes** for Python 3.13 (`Any` in `lexer.py`, `Tuple` in
  `ir/tac.py`).

`1e66807`'s alternative pass implementations (`optimizer/_util.py`,
`run(func, prog)` signature, fix-point pass manager) are **not** on `main` but
remain in history if any of the items below need a reference fix.

## Review notes on the merged passes (latent — current benchmarks don't hit them)

1. **Strength reduction — initial-value scan.** `_find_biv_init_val` walks
   `reversed(func.instructions)` and returns the first `ASSIGN` to the induction
   variable. For this front end's staged update (`t = i + c; i = t`) that is the
   in-loop `i = t`, so the pre-header seed becomes `sr = t * k` referencing a
   temp not yet computed. Not triggered today because no benchmark lowers to an
   explicit `IV * const` in TAC (2-D indexing hides the multiply). Fix before any
   strength-reduction-friendly benchmark lands.
2. **LICM — no zero-divisor guard.** A hoistable `t = x / y` / `x % y` moved into
   the pre-header runs even on a zero-trip loop; if `y == 0` there it traps where
   the baseline would not. Guard: only hoist DIV/MOD when the divisor is a
   non-zero constant.
3. **Constant folding — 32-bit semantics.** Folding uses Python big ints. C
   `int` overflow wraps at runtime, so a folded constant can disagree with the
   unoptimized baseline for expressions that overflow 32 bits. Also `%` follows
   Python's sign-of-divisor rule vs C's sign-of-dividend for negatives. Wrap
   results to `int32` and use truncating division/remainder.
4. **CSE — globals across calls.** On `CALL` only load/field expressions are
   invalidated, not arithmetic over globals: `t1 = g + 1; f(); t2 = g + 1`
   reuses `t1` even if `f` writes `g`.
5. **DCE — globals at exit.** Exit-block `live_out` is empty; a trailing
   `g = expr` to a global that isn't re-read locally could be deleted.

Items 3–5 only matter once benchmarks use mutable globals or wide-integer
arithmetic; MiniC programs so far are self-contained functions returning small
ints.

## How to run

```bash
python -m src.minic.driver canonical_example.mc --optimize 63 --emit-c
python -m src.minic.driver canonical_example.mc --optimize 63 --run
python -m pytest tests/test_optimizer.py -q   # the 64-combo sweep
```
