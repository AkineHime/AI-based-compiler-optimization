# AI Development Prompts & Tech Stack — By Role

Companion to `minic-language-spec.md`, `persons_work_dist.md`, and `project-workflow-and-action-plan.md`.

---

## Person A — Front-End + IR + Feature Extractor

* **Stack:** Python 3.10+, hand-written recursive-descent parser, `dataclasses` for AST/TAC nodes, `pytest`.

### Step-by-Step AI Prompts:
1. *"Build a Python lexer for this MiniC grammar [paste BNF from minic-language-spec.md]. Tokens: keywords (`int`, `float`, `char`, `struct`, `if`, `else`, `while`, `for`, `return`), identifiers, int/float/char/string literals, operators, punctuation. Use a `Token` dataclass with `type`, `value`, and `line_number`. Add unit tests."*
2. *"Using this lexer, build a recursive-descent parser matching this BNF that produces an AST using dataclasses for each node type. Support optional `struct` keyword in type specifier. Report line numbers on syntax errors."*
3. *"Add semantic analysis: nominal struct type matching, array dimension checking, rejecting invalid lvalues (e.g. function call or literal on the left of `=`)."*
4. *"Lower the type-checked AST to three-address code (TAC) using this opcode set [paste agreed TAC opcode format]. Handle array indexing and struct field access as address computation followed by load/store."*
5. *"Write a feature extractor that walks the AST/TAC and computes: loop count, max loop nesting depth, basic block count, branch density, instruction-type histogram, struct field count, array dimensionality. Output as a flat dict."*
6. *"Run this pipeline against the canonical example program from the spec and show me the resulting TAC so I can check it by hand."*

---

## Person B — Optimization Passes + Codegen

* **Stack:** Python 3.10+, AST/TAC dataclasses from Person A, `pytest` regression suite.

### Step-by-Step AI Prompts:
1. *"Given this TAC format [paste A's opcode spec], implement constant folding as a standalone toggleable pass — evaluate compile-time constant expressions and replace with literals."*
2. *"Implement dead code elimination (DCE): backward liveness analysis, remove instructions whose result is never subsequently used."*
3. *"Implement common subexpression elimination (CSE) using value numbering per basic block."*
4. *"Implement loop-invariant code motion (LICM): detect natural loops via back-edges, hoist operand-invariant instructions to the loop preheader."*
5. *"Implement strength reduction: replace multiplication by a loop induction variable with repeated addition."*
6. *"Wire all 5 passes behind a single 5-flag config so any of the 64 combinations can be applied in a fixed canonical order."*
7. *"Write codegen that translates TAC to C, wrapping every array/struct/string in a one-field C struct per Section 4 of minic-language-spec.md, and lowering string literal assignments using C99 compound literals `(str_N){ .data = "literal" }` so assignment stays copy-semantics in emitted C."*
8. *"Write a regression test that runs all 64 combinations against the canonical example and asserts every single one compiles and runs to output 83 — catch any pass that silently breaks program semantics."*

---

## Person C — Timing Harness + ML Model + Demo

* **Stack:** Python 3.10+, `subprocess`, system `gcc`, `pandas`, `scikit-learn` (`RandomForestRegressor` / `GradientBoostingRegressor`), `streamlit` (optional demo UI).

### Step-by-Step AI Prompts:
1. *"Write a Python function that compiles an emitted C file with `gcc -O0 -o out`, runs `out` 20 times via subprocess timing with `time.perf_counter()`, discards the first 3 runs as warm-up, and returns the median execution time in milliseconds."*
2. *"Wrap that in a sweep function that runs across all 64 optimization-flag combinations for a given MiniC program and returns a pandas DataFrame of `(program_id, combo_bits, features, median_time_ms)`."*
3. *"Write a fake-data generator producing random feature vectors and random timings in the same schema, so the training pipeline can be built before real data exists."*
4. *"Build a training script using scikit-learn. Use `GroupKFold` cross-validation grouped by `program_id` to prevent data leakage across combinations of the same benchmark. Try both classification (predict best combo index) and regression (predict speedup ratio per combo, take argmax)."*
5. *"Build a small demo CLI/UI: given a MiniC program, extract features, predict the recommended combo, compile and run both the baseline and recommended version, and print measured speedup percentage."*

---

## Person D — Benchmark Corpus + Correctness Oracle + Report

* **Stack:** Plain MiniC/C syntax, system `gcc` for ground truth verification.

### Step-by-Step AI Prompts:
1. *"Write 30-40 MiniC test programs covering 2D array traversals, struct arithmetic, fixed string processing, recursion, LICM-friendly loops, and strength-reduction loops. Ensure loop trip counts are in the thousands to millions so execution times under `gcc -O0` are >100ms and not drowned out by noise."*
2. *"For each program, provide an equivalent standard C program so we can compile it with real gcc and use the output as ground truth."*
3. *"Write a short script that compiles all reference C versions with gcc, runs them, and outputs a CSV table of `(program_name, expected_output)` to diff our compiler's results against."*
4. *"Draft a report section explaining why MiniC excludes pointers and dynamic memory, and why arrays/structs use value semantics — written for a compiler-design audience, referencing alias analysis complexity."*
