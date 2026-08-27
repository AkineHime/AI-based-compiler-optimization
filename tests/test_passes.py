"""Unit tests for the individual optimization passes (Person B)."""
import unittest

from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.sema import SemanticAnalyzer
from src.minic.ir.ir_generator import IRGenerator
from src.minic.ir.tac import Opcode, Constant
from src.minic.optimizer import optimize, combo_flags, combo_label, NUM_COMBOS
from src.minic.optimizer import constant_folding, dce, cse, licm, strength_reduction


def tac(src: str):
    toks = Lexer(src).tokenize()
    ast = Parser(toks, src).parse()
    SemanticAnalyzer(src).analyze(ast)
    return IRGenerator().generate(ast)


def insts(func):
    return list(func.instructions)


class TestConstantFolding(unittest.TestCase):
    def test_folds_and_propagates(self):
        prog = tac("int main() { int a = 3 + 4; int b = a * 2; return b; }")
        constant_folding.run(prog.functions[0], prog)
        # every remaining computation is a literal ASSIGN, no live ADD/MUL
        consts = [i for i in insts(prog.functions[0])
                  if i.opcode == Opcode.ASSIGN and isinstance(i.src1, Constant)]
        self.assertTrue(any(i.src1.value == 7 for i in consts))
        self.assertTrue(any(i.src1.value == 14 for i in consts))

    def test_constant_branch_is_simplified(self):
        # condition (2 < 1) is always false -> the ifFalse branch is always
        # taken and becomes an unconditional jump over the then-block.
        prog = tac("int main() { int c = 0; if (2 < 1) { c = 5; } return c; }")
        f = prog.functions[0]
        constant_folding.run(f, prog)
        self.assertFalse(any(i.opcode == Opcode.JUMP_IF_FALSE for i in insts(f)))
        self.assertTrue(any(i.opcode == Opcode.JUMP for i in insts(f)))

        # condition (1 < 2) is always true -> the ifFalse branch is never taken
        # and is removed outright.
        prog2 = tac("int main() { int c = 7; if (1 < 2) { c = 9; } return c; }")
        f2 = prog2.functions[0]
        constant_folding.run(f2, prog2)
        self.assertFalse(any(i.opcode in (Opcode.JUMP_IF_FALSE, Opcode.JUMP)
                             for i in insts(f2)))


class TestDCE(unittest.TestCase):
    def test_removes_dead_assignment(self):
        prog = tac("int main() { int used = 1; int dead = 2 + 2; return used; }")
        f = prog.functions[0]
        before = len(insts(f))
        dce.run(f, prog)
        after = len(insts(f))
        self.assertLess(after, before)
        self.assertFalse(any(i.opcode == Opcode.ADD for i in insts(f)))


class TestCSE(unittest.TestCase):
    def test_reuses_repeated_expression(self):
        prog = tac("int f(int x,int y){int a=x+y;int b=x+y;return a+b;} "
                   "int main(){return f(1,2);}")
        f = prog.functions[0]
        cse.run(f, prog)
        adds = [i for i in insts(f) if i.opcode == Opcode.ADD]
        # x+y computed once; the second becomes a copy (ASSIGN)
        self.assertEqual(sum(1 for i in adds), 2)  # x+y  and  a+b


class TestLICM(unittest.TestCase):
    def test_hoists_invariant_into_preheader(self):
        src = ("int f(int n){int k=5;int s=0;int i=0;"
               "while(i<n){int c=k*10;s=s+c;i=i+1;}return s;}"
               "int main(){return f(3);}")
        prog = tac(src)
        f = prog.functions[0]
        licm.run(f, prog)
        labels = [str(i.dst) for i in insts(f) if i.opcode == Opcode.LABEL]
        self.assertTrue(any("preheader" in n for n in labels))


class TestStrengthReduction(unittest.TestCase):
    def test_replaces_mul_with_add_accumulator(self):
        src = ("int f(int n){int s=0;int i=0;"
               "while(i<n){int t=i*8;s=s+t;i=i+1;}return s;}"
               "int main(){return f(4);}")
        prog = tac(src)
        f = prog.functions[0]
        strength_reduction.run(f, prog)
        # an sr accumulator is seeded and updated with ADD
        self.assertTrue(any(i.opcode == Opcode.MUL for i in insts(f)))  # the seed
        names = [str(i.dst) for i in insts(f)
                 if i.opcode == Opcode.ADD and str(i.dst).startswith("__sr")]
        self.assertTrue(names)


class TestComboMetadata(unittest.TestCase):
    def test_flag_decoding(self):
        self.assertEqual(combo_flags(0),
                         {"flag_cf": False, "flag_dce": False, "flag_cse": False,
                          "flag_licm": False, "flag_sr": False})
        self.assertEqual(combo_flags(63),
                         {"flag_cf": True, "flag_dce": True, "flag_cse": True,
                          "flag_licm": True, "flag_sr": True})
        self.assertIn("baseline", combo_label(0))

    def test_baseline_is_identity(self):
        prog = tac("int main(){int a=1+1;return a;}")
        out = optimize(prog, 0)
        self.assertEqual([i.opcode for i in out.functions[0].instructions],
                         [i.opcode for i in prog.functions[0].instructions])

    def test_all_combo_ids_valid(self):
        self.assertEqual(NUM_COMBOS, 64)


if __name__ == "__main__":
    unittest.main()
