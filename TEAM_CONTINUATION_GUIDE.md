# MiniC Compiler Optimizer — Team Continuation & Handoff Guide
**Project:** AI-Based Compiler Optimization Recommendation System  
**Current Milestone:** Person A's pipeline is complete and verified.

---

## 1. Current State of the Codebase (Person A Handoff)

Person A has implemented and tested the entire front-end, intermediate representation (IR), and static feature extractor. All modules are located under `src/minic/`:

```
src/minic/
├── frontend/        # Lexer, Parser, AST Nodes, Semantic Analyzer, ASTPrinter
├── ir/              # TAC Instruction types, Operands, CFG Builder, Dominators, IRPrinter
├── features/        # 18-metric Static Feature Extractor
└── driver.py        # CLI driver for parsing, TAC generation, and feature extraction
```

### How to use Person A's pipeline in Python:
```python
from src.minic.frontend import Lexer, Parser, SemanticAnalyzer
from src.minic.ir import IRGenerator, IRPrinter, build_cfg_for_function
from src.minic.features import FeatureExtractor

# 1. Parse source code to AST
source_code = open("canonical_example.mc").read()
tokens = Lexer(source_code).tokenize()
ast = Parser(tokens, source_code).parse()

# 2. Semantic type checking
SemanticAnalyzer(source_code).analyze(ast)

# 3. Lower AST to Three-Address Code (TAC)
tac_prog = IRGenerator().generate(ast)

# 4. Extract 18 static features
features = FeatureExtractor().extract(ast, tac_prog)
```

---

## 2. Person B — Optimization Passes & IR-to-C Codegen

* **Goal:** Implement the 5 toggleable IR optimization passes and emit executable C code that preserves MiniC's value semantics.
* **Target Directory:** `src/minic/optimizer/` and `src/minic/codegen/`

### Step-by-Step Action Plan:

#### Step 1: Create `src/minic/optimizer/pass_manager.py`
The pass manager orchestrates the 5 passes using a 5-bit integer (`0` to `63`):
* Bit 0 (`1`): Constant Folding
* Bit 1 (`2`): Dead Code Elimination (DCE)
* Bit 2 (`4`): Common Subexpression Elimination (CSE)
* Bit 3 (`8`): Loop-Invariant Code Motion (LICM)
* Bit 4 (`16`): Strength Reduction

```python
# Pass signature template:
def optimize_program(tac_prog: TACProgram, combo_mask: int) -> TACProgram:
    optimized = copy.deepcopy(tac_prog)
    for func in optimized.functions:
        if combo_mask & 1:  # Bit 0
            func = constant_folding_pass(func)
        if combo_mask & 4:  # Bit 2
            func = cse_pass(func)
        if combo_mask & 8:  # Bit 3
            func = licm_pass(func)
        if combo_mask & 16: # Bit 4
            func = strength_reduction_pass(func)
        if combo_mask & 2:  # Bit 1 (run DCE last to clean up dead code)
            func = dce_pass(func)
    return optimized
```

#### Step 2: Implement the 5 Passes
1. **Constant Folding (`constant_folding.py`):**
   - Fold binary arithmetic on constants (e.g. `t1 = 3 + 5` $\rightarrow$ `t1 = 8`).
   - Propagate known constants forward into subsequent instruction operands.
   - Simplify constant branches (`if 1 goto L1` $\rightarrow$ `goto L1`; `if 0 goto L1` $\rightarrow$ delete).
2. **Dead Code Elimination (`dce.py`):**
   - Use `src.minic.ir.cfg.build_cfg_for_function` to get the CFG.
   - Perform backward liveness analysis: compute `LiveIn` and `LiveOut` sets per basic block.
   - Remove assignments `t = ...` where `t` is never read downstream and has no side effects.
3. **Common Subexpression Elimination (`cse.py`):**
   - Use Local Value Numbering (LVN) per basic block.
   - Map expression tuples `(OP, val1, val2)` to existing temporaries.
4. **Loop-Invariant Code Motion (`licm.py`):**
   - Identify natural loops using `cfg.loops`.
   - Identify instructions whose operands are defined outside the loop or are constant.
   - Hoist invariant instructions into the loop preheader.
5. **Strength Reduction (`strength_reduction.py`):**
   - Detect induction variables (e.g. `j = i * 4` where `i = i + 1`).
   - Replace multiplication with repeated addition (`j = j + 4`).

#### Step 3: Implement IR-to-C Codegen (`src/minic/codegen/c_emitter.py`)
Translate optimized `TACProgram` into C source text:
* Wrap 1D and 2D arrays and strings into 1-field C `struct`s (`typedef struct { int data[3][3]; } arr_int_3_3;`) so function arguments and assignments use true copy semantics.
* Lower string literal assignments using C99 compound literals: `(str_6){ .data = "grid1" }`.

#### Step 4: Correctness Check
Write `tests/test_optimizer.py`:
- Run all 64 pass combinations on `canonical_example.mc`.
- Compile each with `gcc -O0` and assert that **all 64 combinations output exactly 83**.

---

## 3. Person D — Benchmark Corpus & Correctness Oracle

* **Goal:** Write 30–40 MiniC benchmark programs and an automated ground-truth reference table.
* **Target Directory:** `benchmarks/`

### Step-by-Step Action Plan:

#### Step 1: Write 30–40 `.mc` Benchmark Programs
Distribute programs across 5 categories in `benchmarks/`:
1. `benchmarks/numeric/` (8 programs): `matrix_mult.mc`, `matrix_transpose.mc`, `conv2d_3x3.mc`, `vector_dot.mc`, `gaussian_elim.mc`, etc.
2. `benchmarks/structs/` (7 programs): `point_distance.mc`, `particle_sim.mc`, `bounding_box.mc`, `complex_arithmetic.mc`, etc.
3. `benchmarks/strings/` (6 programs): `palindrome.mc`, `caesar_cipher.mc`, `string_reverse.mc`, `run_length.mc`, etc.
4. `benchmarks/recursion/` (7 programs): `fibonacci.mc`, `hanoi.mc`, `quicksort.mc`, `tree_search.mc`, etc.
5. `benchmarks/loops/` (7 programs): `licm_stress.mc`, `strength_reduction_stress.mc`, `polynomial_eval.mc`, `prime_sieve.mc`, etc.

#### Step 2: Ensure High Loop Trip Counts
* **Critical Rule:** Under `gcc -O0`, execution times must be **>100ms** so that optimization speedups exceed clock noise.
* Add an outer loop wrapper in `main()` (e.g. repeat calculation 10,000 to 500,000 times) to ensure measurable execution duration.

#### Step 3: Create `benchmarks/ground_truth.csv`
For each `.mc` program, write an equivalent standard `.c` program, compile with GCC, run it, and log the expected return code/output:
```csv
program_id,category,expected_output
matrix_mult,numeric,45200
particle_sim,structs,1204
palindrome,strings,1
```

#### Step 4: Draft Report Theoretical Section
Author Section 2 of the final report: *"Why MiniC omits pointers & dynamic memory, and why value semantics eliminate alias analysis complexity."*

---

## 4. Person C — Timing Harness, ML Recommendation Model & Demo

* **Goal:** Automate 64-combo timing sweeps, train the pass recommendation model, and build the interactive demo.
* **Target Directory:** `src/minic/harness/`, `src/minic/ml/`, `demo/`

### Step-by-Step Action Plan:

#### Step 1: Build Timing Harness (`src/minic/harness/`)
1. `compiler.py`: Calls `gcc -O0 -o temp.exe temp.c` using `subprocess.run()`.
2. `timer.py`: Executes `temp.exe` 20 times:
   - Discards the first 3 runs (warm-up).
   - Takes the median of the remaining 17 runs using `time.perf_counter_ns()`.

#### Step 2: Automated Sweep Script (`src/minic/harness/sweeper.py`)
Loop over all 35 benchmarks $\times$ 64 combinations = **2,240 rows**:
1. For each program, extract 18 static features via Person A's `FeatureExtractor`.
2. For each combo $0..63$, apply Person B's `optimize_program`, generate C code via `CEmitter`, compile with `gcc -O0`, and record `median_time_ms`.
3. Compute speedup ratio: $\text{speedup} = T_{\text{combo 0}} / T_{\text{combo } k}$.
4. Save to `data/benchmark_dataset.csv`.

#### Step 3: Train Machine Learning Model (`src/minic/ml/`)
1. **Model:** Train a `RandomForestRegressor` or `GradientBoostingRegressor` on `[18 Static Features + 5 One-Hot Combo Flags] -> speedup_ratio`.
2. **Cross-Validation:** MUST use `GroupKFold(n_splits=5)` grouped strictly by `program_id` to prevent data leakage across combinations of the same benchmark.
3. **Inference / Recommendation:**
   ```python
   def recommend_combo(features: dict) -> int:
       # Evaluate predicted speedup for all 64 combos and pick the argmax
       best_combo = 0
       best_speedup = 0.0
       for combo in range(64):
           pred = model.predict([features + one_hot(combo)])
           if pred > best_speedup:
               best_speedup = pred
               best_combo = combo
       return best_combo
   ```

#### Step 4: Interactive Demo UI (`demo/app.py`)
Build a lightweight Streamlit app:
- Input: Paste MiniC source code.
- Features: Displays radar chart of extracted static metrics.
- Recommendation: Highlights the recommended optimization combo (e.g. `CF + CSE + LICM`).
- Speedup: Shows baseline execution time vs. optimized execution time and percentage speedup.

---

## 5. Summary Dependency Graph

```
[Person A: Front-End & TAC] (DONE)
        │
        ├───> [Person B: 5 Passes + IR-to-C Codegen]
        │             │
        │             v
        └───> [Person D: 35 Benchmarks] ───> [Person C: Sweep 2,240 Rows]
                                                      │
                                                      v
                                            [Person C: Train ML Model]
                                                      │
                                                      v
                                            [Person C: Streamlit Demo]
```
