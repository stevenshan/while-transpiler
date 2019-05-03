"""
Definition of tokens for lexer to parse character stream into
"""

from .shared import TokenMetadata

class ImplicitToken(TokenMetadata):
    def __init__(self, value):
        self.value = value
        if isinstance(value, TokenMetadata):
            self.set_metadata([value])

    def __eq__(self, other):
        return self.__class__ == other

    def __repr__(self):
        return f"<{self.__class__.__name__.strip('_')} {self.value}>"

class TokenString(str, TokenMetadata):
    def __init__(self, *args, **kwargs):
        if "line_num" in kwargs:
            line_num = kwargs["line_num"]
            self.line_range = (line_num, line_num)

        if "char_num" in kwargs:
            char_num = kwargs["char_num"]
            self.char_range = (char_num, char_num)

    @classmethod
    def join(cls, objects):
        string = "".join(objects)
        obj = cls(string)
        obj.set_metadata(objects)
        return obj

    def __add__(self, other):
        if isinstance(other, TokenString):
            return self.join((self, other))
        else:
            obj = TokenString(self + other, line_num=0)
            obj.line_range = self.line_range
            return obj

    def __radd__(self, other):
        return self.__add__(other)

    def __new__(cls, string_arg, line_num=None, char_num=None):
        str_obj = str.__new__(cls, string_arg)
        return str_obj

class Tokens:
    class _Variable(ImplicitToken):
        pass

    class _Number(ImplicitToken):
        pass

    class _Comment(ImplicitToken):
        pass

    LEFT_CURLY_BRACE = "{"
    RIGHT_CURLY_BRACE = "}"

    ASSIGN = "="
    SKIP = "skip"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    PRINT = "print"

    SEMICOLON = ";"

    LEFT_PAREN = "("
    RIGHT_PAREN = ")"

    BEGIN_COMMENT = "//"

    TRUE = "true"
    FALSE = "false"
    NOT = "not"

    # Binary Operations
    AND = "and"
    OR = "or"

    # Comparison Operations
    LT = "<"
    LEQ = "<="
    EQ = "=="
    GT = ">"
    GTE = ">="
    NEQ = "!="

    # Arithmetic Operations
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIVIDE = "/"
    SHL = "<<"
    SHR = ">>"
    MOD = "%"

