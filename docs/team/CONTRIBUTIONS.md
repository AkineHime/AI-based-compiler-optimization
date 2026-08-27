# Contributions

Work is split into four roles (see [`../planning/persons_work_dist.md`](../planning/persons_work_dist.md)). Every commit carries
a `Co-Authored-By` trailer; this file maps areas to owners so attribution stays
explicit as the project grows.

| Area | Files | Owner |
|---|---|---|
| Lexer, parser, AST, semantic analysis | `src/minic/frontend/` | Person A |
| TAC IR, CFG, dominators, natural loops, IR printer | `src/minic/ir/` | Person A |
| Static feature extractor (19 metrics) | `src/minic/features/extractor.py` | Person A |
| Optimization passes 1-5 (CF, DCE, CSE, LICM, SR) | `src/minic/optimizer/{constant_folding,dce,cse,licm,strength_reduction}.py` | Person B |
| Pass manager, 6-flag combo controller, fixpoint iteration | `src/minic/optimizer/pass_manager.py` | Person B |
| Loop unrolling (pass 6) | `src/minic/optimizer/loop_unroll.py` | Person B |
| TAC -> C codegen, value-semantics wrappers | `src/minic/codegen/` | Person B |
| Correctness harness (64-combo regression) | `tests/test_pass_regressions.py`, `tests/test_optimizer.py`, `tests/test_loop_unroll.py`, `tests/test_nested_aggregates.py` | Person B |
| `variable_count` -> `named_/temp_variable_count` split | `src/minic/features/extractor.py` | Person B |
| Opportunity features (8 metrics) | `src/minic/features/opportunity.py` | Person C |
| Timing harness, parallel 64-combo sweep, ground-truth oracle | `src/minic/harness/` | Person C |
| Parametric benchmark generator | `src/minic/harness/gen_corpus.py` | Person C |
| ML dataset, risk-aware strategy bake-off, GroupKFold training, predictor | `src/minic/ml/` | Person C |
| CLI + browser playground | `demo/` | Person C |
| Results report + chart + published page | `src/minic/harness/{report,plot,gen_resultspage}.py`, `RESULTS.md`, `docs/results.html` | Person C |
| Hand-written benchmark corpus, ground truth | `benchmarks/` | Person D |
| Report sections (MiniC design rationale) | — | Person D |

Cross-cutting fixes (Python 3.13 imports in Part A; nested-aggregate l-value
lowering in `ir_generator.py`; several latent optimizer bugs surfaced while
integrating later passes) were made in place with the relevant area's owner
credited and documented in [`PERSON_B_NOTES.md`](PERSON_B_NOTES.md) /
[`PERSON_C_NOTES.md`](PERSON_C_NOTES.md).
