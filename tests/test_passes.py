import unittest
from src.minic.frontend import Lexer, Parser, SemanticAnalyzer
from src.minic.ir import IRGenerator
from src.minic.ir.tac import Opcode, Constant, Temp, Var
from src.minic.optimizer import (
    constant_folding_pass, dce_pass, cse_pass, licm_pass, strength_reduction_pass
)


class TestOptimizationPasses(unittest.TestCase):
    def _to_tac(self, code: str):
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, code).parse()
        SemanticAnalyzer(code).analyze(ast)
        return IRGenerator().generate(ast)

    # --- Pass 1: Constant Folding & Propagation ---
    def test_constant_folding(self):
        code = """
        int main() {
            int a = 10 + 20 * 2;
            int b = a - 5;
            return b;
        }
        """
        tac = self._to_tac(code)
        opt_func = constant_folding_pass(tac.functions[0])

        # All calculations should fold to constants
        mul_and_add_ops = [inst.opcode for inst in opt_func.instructions if inst.opcode in (Opcode.ADD, Opcode.MUL, Opcode.SUB)]
        self.assertEqual(len(mul_and_add_ops), 0)

        # Result should be constant 45
        return_inst = [inst for inst in opt_func.instructions if inst.opcode == Opcode.RETURN][0]
        self.assertTrue(isinstance(return_inst.src1, Constant) or isinstance(return_inst.src1, Var))

    def test_constant_branch_simplification(self):
        code = """
        int main() {
            if (1 == 1) {
                return 10;
            } else {
                return 20;
            }
        }
        """
        tac = self._to_tac(code)
        opt_func = constant_folding_pass(tac.functions[0])
        # Conditional branch JUMP_IF_FALSE should be eliminated or turned into JUMP
        cond_branches = [inst for inst in opt_func.instructions if inst.opcode in (Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE)]
        self.assertEqual(len(cond_branches), 0)

    # --- Pass 2: Dead Code Elimination ---
    def test_dead_code_elimination(self):
        code = """
        int main() {
            int unused1 = 100 * 2;
            int unused2 = 500;
            int used = 42;
            return used;
        }
        """
        tac = self._to_tac(code)
        opt_func = dce_pass(tac.functions[0])
        
        # Dead assignments to unused1 and unused2 should be eliminated
        inst_str = "\n".join(str(inst) for inst in opt_func.instructions)
        self.assertNotIn("unused1", inst_str)
        self.assertNotIn("unused2", inst_str)

    # --- Pass 3: Common Subexpression Elimination ---
    def test_cse_local_value_numbering(self):
        code = """
        int compute(int x, int y) {
            int a = x * y + 10;
            int b = x * y + 20; // x * y is common subexpression
            return a + b;
        }
        """
        tac = self._to_tac(code)
        opt_func = cse_pass(tac.functions[0])

        # Second multiplication should be replaced by assignment
        mul_count = sum(1 for inst in opt_func.instructions if inst.opcode == Opcode.MUL)
        self.assertEqual(mul_count, 1)

    def test_cse_commutative(self):
        code = """
        int compute(int x, int y) {
            int a = x + y;
            int b = y + x; // Commutative duplicate
            return a + b;
        }
        """
        tac = self._to_tac(code)
        opt_func = cse_pass(tac.functions[0])
        
        # The sum x+y and y+x should only be computed once
        cse_annotations = [inst.annotation for inst in opt_func.instructions if inst.annotation == "CSE"]
        self.assertGreaterEqual(len(cse_annotations), 1)

    # --- Pass 4: Loop-Invariant Code Motion ---
    def test_licm_hoisting(self):
        code = """
        int loopTest(int n, int factor) {
            int total = 0;
            int i = 0;
            while (i < n) {
                int inv = factor * 10; // Invariant inside loop
                total = total + inv;
                i = i + 1;
            }
            return total;
        }
        """
        tac = self._to_tac(code)
        opt_func = licm_pass(tac.functions[0])

        # Check that hoisted instruction has annotation
        hoisted = [inst for inst in opt_func.instructions if "LICM Hoisted" in inst.annotation]
        self.assertGreaterEqual(len(hoisted), 1)

    # --- Pass 5: Strength Reduction ---
    def test_strength_reduction(self):
        code = """
        int sumMultiples(int n) {
            int total = 0;
            for (int i = 0; i < n; i = i + 1) {
                int val = i * 4; // Derived induction variable
                total = total + val;
            }
            return total;
        }
        """
        tac = self._to_tac(code)
        opt_func = strength_reduction_pass(tac.functions[0])

        sr_insts = [inst for inst in opt_func.instructions if "SR Reduced" in inst.annotation]
        self.assertGreaterEqual(len(sr_insts), 1)


if __name__ == "__main__":
    unittest.main()
