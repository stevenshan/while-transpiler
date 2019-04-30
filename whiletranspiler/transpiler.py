"""
Code for converting AST into C source code
"""

from .ast import AST
from .config import INDENT

BINOP_MAP = [
    (AST.AND, "&&"),
    (AST.OR, "||"),
    (AST.LT, "<"),
    (AST.LEQ, "<="),
    (AST.EQ, "=="),
    (AST.GT, ">"),
    (AST.GTE, ">="),
    (AST.NEQ, "!="),
    (AST.PLUS, "+"),
    (AST.MINUS, "-"),
    (AST.TIMES, "*"),
    (AST.DIVIDE, "/"),
    (AST.SHL, "<<"),
    (AST.SHR, ">>"),
    (AST.MOD, "%"),
]

def transpile_parsed(parsed, file_obj):
    """
    Wrapper to convert result of parsing to C code.
    """

    class _OptionsClosure:
        def __init__(self):
            self.outer_paren_grouping = False
            self.indent = 0

    options_closure = _OptionsClosure()

    def write(string, begin_line=False):
        if begin_line:
            level = options_closure.indent - 1
            file_obj.write(f"{INDENT * level}{string}")
        else:
            file_obj.write(string)

    def generate_output(ast_node):
        """
        Converts abstract syntax tree to C code.
        """

        outer_paren_grouping = options_closure.outer_paren_grouping
        options_closure.outer_paren_grouping = False
        options_closure.indent += 1

        if isinstance(ast_node, AST.SEQUENCE):
            options_closure.indent -= 1
            for statement in ast_node.statements:
                generate_output(statement)
            options_closure.indent += 1

        elif isinstance(ast_node, AST.ASSIGN):
            write(f"{ast_node.lhs.value} = ", begin_line=True)
            options_closure.outer_paren_grouping = True
            generate_output(ast_node.rhs)
            write(";\n")

        elif isinstance(ast_node, AST.IF):
            write(f"if (", begin_line=True)
            options_closure.outer_paren_grouping = True
            generate_output(ast_node.condition)
            write(") {\n")
            generate_output(ast_node.if_true)
            if ast_node.if_false is not None:
                write("} else {\n", begin_line=True)
                generate_output(ast_node.if_false)
            write("}\n", begin_line=True)

        elif isinstance(ast_node, AST.WHILE):
            write(f"while (", begin_line=True)
            options_closure.outer_paren_grouping = True
            generate_output(ast_node.condition)
            write(") {\n")
            generate_output(ast_node.body)
            write("}\n", begin_line=True)

        elif isinstance(ast_node, AST.PRINT):
            write(f'printf("%d\\n", ', begin_line=True)
            options_closure.outer_paren_grouping = True
            generate_output(ast_node.expression)
            write(");\n")

        elif isinstance(ast_node, AST.COMMENT):
            write(f"//{ast_node.string.value}\n", begin_line=True)

        elif isinstance(ast_node, AST.NOT):
            write("!")
            generate_output(ast_node.condition)

        elif (isinstance(ast_node, AST.Symbols.VARIABLE) or
                isinstance(ast_node, AST.Symbols.NUMBER) or
                isinstance(ast_node, AST.Symbols.COMMENT)):
            write(f"{ast_node}")

        elif isinstance(ast_node, AST.Symbols.BOOLEAN):
            if ast_node.value == "true":
                write("1");
            elif ast_node.value == "false":
                write("0");
            else:
                raise ValueError("Unimplemented boolean value")

        else:
            found = False
            # convert binary operations
            for cls, symbol in BINOP_MAP:
                if isinstance(ast_node, cls):
                    if not outer_paren_grouping:
                        write("(")
                    generate_output(ast_node.arg1)
                    write(f" {symbol} ")
                    generate_output(ast_node.arg2)
                    if not outer_paren_grouping:
                        write(")")
                    found = True
                    break

            if not found:
                raise ValueError("Unimplemented AST node")

        options_closure.indent -= 1

    write("#include <stdio.h>\n"
          "int main() {\n", begin_line=True)

    options_closure.indent += 1
    if len(parsed.variable_names) > 0:
        write(f"{INDENT}int {', '.join(parsed.variable_names)};\n",
                begin_line=True)
    generate_output(parsed.ast)
    options_closure.indent -= 1

    write("}", begin_line=True)

