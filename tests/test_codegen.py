"""Unit tests for TAC -> C code generation (Person B)."""
import shutil
import unittest

from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.sema import SemanticAnalyzer
from src.minic.ir.ir_generator import IRGenerator
from src.minic.codegen import emit_c
from src.minic.codegen.c_emitter import parse_type, wrapper_name
from src.minic.pipeline import source_to_c, compile_and_run


def to_c(src: str, combo: int = 0) -> str:
    toks = Lexer(src).tokenize()
    ast = Parser(toks, src).parse()
    SemanticAnalyzer(src).analyze(ast)
    return emit_c(IRGenerator().generate(ast)) if combo == 0 else source_to_c(src, combo)


class TestWrapperNaming(unittest.TestCase):
    def test_type_parsing(self):
        self.assertEqual(wrapper_name(parse_type("int[3][3]")), "arr_int_3_3")
        self.assertEqual(wrapper_name(parse_type("char[6]")), "str_6")
        self.assertEqual(wrapper_name(parse_type("float[8]")), "arr_float_8")
        self.assertFalse(parse_type("int").is_array)
        self.assertEqual(parse_type("struct Point").c_base, "Point")


class TestEmittedSource(unittest.TestCase):
    def test_arrays_and_strings_are_wrapped(self):
        src = ('int sum(int m[2][2]) { return m[0][0] + m[1][1]; }\n'
               'int main() {\n'
               '  char s[4] = "ab";\n'
               '  int g[2][2];\n'
               '  g[0][0] = 40; g[1][1] = 2; g[0][1] = 0; g[1][0] = 0;\n'
               '  return sum(g);\n'
               '}\n')
        c = to_c(src)
        self.assertIn("typedef struct { int data[2][2]; } arr_int_2_2;", c)
        self.assertIn("typedef struct { char data[4]; } str_4;", c)
        self.assertIn("int sum(arr_int_2_2 m)", c)          # struct-by-value param
        self.assertIn(".data = \"ab\"", c)                   # C99 compound literal
        self.assertIn("m.data[", c)                          # wrapped access

    def test_minic_struct_maps_to_named_c_struct(self):
        src = ('struct P { int x; int y; };\n'
               'int main() { struct P p; p.x = 41; p.y = 1; return p.x + p.y; }\n')
        c = to_c(src)
        self.assertIn("} P;", c)
        self.assertIn("p.x = 41;", c)


@unittest.skipIf(shutil.which("gcc") is None, "gcc not on PATH")
class TestCompilesAndRuns(unittest.TestCase):
    def test_value_semantics_preserved_through_call(self):
        # If the array param decayed to a pointer, the callee's writes would
        # leak back and change the result.
        src = ('int bump(int a[3]) { a[0] = a[0] + 100; return a[0]; }\n'
               'int main() {\n'
               '  int v[3]; v[0] = 7; v[1] = 0; v[2] = 0;\n'
               '  int inside = bump(v);\n'
               '  return inside - v[0];\n'   # 107 - 7 = 100 iff value semantics hold
               '}\n')
        res = compile_and_run(to_c(src), 0)
        self.assertTrue(res.compiled, res.compile_error)
        self.assertEqual(res.returncode, 100)


if __name__ == "__main__":
    unittest.main()
