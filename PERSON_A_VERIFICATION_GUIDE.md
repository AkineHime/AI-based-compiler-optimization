# Person A Pipeline Verification Guide
**Target Audience:** Person B, Person C, Person D, or Reviewers checking Person A's front-end & IR implementation.

This guide provides step-by-step instructions, commands, and exact expected outputs to verify that the **Lexer**, **Parser**, **Semantic Analyzer**, **Three-Address Code (TAC) Generator**, and **Static Feature Extractor** are working correctly.

---

## 1. Automated Test Suite (Unit Tests)

### Command:
Run the complete unit test suite from the repository root:
```powershell
python -m unittest discover tests
```

### Expected Output:
```text
................
----------------------------------------------------------------------
Ran 17 tests in 0.005s

OK
```
*(All 17 tests across Lexer, Parser, Semantic Analysis, TAC IR, and Canonical Example must pass with `OK`).*

---

## 2. Testing via CLI Driver (`canonical_example.mc`)

Person A provides a CLI tool (`src.minic.driver`) and the official ground-truth test file (`canonical_example.mc`).

### Test 2.1: Verify Three-Address Code (TAC) Generation
#### Command:
```powershell
python -m src.minic.driver canonical_example.mc
```

#### Expected Output:
```text
=== Three-Address Code (TAC) ===
// --- Struct Definitions ---
struct Point {
    int x;
    int y;
};

func matrixSum(m: int[3][3]) -> int:
    alloc total : int
    total = 0
    alloc i : int
    i = 0
L_while_start0:
    t0 = i < 3
    ifFalse t0 goto L_while_end1
    alloc j : int
    j = 0
L_while_start2:
    t1 = j < 3
    ifFalse t1 goto L_while_end3
    t2 = m[i][j]
    t3 = total + t2
    total = t3
    t4 = j + 1
    j = t4
    goto L_while_start2
L_while_end3:
    t5 = i + 1
    i = t5
    goto L_while_start0
L_while_end1:
    return total

func distanceSquared(a: struct Point, b: struct Point) -> int:
    alloc dx : int
    t6 = a.x
    t7 = b.x
    t8 = t6 - t7
    dx = t8
    alloc dy : int
    t9 = a.y
    t10 = b.y
    t11 = t9 - t10
    dy = t11
    t12 = dx * dx
    t13 = dy * dy
    t14 = t12 + t13
    return t14

func fib(n: int) -> int:
    t15 = n < 2
    ifFalse t15 goto L_endif5
    return n
L_endif5:
    t16 = n - 1
    param t16
    t17 = call fib, 1
    t18 = n - 2
    param t18
    t19 = call fib, 1
    t20 = t17 + t19
    return t20

func main() -> int:
    alloc label : char[6]
    label = "grid1"
    alloc p1 : struct Point
    p1.x = 0
    p1.y = 0
    alloc p2 : struct Point
    p2.x = 3
    p2.y = 4
    alloc grid : int[3][3]
    grid[0][0] = 1
    grid[0][1] = 0
    grid[0][2] = 0
    grid[1][0] = 0
    grid[1][1] = 1
    grid[1][2] = 0
    grid[2][0] = 0
    grid[2][1] = 0
    grid[2][2] = 1
    alloc d : int
    param p1
    param p2
    t21 = call distanceSquared, 2
    d = t21
    alloc s : int
    param grid
    t22 = call matrixSum, 1
    s = t22
    alloc f : int
    param 10
    t23 = call fib, 1
    f = t23
    t24 = d + s
    t25 = t24 + f
    return t25
```

---

### Test 2.2: Verify the 18 Static ML Features Extraction
#### Command:
```powershell
python -m src.minic.driver canonical_example.mc --features
```

#### Expected Output:
```json
=== Extracted Static Features (18 metrics) ===
{
  "total_instructions": 84.0,
  "basic_block_count": 12.0,
  "loop_count": 2.0,
  "max_loop_depth": 2.0,
  "branch_count": 3.0,
  "branch_density": 0.0357,
  "arithmetic_ops_count": 13.0,
  "multiplication_count": 2.0,
  "constant_load_count": 25.0,
  "array_access_count": 10.0,
  "array_2d_access_count": 10.0,
  "struct_access_count": 8.0,
  "function_call_count": 5.0,
  "recursive_call_count": 2.0,
  "variable_count": 42.0,
  "string_ops_count": 1.0,
  "instruction_density_in_loops": 0.2143,
  "cyclomatic_complexity": 6.0
}
```

* **Key Metrics to Verify:**
  - `loop_count`: `2.0` (two while loops in `matrixSum`)
  - `max_loop_depth`: `2.0` (nested loop in `matrixSum`)
  - `recursive_call_count`: `2.0` (`fib(n-1)` and `fib(n-2)`)
  - `multiplication_count`: `2.0` (`dx * dx` and `dy * dy`)
  - `array_2d_access_count`: `10.0` (9 matrix writes + 1 matrix read)

---

### Test 2.3: Verify Abstract Syntax Tree (AST) Hierarchy
#### Command:
```powershell
python -m src.minic.driver canonical_example.mc --ast
```

#### Expected Output Snippet:
```yaml
=== Abstract Syntax Tree (AST) ===
Program (L0)
  StructDecl: Point (L1)
    FieldDecl: int x (L2)
    FieldDecl: int y (L3)
  FuncDecl: matrixSum -> int (L6)
    Params:
      Param: int m [3][3] (L6)
    Body:
      Block (L6)
        VarDecl: int total (L7)
          Init:
            Literal(int: 0) (L7)
  ...
```

---

## 3. Testing with Your Own Custom File (`test.mc`)

You can create and test any custom MiniC program to verify specific language features.

### Step 1: Create `test.mc`
Create a file named `test.mc` in the project root with any valid MiniC code:

```c
// test.mc
int multiplyBySum(int a, int b, int factor) {
    int sum = a + b;
    return sum * factor;
}

int main() {
    int x = 5;
    int y = 10;
    int result = multiplyBySum(x, y, 2);
    return result;
}
```

### Step 2: Run the Commands on `test.mc`

#### 1. Generate Three-Address Code (TAC):
```powershell
python -m src.minic.driver test.mc
```
**Expected Output:**
```text
=== Three-Address Code (TAC) ===
func multiplyBySum(a: int, b: int, factor: int) -> int:
    alloc sum : int
    t0 = a + b
    sum = t0
    t1 = sum * factor
    return t1

func main() -> int:
    alloc x : int
    x = 5
    alloc y : int
    y = 10
    alloc result : int
    param x
    param y
    param 2
    t2 = call multiplyBySum, 3
    result = t2
    return result
```

#### 2. Extract Static Features:
```powershell
python -m src.minic.driver test.mc --features
```
**Expected Output:**
```json
=== Extracted Static Features (18 metrics) ===
{
  "total_instructions": 13.0,
  "basic_block_count": 2.0,
  "loop_count": 0.0,
  "max_loop_depth": 0.0,
  "branch_count": 0.0,
  "branch_density": 0.0,
  "arithmetic_ops_count": 2.0,
  "multiplication_count": 1.0,
  "constant_load_count": 3.0,
  "array_access_count": 0.0,
  "array_2d_access_count": 0.0,
  "struct_access_count": 0.0,
  "function_call_count": 1.0,
  "recursive_call_count": 0.0,
  "variable_count": 8.0,
  "string_ops_count": 0.0,
  "instruction_density_in_loops": 0.0,
  "cyclomatic_complexity": 2.0
}
```

#### 3. View the AST Tree:
```powershell
python -m src.minic.driver test.mc --ast
```

---

## 4. Direct Python API Sanity Check (For Person B & C)

Person B and Person C can run this quick verification script in Python to ensure they can import and use Person A's classes:

```python
from src.minic.frontend import Lexer, Parser, SemanticAnalyzer
from src.minic.ir import IRGenerator, IRPrinter, build_cfg_for_function
from src.minic.features import FeatureExtractor

code = """
int square(int x) {
    return x * x;
}
int main() {
    return square(9);
}
"""

# 1. Lex & Parse
tokens = Lexer(code).tokenize()
ast = Parser(tokens, code).parse()

# 2. Semantic Analysis
SemanticAnalyzer(code).analyze(ast)

# 3. Lower to TAC IR
tac = IRGenerator().generate(ast)
print("--- TAC IR ---")
print(IRPrinter.format_program(tac))

# 4. Inspect CFG
cfg = build_cfg_for_function(tac.functions[0])
print(f"Function {tac.functions[0].name} Basic Blocks:", len(cfg.blocks))

# 5. Extract Feature Vector
features = FeatureExtractor().extract(ast, tac)
print("Total instructions:", features["total_instructions"])
print("Multiplication count:", features["multiplication_count"])
```

### Expected Output:
```text
--- TAC IR ---
func square(x: int) -> int:
    t0 = x * x
    return t0

func main() -> int:
    param 9
    t1 = call square, 1
    return t1

Function square Basic Blocks: 1
Total instructions: 5.0
Multiplication count: 1.0
```

---

## 5. Error Handling Verification

Person A's front-end must reject invalid MiniC code with clean error messages and line pointers.

### Test 5.1: Syntax Error (Missing semicolon / unexpected character)
```python
from src.minic.frontend import Lexer, Parser, MiniCError

try:
    source = "int a = 5"  # Missing semicolon
    tokens = Lexer(source).tokenize()
    Parser(tokens, source).parse()
except MiniCError as e:
    print("Caught expected error:\n", e)
```
**Expected:** `[ParserError] Line 1, Column 10: Expected ';' after variable declaration`

### Test 5.2: Semantic Error (Type mismatch)
```python
from src.minic.frontend import Lexer, Parser, SemanticAnalyzer, MiniCError

try:
    source = """
    int main() {
        int x = "hello"; // Cannot assign string to int
        return x;
    }
    """
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens, source).parse()
    SemanticAnalyzer(source).analyze(ast)
except MiniCError as e:
    print("Caught expected error:\n", e)
```
**Expected:** `[SemanticError] Line 3, Column 9: Type mismatch in initialization of 'x': expected int, got char[6]`

### Test 5.3: Self-Referential Struct Rejection
```python
from src.minic.frontend import Lexer, Parser, SemanticAnalyzer, MiniCError

try:
    source = """
    struct Node {
        int val;
        struct Node next; // Pointers are omitted in MiniC; recursive struct is invalid
    };
    """
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens, source).parse()
    SemanticAnalyzer(source).analyze(ast)
except MiniCError as e:
    print("Caught expected error:\n", e)
```
**Expected:** `[SemanticError] Line 0, Column 0: Recursive struct definition detected: 'Node' contains 'Node'`
