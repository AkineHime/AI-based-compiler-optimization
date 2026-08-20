import unittest
from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.sema import SemanticAnalyzer
from src.minic.frontend.error_handler import SemanticError


class TestSemanticAnalyzer(unittest.TestCase):
    def _check(self, code: str):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, code)
        ast = parser.parse()
        analyzer = SemanticAnalyzer(code)
        analyzer.analyze(ast)
        return analyzer

    def test_valid_program(self):
        code = """
        struct Point {
            int x;
            int y;
        };

        int add(struct Point p) {
            return p.x + p.y;
        }

        int main() {
            struct Point p;
            p.x = 10;
            p.y = 20;
            return add(p);
        }
        """
        analyzer = self._check(code)
        self.assertIn("Point", analyzer.structs)
        self.assertIn("add", analyzer.functions)

    def test_recursive_struct_rejection(self):
        code = """
        struct Node {
            int val;
            struct Node next;
        };
        """
        with self.assertRaises(SemanticError):
            self._check(code)

    def test_invalid_lvalue_rejection(self):
        code = """
        int f() { return 1; }
        int main() {
            f() = 10;
            return 0;
        }
        """
        with self.assertRaises(SemanticError):
            self._check(code)

    def test_type_mismatch_rejection(self):
        code = """
        struct A { int x; };
        struct B { int x; };
        int main() {
            struct A a;
            struct B b;
            a = b; // Nominal type mismatch!
            return 0;
        }
        """
        with self.assertRaises(SemanticError):
            self._check(code)

    def test_array_bounds_and_subscript_checking(self):
        code = """
        int main() {
            int arr[10];
            int x = arr[0];
            return x;
        }
        """
        analyzer = self._check(code)
        self.assertIsNotNone(analyzer)


if __name__ == "__main__":
    unittest.main()
