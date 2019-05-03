import argparse
from .transpiler import (
    lexer,
    parser,
    transpile_c,
    utils as transpiler_utils,
)

def main():
    argparser = argparse.ArgumentParser(
        description='Transpile WHILE source code to C'
    )

    argparser.add_argument('file', type=str,
                        help='Source code file to transpile.')

    argparser.add_argument('-o', '--output', type=str,
                        help='Output file.')

    argparser.add_argument('--token-stream', action='store_true',
                        help='Print stream of parsed tokens.')

    argparser.add_argument('--parse-tree', action='store_true',
                        help='Print parse tree.')

    argparser.add_argument('--ast', action='store_true',
                        help='Print AST tree.')

    argparser.add_argument('--stdout', action='store_true',
                        help='Prints the transpiled C source code to STDOUT '
                             'instead of to output file.')

    argparser.add_argument('--gcc', action='store_true',
                        help='Compiles transpiled C source code using gcc.')

    argparser.add_argument('--exec', action='store_true',
                        help='Execute compiled program. Implicitly enables '
                             '--gcc flag.')

    args = argparser.parse_args()

    with open(args.file, "r") as file_obj:
        token_stream = lexer.get_token_stream(file_obj)

        if args.token_stream:
            try:
                while True:
                    print("Line %-4d: %s" % next(token_stream))
            except StopIteration:
                exit(0)

        parse_result = parser.parse(token_stream)

    if args.parse_tree:
        parse_result.parse_tree.print()
        exit(0)

    if args.ast:
        parse_result.ast.print()
        exit(0)

    if args.stdout:
        import sys
        transpile_c.transpile_parsed(parse_result, sys.stdout)
        print()
        exit(0)


    if args.gcc or args.exec:
        output_file = "a.out" if args.output is None else args.output

        status = transpiler_utils.c_compile(parse_result, output_file)

        if status == 0 and args.exec:
            transpiler_utils.exec_file(f"./{output_file}")

    else:
        output_file = "out.c" if args.output is None else args.output
        with open(output_file, "w") as file_obj:
            transpile_parsed(parse_result, file_obj)

if __name__ == "__main__":
    main()
