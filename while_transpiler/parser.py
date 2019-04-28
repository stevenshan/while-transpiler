__all__ = ["parse"]

"""
Code to convert stream of Tokens first into a parse tree and then into an
abstract syntax tree (AST)
"""

from .tokens import Tokens
from .stack import Stack
from .nonterminals import Nonterminals
from .ast import AST, ASTTokenMap

class ParseError(Exception):
    pass

class ParseResult:
    def __init__(self):
        self.parser = None
        self.variable_names = set()
        self.constants = set()

    @property
    def parse_tree(self):
        return self.parser.nodes.peek()

    @property
    def ast(self):
        return parse_tree_to_ast(self.parse_tree)

def parse(token_stream):
    """
    Parses token stream generated by lexer. Note that since it is a stream,
    tokens are found lazily so if it is read from a file descriptor, the file
    descriptor must be left open when `parse` is called.
    """

    result = ParseResult()

    def token_interceptor():
        """
        Middleware to look at each token before it is parsed. Used to get
        list of variable names and constants. Returns generator.
        """

        try:
            while True:
                token_raw = next(token_stream)
                _, token = token_raw

                if token == Tokens._Variable:
                    result.variable_names.add(token.value)
                elif token == Tokens._Number:
                    result.constants.add(token.value)

                yield token_raw
        except StopIteration:
            return

    parser = Parser(token_interceptor())
    parser.statement()
    if not parser.done:
        raise ParseError

    result.parser = parser

    return result

class Parser:
    """
    Generates parse tree for stream of tokens.
    """

    def __init__(self, token_stream):
        self.token = None
        self.token_stream = token_stream
        self.nextsym()
        self.line_num = 1

        self.nodes = Stack()
        self.nodes.push(Nonterminals.Program())

    @property
    def done(self):
        return self.token is None

    def nextsym(self):
        try:
            self.line_num, self.token = next(self.token_stream)
        except StopIteration:
            self.token = None

    def accept(self, token):
        if self.token is None:
            return False
        if self.token == token:
            self.nodes.peek().components.append(self.token)
            self.nextsym()
            return True
        return False

    def raise_error(self):
        raise ParseError(self.line_num)

    def expect(self, token):
        if self.accept(token):
            return True
        self.raise_error()

    def check_parse_error(node_cls):
        def _decorator(func):
            def _check(self, raise_error=True, propagate=True):
                self.nodes.push(node_cls())
                try:
                    result = func(self)
                except ParseError as err:
                    self.nodes.pop()
                    if propagate:
                        raise err
                    else:
                        return None
                else:
                    last_node = self.nodes.pop()
                    if result is None or result == False:
                        if raise_error:
                            self.raise_error()
                        else:
                            return None

                    if len(last_node.components) > 0:
                        self.nodes.peek().components.append(last_node)
                    return True

            return _check
        return _decorator

    @check_parse_error(Nonterminals.Block)
    def block(self):
        self.expect(Tokens.LEFT_CURLY_BRACE)
        if not self.accept(Tokens.RIGHT_CURLY_BRACE):
            self.statement()
            self.expect(Tokens.RIGHT_CURLY_BRACE)
        else:
            pass
        return True

    @check_parse_error(Nonterminals.Statement)
    def statement(self):
        require_semicolon = True
        if self.accept(Tokens._Variable):
            self.expect(Tokens.ASSIGN)
            self.expression()
        elif self.accept(Tokens.SKIP):
            pass
        elif self.accept(Tokens.IF):
            require_semicolon = False
            self.expect(Tokens.LEFT_PAREN)
            self.condition()
            self.expect(Tokens.RIGHT_PAREN)
            self.block()
            if self.accept(Tokens.ELSE):
                self.block()
        elif self.accept(Tokens.WHILE):
            require_semicolon = False
            self.expect(Tokens.LEFT_PAREN)
            self.condition()
            self.expect(Tokens.RIGHT_PAREN)
            self.block()
        elif self.accept(Tokens.PRINT):
            self.expression()
        elif self.accept(Tokens.BEGIN_COMMENT):
            require_semicolon = False
            self.expect(Tokens._Comment)
        else:
            return True

        if require_semicolon:
            self.expect(Tokens.SEMICOLON)

        self.statement()

        return True

    @check_parse_error(Nonterminals.Condition)
    def condition(self):
        if self.accept(Tokens.TRUE):
            pass
        elif self.accept(Tokens.FALSE):
            pass
        elif self.accept(Tokens.NOT):
            self.condition()
        elif self.accept(Tokens.LEFT_PAREN):
            self.condition()
            self.expect(Tokens.RIGHT_PAREN)
        elif self.expression(raise_error=False, propagate=False):
            self.comparison_op()
            self.expression()
        else:
            return None

        if self.binary_op(raise_error=False):
            self.condition()

        return True

    @check_parse_error(Nonterminals.Expression)
    def expression(self):
        if self.accept(Tokens._Variable):
            pass
        elif self.accept(Tokens._Number):
            pass
        elif self.accept(Tokens.LEFT_PAREN):
            self.expression()
            self.expect(Tokens.RIGHT_PAREN)
        else:
            return None

        if self.arithmetic_op(raise_error=False):
            self.expression()

        return True

    @check_parse_error(Nonterminals.BinaryOp)
    def binary_op(self):
        return (self.accept(Tokens.AND) or
                self.accept(Tokens.OR))

    @check_parse_error(Nonterminals.ComparisonOp)
    def comparison_op(self):
        return (self.accept(Tokens.LT) or
                self.accept(Tokens.LEQ) or
                self.accept(Tokens.EQ) or
                self.accept(Tokens.GT) or
                self.accept(Tokens.GTE) or
                self.accept(Tokens.NEQ))

    @check_parse_error(Nonterminals.ArithmeticOp)
    def arithmetic_op(self):
        return (self.accept(Tokens.PLUS) or
                self.accept(Tokens.MINUS) or
                self.accept(Tokens.TIMES) or
                self.accept(Tokens.DIVIDE) or
                self.accept(Tokens.SHL) or
                self.accept(Tokens.SHR) or
                self.accept(Tokens.MOD))

def parse_tree_to_ast(parse_tree):
    """
    Returns abstract syntax tree (AST) from parse tree.
    """
    assert isinstance(parse_tree, Nonterminals.Program)
    return _parse_tree_to_ast(parse_tree)

def _parse_tree_to_ast(parse_tree, parent=None):
    if isinstance(parse_tree, Nonterminals.Program):
        statements = []
        if len(parse_tree.components) > 0:
            _parse_tree_to_ast(parse_tree.components[0], statements)
        return AST.SEQUENCE(statements=statements)

    if isinstance(parse_tree, Nonterminals.Block):
        statements = []
        if len(parse_tree.components) > 2:
            _parse_tree_to_ast(parse_tree.components[1], statements)
        return AST.SEQUENCE(statements=statements)

    elif isinstance(parse_tree, Nonterminals.Statement):
        result = None

        if parse_tree.components[0] == Tokens._Variable:
            result = AST.ASSIGN(
                lhs = _parse_tree_to_ast(parse_tree.components[0]),
                rhs = _parse_tree_to_ast(parse_tree.components[2])
            )

        elif parse_tree.components[0] == Tokens.SKIP:
            pass

        elif parse_tree.components[0] == Tokens.IF:
            if_false = None
            if (len(parse_tree.components) >= 6 and
                    parse_tree.components[5] == Tokens.ELSE):
                if_false = _parse_tree_to_ast(parse_tree.components[6])

            result = AST.IF(
                condition = _parse_tree_to_ast(parse_tree.components[2]),
                if_true = _parse_tree_to_ast(parse_tree.components[4]),
                if_false = if_false
            )

        elif parse_tree.components[0] == Tokens.WHILE:
            result = AST.WHILE(
                condition = _parse_tree_to_ast(parse_tree.components[2]),
                body = _parse_tree_to_ast(parse_tree.components[4]),
            )

        elif parse_tree.components[0] == Tokens.PRINT:
            result = AST.PRINT(
                expression = _parse_tree_to_ast(parse_tree.components[1])
            )

        elif parse_tree.components[0] == Tokens.BEGIN_COMMENT:
            result = AST.COMMENT(
                string = _parse_tree_to_ast(parse_tree.components[1])
            )

        else:
            raise ValueError

        if result is not None:
            parent.append(result)

        if (len(parse_tree.components) > 1 and
                parse_tree.components[-1] == Nonterminals.Statement):
            _parse_tree_to_ast(parse_tree.components[-1], parent)

    elif isinstance(parse_tree, Nonterminals.Condition):
        result = None
        if parse_tree.components[0] == Tokens.TRUE:
            result = Tokens.TRUE

        elif parse_tree.components[0] == Tokens.FALSE:
            result = Tokens.FALSE

        elif parse_tree.components[0] == Tokens.NOT:
            result = AST.NOT(
                condition = _parse_tree_to_ast(parse_tree.components[1])
            )

        elif parse_tree.components[0] == Tokens.LEFT_PAREN:
            result = _parse_tree_to_ast(parse_tree.components[1])

        elif isinstance(parse_tree.components[0], Nonterminals.Expression):
            result = ASTTokenMap.comparison_op[parse_tree.components[1].v](
                arg1 = _parse_tree_to_ast(parse_tree.components[0]),
                arg2 = _parse_tree_to_ast(parse_tree.components[2]),
            )

        else:
            raise ValueError

        if (len(parse_tree.components) > 2 and
                parse_tree.components[-2] == Nonterminals.BinaryOp):
            result = ASTTokenMap.binary_op[parse_tree.components[-2].v](
                arg1 = result,
                arg2 = _parse_tree_to_ast(parse_tree.components[-1]),
            )

        return result

    elif isinstance(parse_tree, Nonterminals.Expression):
        result = None
        if parse_tree.components[0] == Tokens._Variable:
            result = _parse_tree_to_ast(parse_tree.components[0])

        elif parse_tree.components[0] == Tokens._Number:
            result = _parse_tree_to_ast(parse_tree.components[0])

        elif parse_tree.components[0] == Tokens.LEFT_PAREN:
            result = _parse_tree_to_ast(parse_tree.components[1])

        else:
            raise ValueError

        if (len(parse_tree.components) > 2 and
                parse_tree.components[-2] == Nonterminals.ArithmeticOp):
            result = ASTTokenMap.arithmetic_op[parse_tree.components[-2].v](
                arg1 = result,
                arg2 = _parse_tree_to_ast(parse_tree.components[-1]),
            )

        return result

    elif isinstance(parse_tree, Tokens._Variable):
        return AST.Symbols.VARIABLE(parse_tree)

    elif isinstance(parse_tree, Tokens._Number):
        return AST.Symbols.NUMBER(parse_tree)

    elif isinstance(parse_tree, Tokens._Comment):
        return AST.Symbols.COMMENT(parse_tree)

    else:
        raise ValueError


