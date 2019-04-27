from .tokens import Tokens
from .nonterminals import *

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, symbol_stream):
        self.symbol = ""
        self.symbol_stream = symbol_stream

    def nextsym(self):
        self.symbol = next(self.symbol_stream)

    def accept(self, symbol):
        if self.symbol == symbol:
            self.nextsym()
            return True
        return False

    def expect(self, symbol):
        if self.accept(symbol):
            return True
        raise ParseError

    def _check_parse_error(func):
        def _check(self, raise_error = True):
            try:
                result = self.func()
            except ParseError as err:
                if raise_error:
                    raise err
                else:
                    return False
            else:
                if result == False:
                    if raise_error:
                        raise ParseError
                    else:
                        return False
                return True
        return _check

    @_check_parse_error
    def block(self):
        self.expect(Tokens.LEFT_CURLY_BRACE)
        self.statement()
        self.expect(Tokens.RIGHT_CURLY_BRACE)
        return True

    @_check_parse_error
    def statement(self):
        matched = False
        if self.accept(Tokens._Variable):
            self.expect(Tokens.ASSIGN)
            self.expression()
        elif self.accept(Tokens.SKIP):
            pass
        elif self.accept(Tokens.IF):
            self.expect(Tokens.LEFT_PAREN)
            self.condition()
            self.expect(Tokens.RIGHT_PAREN)
            self.block()
            self.expect(Tokens.ELSE)
            self.block()
            self.statement()
        elif self.accept(Tokens.WHILE):
            self.expect(Tokens.LEFT_PAREN)
            self.condition()
            self.expect(Tokens.RIGHT_PAREN)
            self.block()
            self.statement()
        elif self.accept(Tokens.PRINT):
            self.expression()
        elif self.accept(Tokens.BEGIN_COMMENT):
            self.expect(Tokens._Comment)
            self.expect(Tokens.END_COMMENT)
            self.statement()
        else:
            return False

        if self.accept(Tokens.SEMICOLON):
            self.statement()

        return True

    @_check_parse_error
    def condition(self):
        if self.accept(Tokens.TRUE):
            pass
        elif self.accept(Tokens.FALSE):
            pass
        elif self.accept(Tokens.NOT):
            self.condition()

        if self.expression(raise_error=False):
            self.expect(

    @_check_parse_error
    def arithmetic_op(self):
        if

