import unittest
from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.ast_nodes import (
    StructDecl, FuncDecl, VarDecl, WhileStmt, ForStmt, IfStmt,
    BinaryExpr, AssignExpr, ArrayAccessExpr, FieldAccessExpr, CallExpr
)
from src.minic.frontend.error_handler import ParserError


class TestParser(unittest.TestCase):
    def _parse(self, code: str):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, code)
        return parser.parse()

    def test_struct_declaration(self):
        code = """
        struct Point {
            int x;
            int y;
        };
        """
        ast = self._parse(code)
        self.assertEqual(len(ast.declarations), 1)
        self.assertIsInstance(ast.declarations[0], StructDecl)
        struct_decl = ast.declarations[0]
        self.assertEqual(struct_decl.name, "Point")
        self.assertEqual(len(struct_decl.fields), 2)
        self.assertEqual(struct_decl.fields[0].name, "x")
        self.assertEqual(struct_decl.fields[1].name, "y")

    def test_function_and_statements(self):
        code = """
        int compute(int arr[10], struct Point p) {
            int sum = 0;
            for (int i = 0; i < 10; i = i + 1) {
                sum = sum + arr[i];
            }
            if (sum > 100) {
                return sum + p.x;
            } else {
                return sum - p.y;
            }
        }
        """
        ast = self._parse(code)
        self.assertEqual(len(ast.declarations), 1)
        func_decl = ast.declarations[0]
        self.assertIsInstance(func_decl, FuncDecl)
        self.assertEqual(func_decl.name, "compute")
        self.assertEqual(len(func_decl.params), 2)
        self.assertEqual(func_decl.params[0].array_suffix.dim1, 10)
        self.assertTrue(func_decl.params[1].type_spec.is_struct)

        body = func_decl.body.statements
        self.assertIsInstance(body[0], VarDecl)
        self.assertIsInstance(body[1], ForStmt)
        self.assertIsInstance(body[2], IfStmt)

    def test_2d_array_and_member_access(self):
        code = """
        int getElem(int grid[3][3], struct Point pts[5]) {
            return grid[0][1] + pts[2].x;
        }
        """
        ast = self._parse(code)
        func_decl = ast.declarations[0]
        self.assertEqual(func_decl.params[0].array_suffix.dim2, 3)


if __name__ == "__main__":
    unittest.main()
