import unittest
import os
import shutil
import subprocess
import tempfile
from src.minic.frontend import Lexer, Parser, SemanticAnalyzer
from src.minic.ir import IRGenerator
from src.minic.optimizer import PassManager, optimize_program, get_pass_names
from src.minic.codegen import CEmitter


class TestOptimizerSweep(unittest.TestCase):
    def _run_64_combo_sweep(self, program_code: str, expected_exit_code: int, test_name: str):
        tokens = Lexer(program_code).tokenize()
        ast = Parser(tokens, program_code).parse()
        SemanticAnalyzer(program_code).analyze(ast)
        tac_base = IRGenerator().generate(ast)
        emitter = CEmitter()
        exe = ".exe" if os.name == "nt" else ""
        workdir = tempfile.mkdtemp(prefix=f"minic_sweep_{test_name}_")

        try:
            for combo in range(64):
                opt_tac = optimize_program(tac_base, combo)
                c_code = emitter.emit(opt_tac)

                c_file = os.path.join(workdir, f"{test_name}_{combo}.c")
                bin_file = os.path.join(workdir, f"{test_name}_{combo}{exe}")

                with open(c_file, "w") as f:
                    f.write(c_code)

                comp = subprocess.run(["gcc", "-O0", "-o", bin_file, c_file], capture_output=True, text=True)
                self.assertEqual(
                    comp.returncode, 0,
                    f"Combo {combo} ({bin(combo)}) failed GCC compilation for {test_name}:\n{comp.stderr}\nCode:\n{c_code}"
                )

                run = subprocess.run([bin_file])
                self.assertEqual(
                    run.returncode, expected_exit_code,
                    f"Combo {combo} ({bin(combo)}) produced incorrect output {run.returncode}, expected {expected_exit_code} for {test_name}"
                )
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    def test_canonical_example_64_combos(self):
        canon = os.path.join(os.path.dirname(__file__), os.pardir, "canonical_example.mc")
        with open(canon, "r", encoding="utf-8") as f:
            code = f.read()
        self._run_64_combo_sweep(code, 83, "canonical")

    def test_numeric_matrix_mult_64_combos(self):
        code = """
        int matMulSum() {
            int a[2][2];
            int b[2][2];
            int c[2][2];
            a[0][0] = 1; a[0][1] = 2;
            a[1][0] = 3; a[1][1] = 4;
            b[0][0] = 5; b[0][1] = 6;
            b[1][0] = 7; b[1][1] = 8;

            int sum = 0;
            for (int i = 0; i < 2; i = i + 1) {
                for (int j = 0; j < 2; j = j + 1) {
                    int cell = 0;
                    for (int k = 0; k < 2; k = k + 1) {
                        cell = cell + a[i][k] * b[k][j];
                    }
                    c[i][j] = cell;
                    sum = sum + cell;
                }
            }
            // c[0][0] = 19, c[0][1] = 22, c[1][0] = 43, c[1][1] = 50 -> sum = 134
            return sum;
        }

        int main() {
            return matMulSum();
        }
        """
        self._run_64_combo_sweep(code, 134, "mat_mul")

    def test_struct_particles_64_combos(self):
        code = """
        struct Particle {
            int x;
            int y;
            int vx;
            int vy;
        };

        int main() {
            struct Particle p;
            p.x = 10;
            p.y = 20;
            p.vx = 2;
            p.vy = 3;

            for (int step = 0; step < 5; step = step + 1) {
                p.x = p.x + p.vx;
                p.y = p.y + p.vy;
            }
            // After 5 steps: x = 10 + 10 = 20, y = 20 + 15 = 35 -> 20 + 35 = 55
            return p.x + p.y;
        }
        """
        self._run_64_combo_sweep(code, 55, "particles")

    def test_pass_names_and_manager(self):
        names_0 = get_pass_names(0)
        self.assertEqual(len(names_0), 0)

        names_63 = get_pass_names(63)
        self.assertEqual(len(names_63), 6)  # CF DCE CSE LICM SR LU

        names_5 = get_pass_names(1 | 4)  # CF + CSE
        self.assertEqual(len(names_5), 2)
        self.assertIn("Constant Folding (CF)", names_5)
        self.assertIn("Common Subexpression Elimination (CSE)", names_5)


if __name__ == "__main__":
    unittest.main()
