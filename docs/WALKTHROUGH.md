# MiniC Optimizer — end-to-end walkthrough

This traces **one program through every stage** of the system: lexer → parser →
AST → semantic analysis → TAC IR → control-flow graph → feature extraction →
optimization passes → C codegen → compile & time → ML pass recommendation.

Every block below is real output from the tools in this repo. The running example
is [`docs/walk.mc`](walk.mc) — reproduce any stage with
`python -m src.minic.driver docs/walk.mc --<flag>`.

---

## 0 · The example program

[`docs/walk.mc`](walk.mc):

```c
int main() {
    int scale = 8;
    int total = 0;
    int i = 0;
    while (i < 1000) {
        total = total + i * scale + i * scale;
        i = i + 1;
    }
    return total % 256;
}
```

Small on purpose — every stage's output stays readable. It still contains three
things the optimizer can exploit: a constant (`scale = 8`), a repeated
subexpression (`i * scale` twice), and a loop-carried multiply (`i * scale`).

> MiniC is C with **no pointers, no `malloc`, no I/O**. A program's entire
> observable result is `main()`'s return value (0–255). No pointers means **no
> aliasing**, which is what makes every pass below provably sound.

---

## 1 · Lexer — text → tokens

`src/minic/frontend/lexer.py`. Scans the raw source into a flat token stream,
each token tagged with its kind and source line.

```
TokenType.INT          'int'   line 1
TokenType.IDENT       'main'   line 1
TokenType.LPAREN         '('   line 1
TokenType.RPAREN         ')'   line 1
TokenType.LBRACE         '{'   line 1
TokenType.INT          'int'   line 2
TokenType.IDENT      'scale'   line 2
TokenType.ASSIGN         '='   line 2
TokenType.INT_LIT          8   line 2
TokenType.SEMICOLON      ';'   line 2
TokenType.WHILE      'while'   line 5
TokenType.IDENT          'i'   line 5
TokenType.LT             '<'   line 5
TokenType.INT_LIT       1000   line 5
...
```

Token kinds: keywords (`int float char struct if else while for return`),
identifiers, `int` / `float` / `char` / string literals, operators, punctuation.
Line numbers are attached here and carried all the way to error messages.

---

## 2 · Parser — tokens → Abstract Syntax Tree

`src/minic/frontend/parser.py` — a hand-written recursive-descent parser matching
the MiniC grammar (`docs/spec/minic-language-spec.md`).

```bash
python -m src.minic.driver walk.mc --tree
```

```
Program (L0)
└── FuncDecl: main -> int (L1)
    └── Body
        ├── VarDecl: int scale (L2)
        │   └── Init
        │       └── Literal(int: 8)
        ├── VarDecl: int total (L3)
        │   └── Init
        │       └── Literal(int: 0)
        ├── VarDecl: int i (L4)
        │   └── Init
        │       └── Literal(int: 0)
        ├── WhileStmt (L5)
        │   ├── Condition
        │   │   └── BinaryExpr(<)
        │   │       ├── Left
        │   │       │   └── Var(i)
        │   │       └── Right
        │   │           └── Literal(int: 1000)
        │   └── Body
        │       └── Block (L5)
        │           ├── ExprStmt (L6)
        │           │   └── Assign '=' (L6)
        │           │       ├── Target
        │           │       │   └── Var(total)
        │           │       └── Value
        │           │           └── BinaryExpr(+)
        │           │               ├── Left
        │           │               │   └── BinaryExpr(+)
        │           │               │       ├── Left
        │           │               │       │   └── Var(total)
        │           │               │       └── Right
        │           │               │           └── BinaryExpr(*)   [ Var(i) * Var(scale) ]
        │           │               └── Right
        │           │                   └── BinaryExpr(*)           [ Var(i) * Var(scale) ]
        │           └── ExprStmt (L7)
        │               └── Assign '=' (L7)                         [ i = i + 1 ]
        └── ReturnStmt (L9)
            └── BinaryExpr(%)                                       [ Var(total) % 256 ]
```

*(The two `BinaryExpr(*)` and `i = i + 1` subtrees are abbreviated above; run the
command for the full tree.)*

The AST is the last representation that still looks like the source. Node types
live in `src/minic/frontend/ast_nodes.py` (`Program`, `FuncDecl`, `StructDecl`,
`VarDecl`, `WhileStmt`, `BinaryExpr`, `ArrayAccessExpr`, `FieldAccessExpr`,
`CallExpr`, …).

---

## 3 · Semantic analysis — is the program *valid*?

`src/minic/frontend/sema.py`. Walks the AST and rejects programs that parse but
don't make sense. Checks include:

| check | example rejection |
|---|---|
| every variable declared before use | `Undeclared variable 'y'` |
| every called function exists, arg count matches | `Call to undeclared function 'foo'` |
| operator / operand types agree | `Binary operator '+' not supported on types int and struct Point` |
| array subscripts are integers, ≤ 2 dimensions | `Array subscript must be an integer, got float` |
| assignment target is an l-value | `Invalid l-value on left side of assignment` |
| structs are not recursively sized | `Struct 'Node' contains itself` |
| non-void functions return a value | `Non-void function 'f' must return a value` |
| no duplicate declarations (var / param / struct field / function) | `Redefinition of variable 'x'` |

Errors carry a line, a column, and a caret:

```
[SemanticError] Line 3, Column 16: Undeclared variable 'y'
      return x + y;
                 ^
```

(Parse errors look the same — `[ParserError] Line 2, Column 13: Expected
expression, got ';'`.)

`walk.mc` passes cleanly, so analysis is silent.

---

## 4 · IR generation — AST → three-address code (TAC)

`src/minic/ir/ir_generator.py`. Lowers the tree into a flat list of simple
instructions — at most one operation each, explicit temporaries (`t0`, `t1`, …),
explicit control flow with labels and conditional jumps. This is the form every
optimization pass and the C emitter work on.

```bash
python -m src.minic.driver walk.mc --tac
```

```
func main() -> int:
    alloc scale : int
    scale = 8
    alloc total : int
    total = 0
    alloc i : int
    i = 0
L_while_start0:
    t0 = i < 1000
    ifFalse t0 goto L_while_end1
    t1 = i * scale
    t2 = total + t1
    t3 = i * scale          ← identical to t1
    t4 = t2 + t3
    total = t4
    t5 = i + 1
    i = t5
    goto L_while_start0
L_while_end1:
    t6 = total % 256
    return t6
```

Instruction / operand types are in `src/minic/ir/tac.py`
(`TACInstruction`, `Temp`, `Var`, `Constant`, `Label`, `TACFunction`,
`TACProgram`). Arrays, structs, and strings are lowered with **value semantics** —
passing one copies it — because that's what MiniC guarantees.

---

## 5 · Control-flow graph — structure for the analyses

`src/minic/ir/cfg.py`. Splits the instruction list into **basic blocks** (straight-line
runs), connects them with edges, and finds **natural loops** via back-edges and
dominators. LICM, strength reduction, and unrolling all need this.

```bash
python -m src.minic.driver walk.mc --cfg
```

```
--- Function: main (Blocks: 4, Loops: 1, Max Depth: 1) ---
BasicBlock 0 (Preds: Entry) -> (Succs: BB1)
    alloc scale : int ; scale = 8 ; alloc total ; total = 0 ; alloc i ; i = 0
BasicBlock 1 [L_while_start0] (Preds: BB0, BB2) -> (Succs: BB3, BB2)
    t0 = i < 1000 ; ifFalse t0 goto L_while_end1
BasicBlock 2 (Preds: BB1) -> (Succs: BB1)              ← the loop body
    t1 = i * scale ; t2 = total + t1 ; t3 = i * scale ; t4 = t2 + t3
    total = t4 ; t5 = i + 1 ; i = t5 ; goto L_while_start0
BasicBlock 3 [L_while_end1] (Preds: BB1) -> (Succs: Exit)
    t6 = total % 256 ; return t6
```

`BB2 -. Loop Back-Edge .-> BB1` — BB1 is the loop **header**, BB2 the **latch**.
`--cfg` also prints a Mermaid diagram of the same thing.

---

## 6 · Feature extraction — what the ML model reads

`src/minic/features/`. Produces **27 numbers** per program, entirely from the AST
and TAC — no execution:

```bash
python -m src.minic.driver walk.mc --features
```

```json
{
  "total_instructions": 20, "basic_block_count": 4,
  "loop_count": 1, "max_loop_depth": 1,
  "branch_count": 1, "branch_density": 0.05,
  "arithmetic_ops_count": 6, "multiplication_count": 2,
  "constant_load_count": 6, "array_access_count": 0, "array_2d_access_count": 0,
  "struct_access_count": 0, "function_call_count": 0, "recursive_call_count": 0,
  "named_variable_count": 3, "temp_variable_count": 7, "string_ops_count": 0,
  "instruction_density_in_loops": 0.55, "cyclomatic_complexity": 2,

  "opp_const_foldable": 0, "opp_cse_redundant": 1, "opp_licm_hoistable": 0,
  "opp_sr_reducible": 0, "opp_unrollable_loops": 0,
  "opp_loop_body_insts": 11, "opp_hot_invariant_frac": 0.0,
  "opp_est_dyn_kilo_insts": 11
}
```

- **19 structural** features (`src/minic/features/extractor.py`): loop nesting,
  branch density, the instruction-type histogram, variable counts, cyclomatic
  complexity, …
- **8 "opportunity" features** (`src/minic/features/opportunity.py`): a cheap
  static estimate of *how much each pass would actually change* — here it spotted
  `opp_cse_redundant = 1` (one repeated subexpression). These give the model a
  preview of each pass's payoff without running anything.

---

## 7 · Optimization passes — 6 toggles, 64 combinations

`src/minic/optimizer/`. Six passes, each one bit:

| bit | pass | what it does |
|---:|---|---|
| 1  | **CF** — constant folding & propagation | evaluate constant expressions; propagate single-assignment constants; algebraic identities. 32-bit two's-complement, C division/modulo semantics. |
| 2  | **DCE** — dead-code elimination | drop instructions whose results are never used; unreachable blocks; dead `alloc`s. |
| 4  | **CSE** — common-subexpression elimination | local value numbering + copy propagation: compute a repeated expression once. |
| 8  | **LICM** — loop-invariant code motion | hoist computations that don't change across iterations into a pre-header. |
| 16 | **SR** — strength reduction | turn a loop-varying multiply (`i * k`) into an addition (`acc += k`). |
| 32 | **LU** — loop unrolling | duplicate a counted loop body ×4, keep the original as a remainder loop. |

`combo_id` is the OR of the bits; `combo 0` = untouched, `combo 63` = all six.

### Passes enable each other

Run **CF alone** (`--optimize 1`) on `walk.mc`:

```
    t1 = i * 8             ← scale propagated: i * scale  →  i * 8
    t2 = total + t1
    t3 = i * 8
    t4 = t2 + t3
```

Now **SR alone** (`--optimize 16`) does **nothing** — it needs `i * <constant>`,
but before CF the operand is the *variable* `scale`. It's only once CF has run
that SR has something to reduce.

Run **CF + CSE + SR** (`--optimize 21`):

```
    __sr7 = 0             ← induction expression seeded before the loop
L_while_start0:
    t0 = i < 1000
    ifFalse t0 goto L_while_end1
    t2 = total + __sr7    ← both "i * scale" are now just __sr7 — no multiply
    t4 = t2 + __sr7
    total = t4
    t5 = i + 1
    i = t5
    __sr7 = __sr7 + 8     ← strength reduction: one add per iteration, not a multiply
    goto L_while_start0
```

Run **all six** (`--optimize 63`): the above, plus DCE removes `alloc scale`, plus
LU unrolls the loop body ×4. The pass manager (`pass_manager.py`) applies the
canonical order **CF → CSE → LU → LICM → SR → DCE** and **repeats it to a fixed
point** so each pass cleans up after the others.

> This is exactly why "just turn everything on" isn't the answer and a
> per-program recommender is worth having — see [`../RESULTS.md`](../RESULTS.md):
> all-six-on is *not* the fastest choice on 243 of 270 benchmarks.

---

## 8 · Code generation — TAC → value-semantics C

`src/minic/codegen/c_emitter.py`. Emits C that a normal `gcc` can compile, while
preserving MiniC's copy semantics.

```bash
python -m src.minic.driver walk.mc --optimize 0 --emit-c
```

```c
// Generated by MiniC Compiler Optimizer
int main(void);
int main(void) {
    int i = (int){0};
    int scale = (int){0};
    int t0 = (int){0}; /* ... one C local per TAC temp ... */
    int total = (int){0};
    scale = 8;
    total = 0;
    i = 0;
    L_while_start0: ;
    t0 = i < 1000;
    if (!(t0)) goto L_while_end1;
    t1 = i * scale;
    t2 = total + t1;
    t3 = i * scale;
    t4 = t2 + t3;
    total = t4;
    t5 = i + 1;
    i = t5;
    goto L_while_start0;
    L_while_end1: ;
    t6 = total % 256;
    return t6;
}
```

Arrays / structs / strings become **one-field wrapper structs** (`arr_int_3_3`,
`str_6`) so that C assignment stays a copy; string literals use C99 compound
literals. Typedefs are emitted in dependency order.

---

## 9 · Compile & time — the measurement

`src/minic/harness/`. Each emitted C file is compiled with **`gcc -O0`** and the
binary is executed several times; we keep the median (playground) or the minimum
(research sweep).

`-O0` is deliberate: at `-O0` the C compiler does essentially nothing, so the
measured difference between combo 0 and combo N is **our optimizer's** work, not
gcc's.

**The correctness gate:** every optimized binary must reproduce combo 0's exit
code before its timing is recorded (`timer.py` raises if it doesn't). Across the
full 270-program × 64-combo sweep — 17,280 binaries — **zero disagreed**.

For `walk.mc` (loop bound raised to 20 M so it's above timer noise):

```
$ python -m demo.cli --runs 9 recommend walk.mc --verify
ML-recommended combo: 55  [CF, DCE, CSE, SR, LU]   predicted speedup x1.79
measured:  baseline 54.58 ms   combo 55 43.19 ms   speedup x1.26   (exit 0, match True)
```

---

## 10 · The ML recommender — features → which passes

`src/minic/ml/`. Given the 27 features of a program it has **never run**, predict
the combo to use.

- **Training data:** the sweep CSV — one row per (program, combo) with the 27
  features, the 6 pass-flag bits, and the measured `speedup_ratio`.
- **Model:** the winner of a cross-validated bake-off
  (`train.py::choose_strategy`): **HistGradientBoosting** regressor +
  an **abstain margin**. For a new program it scores all 64 combos and takes the
  best — *unless* even the best predicted speedup is below ×1.12, in which case it
  recommends **no passes** rather than risk a slowdown.
- **Validation:** `GroupKFold` on `program_id` — whole programs are held out. A
  program's 64 rows share identical features, so a random split would leak.

Held-out results ([`../RESULTS.md`](../RESULTS.md)): recommended combo runs
**×1.23** on average vs a **×1.54** best-in-hindsight oracle (44% of the available
speedup), and only **9%** of recommendations land below baseline — down from 21%
for naive argmax, which is what the abstain margin buys.

The **playground** (`demo/app.py`, `python -m demo.app`) runs this whole chain
live: it compiles your program two ways, times both, checks they agree, and shows
the recommended passes, a per-pass "what it changed" table, and the TAC diff. Pick
**"Custom — write your own"** in the dropdown to run your own MiniC.

---

## The canonical example

`canonical_example.mc` is the program used as the 64-combo correctness fixture. It
deliberately exercises **every** MiniC feature at once:

```c
struct Point { int x; int y; };

int matrixSum(int m[3][3]) {          // 2-D array parameter, nested loops
    int total = 0; int i = 0;
    while (i < 3) {
        int j = 0;
        while (j < 3) { total = total + m[i][j]; j = j + 1; }
        i = i + 1;
    }
    return total;
}

int distanceSquared(struct Point a, struct Point b) {   // struct-by-value params
    int dx = a.x - b.x; int dy = a.y - b.y;
    return dx * dx + dy * dy;
}

int fib(int n) {                     // recursion
    if (n < 2) { return n; }
    return fib(n - 1) + fib(n - 2);
}

int main() {
    char label[6] = "grid1";         // string literal init
    struct Point p1; p1.x = 0; p1.y = 0;
    struct Point p2; p2.x = 3; p2.y = 4;
    int grid[3][3];
    grid[0][0] = 1; grid[0][1] = 0; grid[0][2] = 0;
    grid[1][0] = 0; grid[1][1] = 1; grid[1][2] = 0;
    grid[2][0] = 0; grid[2][1] = 0; grid[2][2] = 1;
    int d = distanceSquared(p1, p2); // 9 + 16 = 25
    int s = matrixSum(grid);         // trace = 3
    int f = fib(10);                 // 55
    return d + s + f;                // 25 + 3 + 55 = 83
}
```

```bash
python -m src.minic.driver canonical_example.mc --optimize 0  --run   # → 83
python -m src.minic.driver canonical_example.mc --optimize 63 --run   # → 83  (must match)
```

Every one of the 64 combos, for this program and for all 270 benchmarks, must
return the same value as combo 0.

---

## Reproduce every stage

```bash
cd "path/to/repo"
F=docs/walk.mc               # the example above — or canonical_example.mc, or your own

python -m src.minic.driver $F --tree                    # AST
python -m src.minic.driver $F --tac                     # TAC IR
python -m src.minic.driver $F --cfg                     # basic blocks + loops + Mermaid
python -m src.minic.driver $F --features                # the 27 ML features
python -m src.minic.driver $F --optimize 1  --tac       # CF only
python -m src.minic.driver $F --optimize 63 --tac       # all six passes
python -m src.minic.driver $F --optimize 63 --emit-c    # generated C
python -m src.minic.driver $F --optimize 63 --run       # compile with gcc -O0 and run

python -m demo.cli recommend $F --verify                # ML pick + measured before/after
python -m demo.app                                      # the browser playground
python run_experiment.py --skip-sweep                   # re-run the ML bake-off from the CSV
```
