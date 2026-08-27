import unittest
import os
import subprocess
from src.minic.frontend import Lexer, Parser, SemanticAnalyzer
from src.minic.ir import IRGenerator
from src.minic.codegen import CEmitter


class TestCEmitter(unittest.TestCase):
    def _compile_and_run(self, code: str, expected_exit_code: int):
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, code).parse()
        SemanticAnalyzer(code).analyze(ast)
        tac = IRGenerator().generate(ast)
        c_code = CEmitter().emit(tac)

        c_file = "temp_test_codegen.c"
        bin_file = "./temp_test_codegen"

        with open(c_file, "w") as f:
            f.write(c_code)

        try:
            comp = subprocess.run(["gcc", "-O0", "-o", bin_file, c_file], capture_output=True, text=True)
            self.assertEqual(comp.returncode, 0, f"GCC Compilation failed:\n{comp.stderr}\nEmitted C:\n{c_code}")

            run = subprocess.run([bin_file])
            self.assertEqual(run.returncode, expected_exit_code)
        finally:
            if os.path.exists(c_file):
                os.remove(c_file)
            if os.path.exists(bin_file):
                os.remove(bin_file)

    def test_simple_return(self):
        code = """
        int main() {
            return 42;
        }
        """
        self._compile_and_run(code, 42)

    def test_arithmetic_and_function_call(self):
        code = """
        int compute(int a, int b) {
            return a * b + (a - b);
        }
        int main() {
            return compute(6, 4); // 24 + 2 = 26
        }
        """
        self._compile_and_run(code, 26)

    def test_1d_array_value_semantics(self):
        code = """
        int sumArr(int a[3]) {
            int total = 0;
            for (int i = 0; i < 3; i = i + 1) {
                total = total + a[i];
            }
            a[0] = 999; // Should NOT modify caller's array (value semantics!)
            return total;
        }
        int main() {
            int arr[3];
            arr[0] = 10;
            arr[1] = 20;
            arr[2] = 30;
            int s = sumArr(arr); // s = 60
            return s + arr[0];    // 60 + 10 = 70
        }
        """
        self._compile_and_run(code, 70)

    def test_2d_array_value_semantics(self):
        code = """
        int sumMatrix(int m[2][2]) {
            int total = 0;
            for (int i = 0; i < 2; i = i + 1) {
                for (int j = 0; j < 2; j = j + 1) {
                    total = total + m[i][j];
                }
            }
            m[0][0] = 999; // Value semantics check
            return total;
        }
        int main() {
            int mat[2][2];
            mat[0][0] = 1; mat[0][1] = 2;
            mat[1][0] = 3; mat[1][1] = 4;
            int s = sumMatrix(mat); // 10
            return s + mat[0][0];   // 10 + 1 = 11
        }
        """
        self._compile_and_run(code, 11)

    def test_struct_copy_semantics(self):
        code = """
        struct Point {
            int x;
            int y;
        };
        int mutatePoint(struct Point p) {
            p.x = 100;
            return p.x + p.y;
        }
        int main() {
            struct Point pt;
            pt.x = 5;
            pt.y = 15;
            int res = mutatePoint(pt); // 115
            return pt.x + res;         // 5 + 115 = 120
        }
        """
        self._compile_and_run(code, 120)

    def test_string_literal_assignment(self):
        code = """
        int main() {
            char str1[6] = "hello";
            char str2[6];
            str2 = "world";
            return 1;
        }
        """
        self._compile_and_run(code, 1)


if __name__ == "__main__":
    unittest.main()
