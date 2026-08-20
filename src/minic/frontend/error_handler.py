class MiniCError(Exception):
    """Base exception for all MiniC compiler errors."""

    def __init__(self, message: str, line: int = 0, col: int = 0, source: str = ""):
        self.message = message
        self.line = line
        self.col = col
        self.source = source
        super().__init__(self._format_error())

    def _format_error(self) -> str:
        loc = f"Line {self.line}, Column {self.col}" if self.line > 0 else "Error"
        header = f"[{self.__class__.__name__}] {loc}: {self.message}"
        if self.source and self.line > 0:
            lines = self.source.splitlines()
            if 0 < self.line <= len(lines):
                src_line = lines[self.line - 1]
                caret_col = max(1, self.col) - 1
                pointer = " " * caret_col + "^"
                return f"{header}\n  {src_line}\n  {pointer}"
        return header


class LexerError(MiniCError):
    """Raised when tokenization fails."""
    pass


class ParserError(MiniCError):
    """Raised when syntax parsing fails."""
    pass


class SemanticError(MiniCError):
    """Raised when semantic analysis / type checking fails."""
    pass
