"""
Definition of nodes in parse tree
"""

from .config import INDENT
from .shared import TokenMetadata

class _Node(TokenMetadata):
    force_merge_metadata = False

    def __init__(self):
        self.components = []

    @property
    def v(self):
        return self.components[0]

    def add_component(self, component):
        self.components.append(component)
        if (self.force_merge_metadata or
                not isinstance(component, Nonterminals.Statement)):
            # statements are nested within the previous statement so we
            # dont' want the metadata of the previous statement to include
            # the next statement's metadata
            self.merge_metadata([component])

    def __repr__(self):
        children = [(x.__class__.__name__ if isinstance(x, _Node) else x) for
                x in self.components]
        return f"<{self.__class__.__name__} {children}>"

    def __str__(self):
        return f"{self.__class__.__name__}"

    def __eq__(self, other):
        return self.__class__ == other

    def print(self, indent_level=0, return_str=False):
        prefix = INDENT * indent_level
        acc = ""
        string = f"{prefix}{self}"
        if return_str:
            acc += f"{string}\n"
        else:
            print(string)
        prefix += INDENT
        for component in self.components:
            if isinstance(component, _Node):
                temp = component.print(
                    indent_level=indent_level + 1,
                    return_str=return_str
                )
                if return_str:
                    acc += f"{temp}"
            else:
                string = f"{prefix}{component}"
                if return_str:
                    acc += f"{string}\n"
                else:
                    print(string)

        if return_str:
            return acc

class Nonterminals:
    class Program(_Node):
        force_merge_metadata = True

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
