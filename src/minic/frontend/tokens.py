from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    # Keywords
    INT = auto()
    FLOAT = auto()
    CHAR = auto()
    STRUCT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()

    # Literals
    INT_LIT = auto()
    FLOAT_LIT = auto()
    CHAR_LIT = auto()
    STRING_LIT = auto()

    # Identifiers
    IDENT = auto()

    # Operators
    PLUS = auto()         # +
    MINUS = auto()        # -
    STAR = auto()         # *
    SLASH = auto()        # /
    PERCENT = auto()      # %
    ASSIGN = auto()       # =

    # Relational Operators
    EQ = auto()           # ==
    NE = auto()           # !=
    LT = auto()           # <
    LE = auto()           # <=
    GT = auto()           # >
    GE = auto()           # >=

    # Logical Operators
    AND = auto()          # &&
    OR = auto()           # ||
    NOT = auto()          # !

    # Punctuation & Delimiters
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    SEMICOLON = auto()    # ;
    COMMA = auto()        # ,
    DOT = auto()          # .

    # Special
    EOF = auto()


KEYWORDS = {
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "char": TokenType.CHAR,
    "struct": TokenType.STRUCT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "return": TokenType.RETURN,
}


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    col: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.col})"
