import unittest
from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.sema import SemanticAnalyzer
from src.minic.ir.ir_generator import IRGenerator
from src.minic.ir.tac import Opcode
from src.minic.ir.cfg import build_cfg_for_function


class TestIRGenerator(unittest.TestCase):
    def _compile_to_tac(self, code: str):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, code)
        ast = parser.parse()
        sema = SemanticAnalyzer(code)
        sema.analyze(ast)
        ir_gen = IRGenerator()
        tac_prog = ir_gen.generate(ast)
        return ast, tac_prog

    def test_simple_arithmetic_lowering(self):
        code = """
        int calc(int a, int b) {
            int c = a * 2 + b / 4;
            return c;
        }
        """
        _, tac_prog = self._compile_to_tac(code)
        self.assertEqual(len(tac_prog.functions), 1)
        func = tac_prog.functions[0]
        opcodes = [inst.opcode for inst in func.instructions]
        self.assertIn(Opcode.MUL, opcodes)
        self.assertIn(Opcode.DIV, opcodes)
        self.assertIn(Opcode.ADD, opcodes)
        self.assertIn(Opcode.RETURN, opcodes)

    def test_control_flow_and_cfg(self):
        code = """
        int loopTest(int n) {
            int total = 0;
            int i = 0;
            while (i < n) {
                total = total + i;
                i = i + 1;
            }
            return total;
        }
        """
        _, tac_prog = self._compile_to_tac(code)
        func = tac_prog.functions[0]
        cfg = build_cfg_for_function(func)
        self.assertGreaterEqual(len(cfg.blocks), 3)
        self.assertEqual(len(cfg.loops), 1)
        self.assertEqual(cfg.get_max_loop_depth(), 1)


if __name__ == "__main__":
    unittest.main()
