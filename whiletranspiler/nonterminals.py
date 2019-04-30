"""
Definition of nodes in parse tree
"""

from .config import INDENT

class _Node:
    def __init__(self):
        self.components = []

    @property
    def v(self):
        return self.components[0]

    def __repr__(self):
        children = [(x.__class__.__name__ if isinstance(x, _Node) else x) for
                x in self.components]
        return f"<{self.__class__.__name__} {children}>"

    def __str__(self):
        return f"{self.__class__.__name__}"

    def __eq__(self, other):
        return self.__class__ == other

    def print(self, indent_level=0):
        prefix = INDENT * indent_level
        print(f"{prefix}{self}")
        prefix += INDENT
        for component in self.components:
            if isinstance(component, _Node):
                component.print(indent_level=indent_level + 1)
            else:
                print(f"{prefix}{component}")

class Nonterminals:
    class Program(_Node):
        pass

    class Block(_Node):
        pass

    class Statement(_Node):
        pass

    class Condition(_Node):
        pass

    class Expression(_Node):
        pass

    class BinaryOp(_Node):
        pass

    class ComparisonOp(_Node):
        pass

    class ArithmeticOp(_Node):
        pass