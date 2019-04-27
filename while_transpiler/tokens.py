class ImplicitToken:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.__class__ == other

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.value}>"

class Tokens:
    """
    Predefined tokens for lexer to parse character stream into
    """

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

