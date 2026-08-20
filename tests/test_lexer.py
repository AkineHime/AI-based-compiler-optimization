import unittest
from src.minic.frontend.lexer import Lexer
from src.minic.frontend.tokens import TokenType
from src.minic.frontend.error_handler import LexerError


class TestLexer(unittest.TestCase):
    def test_keywords_and_identifiers(self):
        source = "int float char struct if else while for return myVar_123"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.STRUCT,
            TokenType.IF, TokenType.ELSE, TokenType.WHILE, TokenType.FOR,
            TokenType.RETURN, TokenType.IDENT, TokenType.EOF
        ]
        self.assertEqual([t.type for t in tokens], expected_types)
        self.assertEqual(tokens[9].value, "myVar_123")

    def test_literals(self):
        source = '42 3.1415 \'x\' "\\nhello\\tworld"'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.INT_LIT)
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].type, TokenType.FLOAT_LIT)
        self.assertAlmostEqual(tokens[1].value, 3.1415)
        self.assertEqual(tokens[2].type, TokenType.CHAR_LIT)
        self.assertEqual(tokens[2].value, 'x')
        self.assertEqual(tokens[3].type, TokenType.STRING_LIT)
        self.assertEqual(tokens[3].value, "\nhello\tworld")

    def test_operators(self):
        source = "+ - * / % == != < <= > >= && || ! = . ; , ( ) [ ] { }"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected = [
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT,
            TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE,
            TokenType.AND, TokenType.OR, TokenType.NOT, TokenType.ASSIGN, TokenType.DOT,
            TokenType.SEMICOLON, TokenType.COMMA, TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACKET, TokenType.RBRACKET, TokenType.LBRACE, TokenType.RBRACE,
            TokenType.EOF
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_comments(self):
        source = """
        // This is a single line comment
        int a = 5; /* This is a
        multi-line comment */ float b = 2.0;
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertEqual(types, [
            TokenType.INT, TokenType.IDENT, TokenType.ASSIGN, TokenType.INT_LIT, TokenType.SEMICOLON,
            TokenType.FLOAT, TokenType.IDENT, TokenType.ASSIGN, TokenType.FLOAT_LIT, TokenType.SEMICOLON,
            TokenType.EOF
        ])

    def test_invalid_character(self):
        lexer = Lexer("int a = @;")
        with self.assertRaises(LexerError):
            lexer.tokenize()


if __name__ == "__main__":
    unittest.main()
