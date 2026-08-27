from typing import List, Optional, Any
from .tokens import Token, TokenType, KEYWORDS
from .error_handler import LexerError


class Lexer:
    """MiniC Lexical Analyzer."""

    def __init__(self, source: str):
        self.source: str = source
        self.length: int = len(source)
        self.pos: int = 0
        self.line: int = 1
        self.col: int = 1

    def tokenize(self) -> List[Token]:
        """Convert the entire source string into a list of Tokens."""
        tokens: List[Token] = []
        while self.pos < self.length:
            ch = self.source[self.pos]

            # Whitespace
            if ch == '\n':
                self.line += 1
                self.col = 1
                self.pos += 1
                continue
            if ch in ' \t\r\f\v':
                self._advance()
                continue

            # Comments or Slash
            if ch == '/':
                if self._peek(1) == '/':
                    # Single-line comment
                    self._skip_line_comment()
                    continue
                elif self._peek(1) == '*':
                    # Multi-line comment
                    self._skip_block_comment()
                    continue
                else:
                    tokens.append(self._make_token(TokenType.SLASH, "/"))
                    self._advance()
                    continue

            # String literals
            if ch == '"':
                tokens.append(self._read_string())
                continue

            # Character literals
            if ch == "'":
                tokens.append(self._read_char())
                continue

            # Numbers (integers or floats)
            if ch.isdigit() or (ch == '.' and self._peek(1).isdigit()):
                tokens.append(self._read_number())
                continue

            # Identifiers and keywords
            if ch.isalpha() or ch == '_':
                tokens.append(self._read_identifier_or_keyword())
                continue

            # Multi-character operators
            start_line, start_col = self.line, self.col
            if ch == '=':
                if self._peek(1) == '=':
                    self._advance(2)
                    tokens.append(Token(TokenType.EQ, "==", start_line, start_col))
                    continue
                self._advance()
                tokens.append(Token(TokenType.ASSIGN, "=", start_line, start_col))
                continue

            if ch == '!':
                if self._peek(1) == '=':
                    self._advance(2)
                    tokens.append(Token(TokenType.NE, "!=", start_line, start_col))
                    continue
                self._advance()
                tokens.append(Token(TokenType.NOT, "!", start_line, start_col))
                continue

            if ch == '<':
                if self._peek(1) == '=':
                    self._advance(2)
                    tokens.append(Token(TokenType.LE, "<=", start_line, start_col))
                    continue
                self._advance()
                tokens.append(Token(TokenType.LT, "<", start_line, start_col))
                continue

            if ch == '>':
                if self._peek(1) == '=':
                    self._advance(2)
                    tokens.append(Token(TokenType.GE, ">=", start_line, start_col))
                    continue
                self._advance()
                tokens.append(Token(TokenType.GT, ">", start_line, start_col))
                continue

            if ch == '&' and self._peek(1) == '&':
                self._advance(2)
                tokens.append(Token(TokenType.AND, "&&", start_line, start_col))
                continue

            if ch == '|' and self._peek(1) == '|':
                self._advance(2)
                tokens.append(Token(TokenType.OR, "||", start_line, start_col))
                continue

            # Single-character tokens
            single_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.STAR,
                '%': TokenType.PERCENT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
            }

            if ch in single_tokens:
                tokens.append(self._make_token(single_tokens[ch], ch))
                self._advance()
                continue

            raise LexerError(f"Unexpected character {ch!r}", self.line, self.col, self.source)

        tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return tokens

    def _advance(self, count: int = 1) -> None:
        for _ in range(count):
            if self.pos < self.length:
                if self.source[self.pos] == '\n':
                    self.line += 1
                    self.col = 1
                else:
                    self.col += 1
                self.pos += 1

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx < self.length:
            return self.source[idx]
        return ""

    def _make_token(self, token_type: TokenType, value: Any) -> Token:
        return Token(token_type, value, self.line, self.col)

    def _skip_line_comment(self) -> None:
        self._advance(2)  # skip '//'
        while self.pos < self.length and self.source[self.pos] != '\n':
            self._advance()

    def _skip_block_comment(self) -> None:
        start_line, start_col = self.line, self.col
        self._advance(2)  # skip '/*'
        while self.pos < self.length:
            if self.source[self.pos] == '*' and self._peek(1) == '/':
                self._advance(2)
                return
            self._advance()
        raise LexerError("Unterminated block comment", start_line, start_col, self.source)

    def _read_identifier_or_keyword(self) -> Token:
        start_line, start_col = self.line, self.col
        start_pos = self.pos
        while self.pos < self.length and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self._advance()
        ident_text = self.source[start_pos:self.pos]
        token_type = KEYWORDS.get(ident_text, TokenType.IDENT)
        return Token(token_type, ident_text, start_line, start_col)

    def _read_number(self) -> Token:
        start_line, start_col = self.line, self.col
        start_pos = self.pos
        is_float = False

        while self.pos < self.length and self.source[self.pos].isdigit():
            self._advance()

        if self.pos < self.length and self.source[self.pos] == '.' and self._peek(1).isdigit():
            is_float = True
            self._advance()  # consume '.'
            while self.pos < self.length and self.source[self.pos].isdigit():
                self._advance()

        num_str = self.source[start_pos:self.pos]
        if is_float:
            return Token(TokenType.FLOAT_LIT, float(num_str), start_line, start_col)
        else:
            return Token(TokenType.INT_LIT, int(num_str), start_line, start_col)

    def _read_string(self) -> Token:
        start_line, start_col = self.line, self.col
        self._advance()  # skip opening '"'
        chars = []

        while self.pos < self.length and self.source[self.pos] != '"':
            ch = self.source[self.pos]
            if ch == '\n':
                raise LexerError("Unterminated string literal (newline in string)", start_line, start_col, self.source)
            if ch == '\\':
                self._advance()
                if self.pos >= self.length:
                    raise LexerError("Unterminated escape sequence in string literal", start_line, start_col, self.source)
                escape_ch = self.source[self.pos]
                escapes = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', '0': '\0'}
                if escape_ch in escapes:
                    chars.append(escapes[escape_ch])
                else:
                    chars.append(escape_ch)
            else:
                chars.append(ch)
            self._advance()

        if self.pos >= self.length or self.source[self.pos] != '"':
            raise LexerError("Unterminated string literal", start_line, start_col, self.source)
        self._advance()  # skip closing '"'
        return Token(TokenType.STRING_LIT, "".join(chars), start_line, start_col)

    def _read_char(self) -> Token:
        start_line, start_col = self.line, self.col
        self._advance()  # skip opening "'"
        if self.pos >= self.length:
            raise LexerError("Unterminated character literal", start_line, start_col, self.source)

        ch = self.source[self.pos]
        if ch == '\\':
            self._advance()
            if self.pos >= self.length:
                raise LexerError("Unterminated escape in character literal", start_line, start_col, self.source)
            escape_ch = self.source[self.pos]
            escapes = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', "'": "'", '0': '\0'}
            ch = escapes.get(escape_ch, escape_ch)
            self._advance()
        else:
            self._advance()

        if self.pos >= self.length or self.source[self.pos] != "'":
            raise LexerError("Unterminated or multi-character char literal", start_line, start_col, self.source)
        self._advance()  # skip closing "'"
        return Token(TokenType.CHAR_LIT, ch, start_line, start_col)
