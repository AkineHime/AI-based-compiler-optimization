# Person B — Optimization Passes + TAC→C Codegen

Status: **complete and verified**. All 64 optimization combinations compiled with
`gcc -O0` reproduce the canonical program's result `83`
(`tests/test_correctness.py`).

## What landed

| Area | Module | Notes |
|---|---|---|
| Constant folding + propagation | `src/minic/optimizer/constant_folding.py` | forward walk, block-boundary reset, 32-bit C-int semantics, constant-branch pruning |
| Dead code elimination | `src/minic/optimizer/dce.py` | backward liveness over the CFG, iterated to a fixed point; globals kept live at exits |
| Common subexpression elim. | `src/minic/optimizer/cse.py` | local value numbering per basic block; only pure arith/rel/logic exprs |
| Loop-invariant code motion | `src/minic/optimizer/licm.py` | hoists single-def temporaries into a synthesized pre-header before the loop header label |
| Strength reduction | `src/minic/optimizer/strength_reduction.py` | `j = i*K` → additive accumulator seeded in the pre-header, updated next to `i`'s increment |
| Pass controller | `src/minic/optimizer/pass_manager.py` | 5-flag `combo_id` 0..63, fixed order **CF → CSE → LICM → SR → DCE**, whole sequence iterated to a fixed point |
| TAC→C codegen | `src/minic/codegen/c_emitter.py` | one-field wrapper structs for every array/string; MiniC structs map to named C structs; C99 compound-literal string init |
| End-to-end helpers | `src/minic/pipeline.py` | `source_to_c(src, combo)`, `compile_and_run(...)` |

Flag bits (matches `FULL_PROJECT_PLAN.md §2.3`):
`1`=CF, `2`=DCE, `4`=CSE, `8`=LICM, `16`=SR. `combo_id == 0` is the untouched baseline.

## Also done, as instructed

* **`variable_count` feature split** into `named_variable_count` (source-level
  locals/params/globals) and `temp_variable_count` (`tN` temporaries) —
  `src/minic/features/extractor.py`. Feature vector is now 19 wide. Person C's
  dataset schema should use these two columns instead of `variable_count`.
* **Two import bugs in Part A fixed** so the repo runs on Python 3.13:
  `lexer.py` used `Any` without importing it; `ir/tac.py` used `Tuple` without
  importing it. (All of Person A's existing tests pass before and after.)

## Decisions worth a look

* **Codegen wraps arrays and strings, not scalar structs.** A MiniC
  `struct Point { int x; int y; }` becomes `typedef struct { int x; int y; } Point;`
  and is passed/returned by value — C structs already have value semantics, so a
  second wrapper adds nothing but `p.data.x` noise. This matches the worked
  example in `FULL_PROJECT_PLAN.md §3.5`. Only array/string decay needs the
  wrapper. Easy to change to "wrap everything" if you'd rather — it's one
  function in `c_emitter.py`.
* **Every pass is correctness-first.** Where a fact can't be proven cheaply
  (aggregate aliasing across calls, loop-exit liveness, div/mod traps) the pass
  declines to transform rather than risk it. MiniC's no-pointer / no-aliasing
  invariant is the one thing they lean on: two named locals can never alias.
* **Pass order** is the plan's canonical `CF → CSE → LICM → SR → DCE`, repeated
  until fixpoint so a combo like CF+DCE cleans up folded temporaries.

## Known limitations (not blockers for the dataset)

* CSE is basic-block-local (no extended/global value numbering).
* Strength reduction only fires on `i = i + c` / staged `t = i + c; i = t`
  induction variables with a literal multiplier.
* Codegen assumes the front end's flattened one-name-per-local scoping (true
  today; would break if the parser ever allowed same-name shadowing in sibling
  blocks).
* 1-index access on a 2-D array (a "row" value) is not exercised by the front
  end and codegen falls back to scalar for that shape.

## How to run

```bash
# emit optimized C for a combo
python -m src.minic.driver canonical_example.mc --optimize 63 --emit-c

# optimize, compile with gcc -O0, run, print exit code
python -m src.minic.driver canonical_example.mc --optimize 63 --run

# the 64-combo correctness sweep
python -m pytest tests/test_correctness.py -q
```
