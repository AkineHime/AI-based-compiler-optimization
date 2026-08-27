"""Loop unrolling (pass 6) + pass-manager fixpoint iteration."""
import shutil
import tempfile
import unittest

from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.sema import SemanticAnalyzer
from src.minic.ir.ir_generator import IRGenerator
from src.minic.ir.tac import Opcode
from src.minic.optimizer import optimize_program, NUM_COMBOS
from src.minic.optimizer.loop_unroll import loop_unroll_pass
from src.minic.codegen import CEmitter
from src.minic.pipeline import compile_and_run


def tac(src):
    toks = Lexer(src).tokenize()
    ast = Parser(toks, src).parse()
    SemanticAnalyzer(src).analyze(ast)
    return IRGenerator().generate(ast)


class TestLoopUnroll(unittest.TestCase):
    def test_num_combos_is_64(self):
        self.assertEqual(NUM_COMBOS, 64)

    def test_unrolls_a_simple_counted_loop(self):
        src = ("int main(){int acc=0;int i=0;"
               "while(i<1000){acc=acc+i;i=i+1;}return acc % 200;}")
        f = tac(src).functions[0]
        out = loop_unroll_pass(f)
        labels = [str(i.dst) for i in out.instructions if i.opcode == Opcode.LABEL]
        self.assertTrue(any(n.startswith("L_unroll_") for n in labels))
        # the original loop is kept as the remainder
        self.assertTrue(any("while_start" in n or "for_start" in n for n in labels))

    def test_leaves_loops_with_control_flow_alone(self):
        src = ("int main(){int acc=0;int i=0;"
               "while(i<1000){ if(i>500){acc=acc+1;} i=i+1;}return acc;}")
        f = tac(src).functions[0]
        out = loop_unroll_pass(f)
        self.assertFalse(any(str(i.dst).startswith("L_unroll_")
                             for i in out.instructions if i.opcode == Opcode.LABEL))


@unittest.skipIf(shutil.which("gcc") is None, "gcc not on PATH")
class TestUnrollCorrectness(unittest.TestCase):
    PROGRAMS = {
        "counted_sum": ("int main(){int a=0;int i=0;"
                        "while(i<400000){a=a+i*3+7;i=i+1;}return ((a%251)+251)%251;}"),
        "two_ivs": ("int main(){int a=0;int i=0;int j=100;"
                    "while(i<300000){a=a+i-j;i=i+1;j=j+2;}return ((a%251)+251)%251;}"),
        "for_loop": ("int main(){int a=0;"
                     "for(int i=0;i<500000;i=i+1){a=a+i*i;}return ((a%251)+251)%251;}"),
        "odd_bound": ("int main(){int a=0;int i=0;"
                      "while(i<333333){a=a+i;i=i+1;}return ((a%251)+251)%251;}"),
        "step_3": ("int main(){int a=0;int i=0;"
                   "while(i<900000){a=a+i;i=i+3;}return ((a%251)+251)%251;}"),
    }

    def test_all_64_combos_match_baseline(self):
        for name, src in self.PROGRAMS.items():
            with self.subTest(program=name):
                t = tac(src)
                wd = tempfile.mkdtemp(prefix=f"minic_unroll_{name}_")
                try:
                    base = compile_and_run(CEmitter().emit(optimize_program(t, 0)), 0, workdir=wd)
                    self.assertTrue(base.compiled, base.compile_error)
                    bad = []
                    for combo in range(1, NUM_COMBOS):
                        r = compile_and_run(CEmitter().emit(optimize_program(t, combo)), combo, workdir=wd)
                        if not r.compiled:
                            bad.append(f"combo {combo}: compile error")
                        elif r.returncode != base.returncode:
                            bad.append(f"combo {combo}: {r.returncode} != {base.returncode}")
                    self.assertFalse(bad, f"[{name}] " + "; ".join(bad[:8]))
                finally:
                    shutil.rmtree(wd, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
