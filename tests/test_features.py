import unittest
from src.minic.frontend.lexer import Lexer
from src.minic.frontend.parser import Parser
from src.minic.frontend.sema import SemanticAnalyzer
from src.minic.ir.ir_generator import IRGenerator
from src.minic.features.extractor import FeatureExtractor, FEATURE_NAMES


class TestFeatureExtractor(unittest.TestCase):
    def test_feature_extraction(self):
        code = """
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

        int main() {
            int grid[3][3];
            grid[0][0] = 1;
            return matrixSum(grid);
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, code)
        ast = parser.parse()
        sema = SemanticAnalyzer(code)
        sema.analyze(ast)

        ir_gen = IRGenerator()
        tac = ir_gen.generate(ast)

        extractor = FeatureExtractor()
        features = extractor.extract(ast, tac)

        self.assertEqual(len(features), 18)
        for name in FEATURE_NAMES:
            self.assertIn(name, features)

        # Check loop depth in matrixSum (nested while loop)
        self.assertGreaterEqual(features["max_loop_depth"], 2.0)
        self.assertGreaterEqual(features["loop_count"], 2.0)
        self.assertGreater(features["array_2d_access_count"], 0)


if __name__ == "__main__":
    unittest.main()
