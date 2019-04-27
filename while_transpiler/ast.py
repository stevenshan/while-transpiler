from .tokens import Tokens

class ASTNode:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            assert hasattr(self.__class__, key)
            setattr(self, key, value)

class BinOp(ASTNode):
    arg1 = None
    arg2 = None

class AST:
    """
    Nodes in abstract syntax tree (AST)
    """

    class SEQUENCE(ASTNode):
        statements = None

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
