from .tokens import Tokens
from .stack import Stack
from .nonterminals import *

class ParseError(Exception):
    pass

def parse(token_stream):
    parser = Parser(token_stream)
    parser.statement()
    if not parser.done:
        raise ParseError

    return parser.nodes.peek()

class Parser:
    def __init__(self, token_stream):
        self.token = None
        self.token_stream = token_stream
        self.nextsym()
        self.line_num = 1

        self.nodes = Stack()
        self.nodes.push(Program())

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

                    self.nodes.peek().components.append(last_node)
                    return True

            return _check
        return _decorator

    @check_parse_error(Block)
    def block(self):
        self.expect(Tokens.LEFT_CURLY_BRACE)
        if not self.accept(Tokens.RIGHT_CURLY_BRACE):
            self.statement()
            self.expect(Tokens.RIGHT_CURLY_BRACE)
        else:
            pass
        return True

    @check_parse_error(Statement)
    def statement(self):
        result = Statement()
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

    @check_parse_error(Condition)
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

    @check_parse_error(Expression)
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

    @check_parse_error(BinaryOp)
    def binary_op(self):
        return (self.accept(Tokens.AND) or
                self.accept(Tokens.OR))

    @check_parse_error(ComparisonOp)
    def comparison_op(self):
        return (self.accept(Tokens.LT) or
                self.accept(Tokens.LEQ) or
                self.accept(Tokens.EQ) or
                self.accept(Tokens.GT) or
                self.accept(Tokens.GTE) or
                self.accept(Tokens.NEQ))

    @check_parse_error(ArithmeticOp)
    def arithmetic_op(self):
        return (self.accept(Tokens.PLUS) or
                self.accept(Tokens.MINUS) or
                self.accept(Tokens.TIMES) or
                self.accept(Tokens.DIVIDE) or
                self.accept(Tokens.SHL) or
                self.accept(Tokens.SHR) or
                self.accept(Tokens.MOD))

