from typing import List, Optional
from .tokens import Token, TokenType
from .ast_nodes import (
    ASTNode, TypeSpec, ArraySuffix, FieldDecl, StructDecl, VarDecl,
    Param, FuncDecl, Block, ExprStmt, IfStmt, WhileStmt, ForStmt,
    ReturnStmt, Literal, VarExpr, ArrayAccessExpr, FieldAccessExpr,
    CallExpr, UnaryExpr, BinaryExpr, AssignExpr, Program
)
from .error_handler import ParserError


class Parser:
    """MiniC Recursive-Descent Parser."""

    def __init__(self, tokens: List[Token], source: str = ""):
        self.tokens: List[Token] = tokens
        self.source: str = source
        self.pos: int = 0

    def parse(self) -> Program:
        """Parse the token list into a complete Program AST."""
        declarations: List[ASTNode] = []
        while not self._is_at_end():
            decl = self._parse_top_level_declaration()
            declarations.append(decl)
        return Program(declarations=declarations)

    # --- Top-Level Declarations ---

    def _parse_top_level_declaration(self) -> ASTNode:
        # Check for struct definition: 'struct' IDENT '{'
        if self._check(TokenType.STRUCT) and self._peek(1).type == TokenType.IDENT and self._peek(2).type == TokenType.LBRACE:
            return self._parse_struct_decl()

        # Otherwise it starts with a type_spec, followed by IDENT
        type_spec = self._parse_type_spec()
        ident_tok = self._consume(TokenType.IDENT, "Expected identifier after type specification")

        # Distinguish between function declaration and global variable declaration
        if self._check(TokenType.LPAREN):
            return self._parse_func_decl_rest(type_spec, ident_tok)
        else:
            return self._parse_var_decl_rest(type_spec, ident_tok)

    def _parse_struct_decl(self) -> StructDecl:
        struct_tok = self._consume(TokenType.STRUCT, "Expected 'struct'")
        name_tok = self._consume(TokenType.IDENT, "Expected struct name")
        self._consume(TokenType.LBRACE, "Expected '{' in struct declaration")

        fields: List[FieldDecl] = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            fields.append(self._parse_field_decl())

        if not fields:
            raise ParserError("Struct declaration must have at least one field", struct_tok.line, struct_tok.col, self.source)

        self._consume(TokenType.RBRACE, "Expected '}' after struct body")
        self._consume(TokenType.SEMICOLON, "Expected ';' after struct declaration")
        return StructDecl(name=name_tok.value, fields=fields, line=struct_tok.line, col=struct_tok.col)

    def _parse_field_decl(self) -> FieldDecl:
        type_spec = self._parse_type_spec()
        ident_tok = self._consume(TokenType.IDENT, "Expected field name")
        suffix = self._parse_array_suffix_opt()
        self._consume(TokenType.SEMICOLON, "Expected ';' after field declaration")
        return FieldDecl(type_spec=type_spec, name=ident_tok.value, array_suffix=suffix, line=ident_tok.line, col=ident_tok.col)

    def _parse_func_decl_rest(self, return_type: TypeSpec, ident_tok: Token) -> FuncDecl:
        self._consume(TokenType.LPAREN, "Expected '(' in function declaration")
        params: List[Param] = []

        if not self._check(TokenType.RPAREN):
            params.append(self._parse_param())
            while self._match(TokenType.COMMA):
                params.append(self._parse_param())

        self._consume(TokenType.RPAREN, "Expected ')' after parameter list")
        body = self._parse_block()
        return FuncDecl(return_type=return_type, name=ident_tok.value, params=params, body=body, line=ident_tok.line, col=ident_tok.col)

    def _parse_param(self) -> Param:
        type_spec = self._parse_type_spec()
        ident_tok = self._consume(TokenType.IDENT, "Expected parameter name")
        suffix = self._parse_array_suffix_opt()
        return Param(type_spec=type_spec, name=ident_tok.value, array_suffix=suffix, line=ident_tok.line, col=ident_tok.col)

    def _parse_var_decl_rest(self, type_spec: TypeSpec, ident_tok: Token, require_semicolon: bool = True) -> VarDecl:
        suffix = self._parse_array_suffix_opt()
        init_expr = None
        if self._match(TokenType.ASSIGN):
            init_expr = self._parse_expr()

        if require_semicolon:
            self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")

        return VarDecl(type_spec=type_spec, name=ident_tok.value, array_suffix=suffix, init_expr=init_expr, line=ident_tok.line, col=ident_tok.col)

    # --- Types & Suffixes ---

    def _parse_type_spec(self) -> TypeSpec:
        tok = self._peek()
        if self._match(TokenType.INT):
            return TypeSpec(name="int", is_struct=False, line=tok.line, col=tok.col)
        elif self._match(TokenType.FLOAT):
            return TypeSpec(name="float", is_struct=False, line=tok.line, col=tok.col)
        elif self._match(TokenType.CHAR):
            return TypeSpec(name="char", is_struct=False, line=tok.line, col=tok.col)
        elif self._match(TokenType.STRUCT):
            ident_tok = self._consume(TokenType.IDENT, "Expected struct name after 'struct'")
            return TypeSpec(name=ident_tok.value, is_struct=True, line=tok.line, col=tok.col)
        elif self._match(TokenType.IDENT):
            return TypeSpec(name=tok.value, is_struct=True, line=tok.line, col=tok.col)
        else:
            raise ParserError(f"Expected type specifier, got {tok.value!r}", tok.line, tok.col, self.source)

    def _parse_array_suffix_opt(self) -> Optional[ArraySuffix]:
        if not self._match(TokenType.LBRACKET):
            return None

        line, col = self._previous().line, self._previous().col
        dim1_tok = self._consume(TokenType.INT_LIT, "Expected integer constant for array dimension")
        dim1 = int(dim1_tok.value)
        self._consume(TokenType.RBRACKET, "Expected ']' after array dimension")

        dim2 = None
        if self._match(TokenType.LBRACKET):
            dim2_tok = self._consume(TokenType.INT_LIT, "Expected integer constant for 2D array dimension")
            dim2 = int(dim2_tok.value)
            self._consume(TokenType.RBRACKET, "Expected ']' after 2D array dimension")

        return ArraySuffix(dim1=dim1, dim2=dim2, line=line, col=col)

    # --- Statements ---

    def _parse_block(self) -> Block:
        lbrace = self._consume(TokenType.LBRACE, "Expected '{' to start block")
        stmts: List[ASTNode] = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            stmts.append(self._parse_stmt())
        self._consume(TokenType.RBRACE, "Expected '}' to close block")
        return Block(statements=stmts, line=lbrace.line, col=lbrace.col)

    def _parse_stmt(self) -> ASTNode:
        if self._check(TokenType.LBRACE):
            return self._parse_block()
        if self._match(TokenType.IF):
            return self._parse_if_stmt()
        if self._match(TokenType.WHILE):
            return self._parse_while_stmt()
        if self._match(TokenType.FOR):
            return self._parse_for_stmt()
        if self._match(TokenType.RETURN):
            return self._parse_return_stmt()

        # Check if statement is a variable declaration
        if self._is_type_spec_start():
            type_spec = self._parse_type_spec()
            ident_tok = self._consume(TokenType.IDENT, "Expected identifier in variable declaration")
            return self._parse_var_decl_rest(type_spec, ident_tok)

        # Otherwise it's an expression statement
        expr = self._parse_expr()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return ExprStmt(expr=expr, line=expr.line, col=expr.col)

    def _is_type_spec_start(self) -> bool:
        if self._check(TokenType.INT) or self._check(TokenType.FLOAT) or self._check(TokenType.CHAR):
            return True
        if self._check(TokenType.STRUCT):
            return True
        # If IDENT followed by IDENT, it's a struct type like `Point p;`
        if self._check(TokenType.IDENT) and self._peek(1).type == TokenType.IDENT:
            return True
        return False

    def _parse_if_stmt(self) -> IfStmt:
        if_tok = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'if'")
        cond = self._parse_expr()
        self._consume(TokenType.RPAREN, "Expected ')' after if condition")
        then_branch = self._parse_stmt()
        else_branch = None
        if self._match(TokenType.ELSE):
            else_branch = self._parse_stmt()
        return IfStmt(cond=cond, then_branch=then_branch, else_branch=else_branch, line=if_tok.line, col=if_tok.col)

    def _parse_while_stmt(self) -> WhileStmt:
        while_tok = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'while'")
        cond = self._parse_expr()
        self._consume(TokenType.RPAREN, "Expected ')' after while condition")
        body = self._parse_stmt()
        return WhileStmt(cond=cond, body=body, line=while_tok.line, col=while_tok.col)

    def _parse_for_stmt(self) -> ForStmt:
        for_tok = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'for'")

        # Init
        init: Optional[ASTNode] = None
        if not self._check(TokenType.SEMICOLON):
            if self._is_type_spec_start():
                type_spec = self._parse_type_spec()
                ident_tok = self._consume(TokenType.IDENT, "Expected identifier in for-loop initializer")
                init = self._parse_var_decl_rest(type_spec, ident_tok, require_semicolon=False)
            else:
                init = self._parse_expr()
        self._consume(TokenType.SEMICOLON, "Expected ';' after for-loop initializer")

        # Condition
        cond: Optional[ASTNode] = None
        if not self._check(TokenType.SEMICOLON):
            cond = self._parse_expr()
        self._consume(TokenType.SEMICOLON, "Expected ';' after for-loop condition")

        # Step
        step: Optional[ASTNode] = None
        if not self._check(TokenType.RPAREN):
            step = self._parse_expr()
        self._consume(TokenType.RPAREN, "Expected ')' after for-loop step")

        body = self._parse_stmt()
        return ForStmt(init=init, cond=cond, step=step, body=body, line=for_tok.line, col=for_tok.col)

    def _parse_return_stmt(self) -> ReturnStmt:
        ret_tok = self._previous()
        expr = None
        if not self._check(TokenType.SEMICOLON):
            expr = self._parse_expr()
        self._consume(TokenType.SEMICOLON, "Expected ';' after return statement")
        return ReturnStmt(expr=expr, line=ret_tok.line, col=ret_tok.col)

    # --- Expressions (Precedence Climbing) ---

    def _parse_expr(self) -> ASTNode:
        return self._parse_assignment()

    def _parse_assignment(self) -> ASTNode:
        expr = self._parse_logic_or()
        if self._match(TokenType.ASSIGN):
            assign_tok = self._previous()
            value = self._parse_assignment()
            return AssignExpr(target=expr, value=value, line=assign_tok.line, col=assign_tok.col)
        return expr

    def _parse_logic_or(self) -> ASTNode:
        expr = self._parse_logic_and()
        while self._match(TokenType.OR):
            op_tok = self._previous()
            right = self._parse_logic_and()
            expr = BinaryExpr(op="||", left=expr, right=right, line=op_tok.line, col=op_tok.col)
        return expr

    def _parse_logic_and(self) -> ASTNode:
        expr = self._parse_equality()
        while self._match(TokenType.AND):
            op_tok = self._previous()
            right = self._parse_equality()
            expr = BinaryExpr(op="&&", left=expr, right=right, line=op_tok.line, col=op_tok.col)
        return expr

    def _parse_equality(self) -> ASTNode:
        expr = self._parse_relational()
        while self._check(TokenType.EQ) or self._check(TokenType.NE):
            self._advance()
            op_tok = self._previous()
            right = self._parse_relational()
            expr = BinaryExpr(op=op_tok.value, left=expr, right=right, line=op_tok.line, col=op_tok.col)
        return expr

    def _parse_relational(self) -> ASTNode:
        expr = self._parse_additive()
        while self._check(TokenType.LT) or self._check(TokenType.LE) or self._check(TokenType.GT) or self._check(TokenType.GE):
            self._advance()
            op_tok = self._previous()
            right = self._parse_additive()
            expr = BinaryExpr(op=op_tok.value, left=expr, right=right, line=op_tok.line, col=op_tok.col)
        return expr

    def _parse_additive(self) -> ASTNode:
        expr = self._parse_multiplicative()
        while self._check(TokenType.PLUS) or self._check(TokenType.MINUS):
            self._advance()
            op_tok = self._previous()
            right = self._parse_multiplicative()
            expr = BinaryExpr(op=op_tok.value, left=expr, right=right, line=op_tok.line, col=op_tok.col)
        return expr

    def _parse_multiplicative(self) -> ASTNode:
        expr = self._parse_unary()
        while self._check(TokenType.STAR) or self._check(TokenType.SLASH) or self._check(TokenType.PERCENT):
            self._advance()
            op_tok = self._previous()
            right = self._parse_unary()
            expr = BinaryExpr(op=op_tok.value, left=expr, right=right, line=op_tok.line, col=op_tok.col)
        return expr

    def _parse_unary(self) -> ASTNode:
        if self._check(TokenType.MINUS) or self._check(TokenType.NOT):
            self._advance()
            op_tok = self._previous()
            operand = self._parse_unary()
            return UnaryExpr(op=op_tok.value, operand=operand, line=op_tok.line, col=op_tok.col)
        return self._parse_postfix()

    def _parse_postfix(self) -> ASTNode:
        expr = self._parse_primary()

        while True:
            if self._match(TokenType.LBRACKET):
                idx = self._parse_expr()
                self._consume(TokenType.RBRACKET, "Expected ']' after array index")
                indices = [idx]
                if self._match(TokenType.LBRACKET):
                    idx2 = self._parse_expr()
                    self._consume(TokenType.RBRACKET, "Expected ']' after 2D array index")
                    indices.append(idx2)
                expr = ArrayAccessExpr(target=expr, indices=indices, line=expr.line, col=expr.col)
            elif self._match(TokenType.DOT):
                field_tok = self._consume(TokenType.IDENT, "Expected struct field name after '.'")
                expr = FieldAccessExpr(target=expr, field=field_tok.value, line=expr.line, col=expr.col)
            elif self._match(TokenType.LPAREN):
                # Function call
                args: List[ASTNode] = []
                if not self._check(TokenType.RPAREN):
                    args.append(self._parse_expr())
                    while self._match(TokenType.COMMA):
                        args.append(self._parse_expr())
                self._consume(TokenType.RPAREN, "Expected ')' after function arguments")
                if not isinstance(expr, VarExpr):
                    raise ParserError("Can only call named functions", expr.line, expr.col, self.source)
                expr = CallExpr(func_name=expr.name, args=args, line=expr.line, col=expr.col)
            else:
                break

        return expr

    def _parse_primary(self) -> ASTNode:
        tok = self._peek()

        if self._match(TokenType.INT_LIT):
            return Literal(value=int(tok.value), lit_type="int", line=tok.line, col=tok.col)
        if self._match(TokenType.FLOAT_LIT):
            return Literal(value=float(tok.value), lit_type="float", line=tok.line, col=tok.col)
        if self._match(TokenType.CHAR_LIT):
            return Literal(value=str(tok.value), lit_type="char", line=tok.line, col=tok.col)
        if self._match(TokenType.STRING_LIT):
            return Literal(value=str(tok.value), lit_type="string", line=tok.line, col=tok.col)
        if self._match(TokenType.IDENT):
            return VarExpr(name=tok.value, line=tok.line, col=tok.col)
        if self._match(TokenType.LPAREN):
            expr = self._parse_expr()
            self._consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        raise ParserError(f"Expected expression, got {tok.value!r}", tok.line, tok.col, self.source)

    # --- Helper Utilities ---

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]  # Return EOF token

    def _previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _match(self, *token_types: TokenType) -> bool:
        for t in token_types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, err_msg: str) -> Token:
        if self._check(token_type):
            return self._advance()
        tok = self._peek()
        raise ParserError(f"{err_msg} (got {tok.value!r})", tok.line, tok.col, self.source)

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.pos += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF
