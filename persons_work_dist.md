# MiniC Compiler Optimizer — Work Distribution & Role Specification

### Person A — Front-End + IR Generator + Static Feature Extractor
* **Scope:** Lexer $\rightarrow$ Recursive-descent parser (matching MiniC BNF grammar) $\rightarrow$ AST $\rightarrow$ Semantic analysis (type-checking, array dimension checks, lvalue checks, nominal struct matching) $\rightarrow$ Lowering to Three-Address Code (TAC).
* **Feature Extraction:** Walks AST/TAC to compute the static feature vector for each program: loop count, max loop nesting depth, basic block count, branch density, instruction-type histogram, struct field count, array dimensionality.
* **Deliverables:** Validated TAC dump + static feature dictionary (`dict`) per MiniC program.
* **Testing:** Uses the canonical example program to verify front-end and IR correctness against hand-derived expected TAC.

---

### Person B — Optimization Passes + IR-to-C Codegen
* **Scope:** 
  1. **Optimization Pass Library (5 standalone toggleable passes):** Constant Folding, Dead Code Elimination (backward liveness), Common Subexpression Elimination (value numbering per basic block), Loop-Invariant Code Motion (hoisting to loop preheader), and Strength Reduction. 
  2. **Pass Controller:** Configured via a 5-bit flag enabling any of the 64 optimization pass combinations.
  3. **Codegen (IR $\rightarrow$ C):** Translates optimized TAC back into C text. Wraps every array, string, and struct in a 1-field C `struct` wrapper (e.g. `typedef struct { char data[6]; } str_6;`) to enforce MiniC value semantics. Lowers string literal assignments using C99 compound literals (e.g. `s = (str_6){ .data = "hello" };`).
* **Correctness Check:** Every one of the 64 pass combinations MUST produce identical program output as the unoptimized baseline on every benchmark.

---

### Person C — Timing Harness + Dataset Assembly + ML Model + Demo Interface
* **Scope:**
  1. **Timing Harness:** Compiles emitted C code with `gcc -O0`, executes binaries 15–20 times (discarding initial warm-up runs), and records median wall-clock execution time (`time.perf_counter()`).
  2. **Sweep Automation:** Sweeps all 64 optimization combinations across all 30–40 benchmark programs to generate the complete dataset (~2,000–2,500 rows).
  3. **ML Model:** Trains a recommendation model (Random Forest / Gradient Boosted Trees). **Crucial Requirement:** Must use `GroupKFold` cross-validation grouped by `program_id` so rows from the same program do not leak across training and test splits.
  4. **Recommendation Demo:** End-to-end pipeline CLI / UI (Streamlit): input MiniC file $\rightarrow$ extract features $\rightarrow$ predict best combo $\rightarrow$ optimize & codegen $\rightarrow$ compile & run $\rightarrow$ display measured speedup % against baseline and optimal combo.

---

### Person D — Benchmark Corpus + Correctness Oracle + Report Architecture
* **Scope:**
  1. **Benchmark Suite:** Writes **30–40 MiniC benchmark programs** covering 2D array traversals, struct arithmetic, fixed string processing, recursion, LICM-friendly loops, and strength-reduction loops.
  2. **High Trip Counts:** Programs MUST feature high computational weight (thousands to millions of loop iterations) so runtime differences under `gcc -O0` exceed timing noise (>100ms per run).
  3. **Ground Truth Oracle:** Provides equivalent standard C reference programs and hand-verified outputs to build an automated reference output table.
  4. **Report & Documentation:** Authors report sections explaining MiniC design decisions (why pointers are omitted, alias analysis complexity, value semantics vs reference semantics).