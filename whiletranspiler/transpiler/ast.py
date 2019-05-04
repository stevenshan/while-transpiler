"""
Definition of nodes and symbols in abstract syntax tree (AST)
"""

from .shared import TokenMetadata
from .tokens import Tokens, TokenString
from .config import INDENT

class ASTNode(TokenMetadata):
    def __init__(self, **kwargs):
        parent = kwargs.pop("parent")
        self.set_metadata([parent])

        for key, value in kwargs.items():
            assert hasattr(self.__class__, key)
            setattr(self, key, value)

    def _fields(self):
        parent_fields = dir(ASTNode)
        fields = [x for x in dir(self.__class__)
                if not x.startswith("_") and x not in parent_fields]
        return ((field, getattr(self, field)) for field in fields)

    def print(self, indent_level=0, return_str=False):
        prefix = INDENT * indent_level
        acc = ""
        string = f"{self.__class__.__name__}"
        if return_str:
            acc += f"{string}\n"
        else:
            print(string)
        prefix += INDENT
        for field, value in self._fields():
            string = f"{prefix}{field}: "
            if return_str:
                acc += string
            else:
                print(string, end="")
            if isinstance(value, ASTNode):
                temp = value.print(indent_level+1, return_str=return_str)
                if return_str:
                    acc += f"{temp}"
            else:
                if return_str:
                    acc += f"{value}\n"
                else:
                    print(value)

        if return_str:
            return acc

class ASTSymbol(TokenMetadata):
    def __init__(self, parent_instance):
        self.set_metadata([parent_instance])

        assert isinstance(parent_instance, self.parent_cls)
        if hasattr(parent_instance, "value"):
            self.value = parent_instance.value
        else:
            self.value = parent_instance

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return self.value == other

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.value}>"

class BinOp(ASTNode):
    arg1 = None
    arg2 = None

class AST:
    """
    Nodes in abstract syntax tree (AST)
    """

    class Symbols:
        class VARIABLE(ASTSymbol):
            parent_cls = Tokens._Variable

        class NUMBER(ASTSymbol):
            parent_cls = Tokens._Number

        class BOOLEAN(ASTSymbol):
            parent_cls = TokenString

        class COMMENT(ASTSymbol):
            parent_cls = Tokens._Comment

    class SEQUENCE(ASTNode):
        statements = None

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_metadata(self.statements)

        def _fields(self):
            return enumerate(self.statements)

    class ASSIGN(ASTNode):
        lhs = None
        rhs = None

    class IF(ASTNode):
        condition = None
        if_true = None
        if_false = None

    class WHILE(ASTNode):
        condition = None
        body = None

    class PRINT(ASTNode):
        expression = None

    class COMMENT(ASTNode):
        string = None

    class NOT(ASTNode):
        condition = None

    class AND(BinOp): pass
    class OR(BinOp): pass
    class LT(BinOp): pass
    class LEQ(BinOp): pass
    class EQ(BinOp): pass
    class GT(BinOp): pass
    class GTE(BinOp): pass
    class NEQ(BinOp): pass
    class PLUS(BinOp): pass
    class MINUS(BinOp): pass
    class TIMES(BinOp): pass
    class DIVIDE(BinOp): pass
    class SHL(BinOp): pass
    class SHR(BinOp): pass
    class MOD(BinOp): pass

class ASTTokenMap:
    binary_op = {
        Tokens.AND: AST.AND,
        Tokens.OR: AST.OR,
    }

    comparison_op = {
        Tokens.LT: AST.LT,
        Tokens.LEQ: AST.LEQ,
        Tokens.EQ: AST.EQ,
        Tokens.GT: AST.GT,
        Tokens.GTE: AST.GTE,
        Tokens.NEQ: AST.NEQ,
    }

    arithmetic_op = {
        Tokens.PLUS: AST.PLUS,
        Tokens.MINUS: AST.MINUS,
        Tokens.TIMES: AST.TIMES,
        Tokens.DIVIDE: AST.DIVIDE,
        Tokens.SHL: AST.SHL,
        Tokens.SHR: AST.SHR,
        Tokens.MOD: AST.MOD,
    }
