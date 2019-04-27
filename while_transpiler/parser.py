from .tokens import Tokens
from .nonterminals import *

class ParseError(Exception):
    pass

def parse(symbol_stream):
    parser = Parser(symbol_stream)
    parser.statement()
    if not parser.done:
        raise ParseError

class Parser:
    def __init__(self, symbol_stream):
        self.symbol = None
        self.symbol_stream = symbol_stream
        self.nextsym()
        self.line_num = 1

    @property
    def done(self):
        return self.symbol is None

    def nextsym(self):
        try:
            self.line_num, self.symbol = next(self.symbol_stream)
        except StopIteration:
            self.symbol = None
        print("%d >> %s" % (self.line_num, self.symbol))

    def accept(self, symbol):
        if self.symbol is None:
            return False
        if self.symbol == symbol:
            self.nextsym()
            return True
        return False

    def raise_error(self):
        raise ParseError(self.line_num)

    def expect(self, symbol):
        if self.accept(symbol):
            return True
        self.raise_error()

    def check_parse_error(func):
        def _check(self, raise_error=True, propagate=True):
            try:
                result = func(self)
            except ParseError as err:
                if propagate:
                    raise err
                else:
                    return False
            else:
                if result == False:
                    if raise_error:
                        self.raise_error()
                    else:
                        return False
                return True
        return _check

    @check_parse_error
    def block(self):
        self.expect(Tokens.LEFT_CURLY_BRACE)
        if not self.accept(Tokens.RIGHT_CURLY_BRACE):
            self.statement()
            self.expect(Tokens.RIGHT_CURLY_BRACE)
        else:
            pass

    @check_parse_error
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

    @check_parse_error
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
            return False

        if self.binary_op(raise_error=False):
            self.condition()

        return True

    @check_parse_error
    def expression(self):
        if self.accept(Tokens._Variable):
            pass
        elif self.accept(Tokens._Number):
            pass
        elif self.accept(Tokens.LEFT_PAREN):
            self.expression()
            self.expect(Tokens.RIGHT_PAREN)
        else:
            return False

        if self.arithmetic_op(raise_error=False):
            self.expression()

        return True

    @check_parse_error
    def binary_op(self):
        return (self.accept(Tokens.AND) or
                self.accept(Tokens.OR))

    @check_parse_error
    def comparison_op(self):
        return (self.accept(Tokens.LT) or
                self.accept(Tokens.LEQ) or
                self.accept(Tokens.EQ) or
                self.accept(Tokens.GT) or
                self.accept(Tokens.GTE) or
                self.accept(Tokens.NEQ))

    @check_parse_error
    def arithmetic_op(self):
        return (self.accept(Tokens.PLUS) or
                self.accept(Tokens.MINUS) or
                self.accept(Tokens.TIMES) or
                self.accept(Tokens.DIVIDE) or
                self.accept(Tokens.SHL) or
                self.accept(Tokens.SHR) or
                self.accept(Tokens.MOD))

