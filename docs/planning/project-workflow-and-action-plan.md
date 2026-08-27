# Project Workflow & Action Plan
## AI-Based Compiler Optimization Recommendation System

Companion to [`../spec/minic-language-spec.md`](../spec/minic-language-spec.md) and `persons_work_dist.md`. This document details the system architecture, team roles, build order, and milestones.

> **Historical document (original plan).** Current state: 6 passes / 64 combos,
> 27 ML features, Flask demo. See [`README.md`](../../README.md) and [`../team/`](../team/).

---

## 1. What This Project Is
Compilers normally run a fixed set of optimization passes on every program. This project builds a custom C-like compiler (**MiniC**) with a library of 5 toggleable classical optimizations (yielding 64 pass combinations). We train a Machine Learning model to inspect a new program's static features and recommend the optimal pass combination—replacing exhaustive search with a fast, learned recommendation.

---

## 2. System Workflow: Two Modes

### Offline Mode: Building the Training Dataset
1. **Benchmark Corpus:** Person D writes 30–40 MiniC programs with high loop trip counts.
2. **Feature Extraction:** Person A parses each program (AST $\rightarrow$ TAC IR) and extracts a static feature vector (loop depth, basic block count, instruction counts, struct/array shapes).
3. **Exhaustive Sweep:** For each program, Person B & C run all 64 pass combinations through IR-to-C codegen, compile with `gcc -O0`, execute 15–20 times, and record median runtime.
4. **Dataset Assembly:** Person C compiles the dataset (~2,000–2,500 total rows: `[program_id, features, combo_bits, median_time_ms]`).

### Online Mode: Recommending for Unseen Code (The Product)
1. A new MiniC program arrives.
2. **Feature Extraction:** Person A's pipeline extracts static features (no execution needed).
3. **Prediction:** Person C's trained ML model predicts the best optimization combination directly.
4. **Optimization & Execution:** Person B's pipeline applies the recommended combo, codegens to C, compiles with `gcc -O0`, executes, and reports the measured speedup against the unoptimized baseline (and compares against the true theoretical optimal combo).

---

## 3. Team Roles & Ownership Matrix

| Role | Teammate | Primary Responsibilities |
| --- | --- | --- |
| **P1** | Person A | Lexer, Recursive-descent Parser, AST, Semantic Checks, TAC IR Generator, Static Feature Extractor. |
| **P2** | Person B | 5 Toggleable Optimization Passes (Constant Folding, DCE, CSE, LICM, Strength Reduction), 64-combo pass manager, **IR $\rightarrow$ C Codegen** (with wrapper structs & compound literal strings). |
| **P3** | Person C | Benchmark Sweep Harness (`gcc -O0` timing with `time.perf_counter()`), Dataset Builder, ML Model Training (`GroupKFold` by program), Demo UI / CLI. |
| **P4** | Person D | Benchmark Corpus (30–40 MiniC programs + standard C reference binaries), Correctness Oracle output table, Theoretical Report section. |

---

## 4. Key Implementation Rules & Technical Safeguards

1. **Language Specification:** See `minic-language-spec.md`. MiniC guarantees **zero aliasing** (no pointers, no dynamic memory, nominal structs, value semantics for arrays/strings/structs).
2. **Codegen String & Array Rule:** All array, string, and struct variables in emitted C must be wrapped in 1-field structs (`typedef struct { T data[N]; } arr_T_N;`). String literal assignments must use C99 compound literals (e.g. `s = (str_6){ .data = "hello" };`).
3. **Execution Timing Safeguard:** `gcc -O0` forces local variable stack-spilling. To prevent measurement noise from drowning out optimization speedups, all benchmark loops MUST have high trip counts so execution times are >100ms.
4. **ML Data Leakage Safeguard:** Person C MUST evaluate models using `GroupKFold` grouped by `program_id`. Standard random splits will cause data leakage because 64 rows share the exact same static feature vector.

---

## 5. Build Order & Milestone Dependencies

| Order | Owner | Can Start When | Notes |
| --- | --- | --- | --- |
| **1** | Person A | Immediately | Parser + TAC IR is on the critical path. |
| **2** | Person B | Immediately (Design); Run on P1 IR | Develop passes on hand-traced TAC IR from canonical example. |
| **3** | Person B | Immediately (Codegen) | Build IR $\rightarrow$ C codegen against hand-written TAC samples. |
| **4** | Person D | Immediately | Write MiniC benchmark programs and C reference binaries. |
| **5** | Person C | Blocked on P1–P4 real outputs | Build timing harness & synthetic ML script first to eliminate idle time. |

---

## 6. Milestones & Checkpoints

1. **Canonical Example Checkpoint:** Canonical program parses, type-checks, and lowers to TAC (Person A).
2. **Pass Verification:** Each of the 5 optimization passes verified individually on TAC (Person B).
3. **First End-to-End Correctness Gate:** Unoptimized TAC $\rightarrow$ Codegen $\rightarrow$ `gcc -O0` $\rightarrow$ Run binary $\rightarrow$ Assert output is **83** for the Canonical Example (Person B & C).
4. **Pass Consistency Gate:** Verify that ALL 64 optimization combinations yield output **83** on canonical example (verifies passes preserve program semantics).
5. **Full Dataset Generation:** 30–40 benchmarks swept across all 64 combos $\rightarrow$ real dataset logged (Person C & D).
6. **Model Training & Recommendation Demo:** Trained model recommends optimal combo on held-out programs with measured speedup reported (Person C).
