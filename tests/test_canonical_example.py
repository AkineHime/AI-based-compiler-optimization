import unittest
from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.sema import SemanticAnalyzer
from src.minic.ir.ir_generator import IRGenerator
from src.minic.ir.ir_printer import IRPrinter
from src.minic.features.extractor import FeatureExtractor


CANONICAL_PROGRAM = """
struct Point {
    int x;
    int y;
};

int matrixSum(int m[3][3]) {
    int total = 0;
    int i = 0;
    while (i < 3) {
        int j = 0;
        while (j < 3) {
            total = total + m[i][j];
            j = j + 1;
        }
        i = i + 1;
    }
    return total;
}

int distanceSquared(struct Point a, struct Point b) {
    int dx = a.x - b.x;
    int dy = a.y - b.y;
    return dx * dx + dy * dy;
}

int fib(int n) {
    if (n < 2) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

int main() {
    char label[6] = "grid1";
    struct Point p1;
    p1.x = 0;
    p1.y = 0;
    struct Point p2;
    p2.x = 3;
    p2.y = 4;
    int grid[3][3];
    grid[0][0] = 1; grid[0][1] = 0; grid[0][2] = 0;
    grid[1][0] = 0; grid[1][1] = 1; grid[1][2] = 0;
    grid[2][0] = 0; grid[2][1] = 0; grid[2][2] = 1;
    int d = distanceSquared(p1, p2);
    int s = matrixSum(grid);
    int f = fib(10);
    return d + s + f;
}
"""


class TestCanonicalExample(unittest.TestCase):
    def test_canonical_pipeline(self):
        # 1. Lex
        lexer = Lexer(CANONICAL_PROGRAM)
        tokens = lexer.tokenize()
        self.assertGreater(len(tokens), 0)

        # 2. Parse
        parser = Parser(tokens, CANONICAL_PROGRAM)
        ast = parser.parse()
        self.assertEqual(len(ast.declarations), 5)  # struct Point, matrixSum, distanceSquared, fib, main

        # 3. Semantic Analysis
        sema = SemanticAnalyzer(CANONICAL_PROGRAM)
        sema.analyze(ast)
        self.assertIn("Point", sema.structs)
        self.assertIn("matrixSum", sema.functions)
        self.assertIn("distanceSquared", sema.functions)
        self.assertIn("fib", sema.functions)
        self.assertIn("main", sema.functions)

        # 4. IR Generation
        ir_gen = IRGenerator()
        tac_prog = ir_gen.generate(ast)
        self.assertEqual(len(tac_prog.functions), 4)

        # Format TAC and check it is non-empty
        formatted_tac = IRPrinter.format_program(tac_prog)
        self.assertIn("func main", formatted_tac)
        self.assertIn("func fib", formatted_tac)
        self.assertIn("func matrixSum", formatted_tac)
        self.assertIn("func distanceSquared", formatted_tac)

        # 5. Feature Extraction
        extractor = FeatureExtractor()
        features = extractor.extract(ast, tac_prog)

        self.assertEqual(features["recursive_call_count"], 2.0)  # fib(n-1) + fib(n-2)
        self.assertEqual(features["max_loop_depth"], 2.0)        # nested loop in matrixSum
        self.assertGreaterEqual(features["struct_access_count"], 4.0)
        self.assertGreaterEqual(features["array_2d_access_count"], 9.0)


if __name__ == "__main__":
    unittest.main()
