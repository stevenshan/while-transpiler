import argparse
from .lexer import get_token_stream
from .parser import parse
from .transpiler import transpile_parsed

def main():
    parser = argparse.ArgumentParser(
        description='Transpile WHILE source code to C'
    )

    parser.add_argument('file', type=str,
                        help='Source code file to transpile.')

    parser.add_argument('-o', '--output', type=str,
                        help='Output file.')

    parser.add_argument('--token-stream', action='store_true',
                        help='Print stream of parsed tokens.')

    parser.add_argument('--parse-tree', action='store_true',
                        help='Print parse tree.')

    parser.add_argument('--ast', action='store_true',
                        help='Print AST tree.')

    parser.add_argument('--stdout', action='store_true',
                        help='Prints the transpiled C source code to STDOUT '
                             'instead of to output file.')

    parser.add_argument('--gcc', action='store_true',
                        help='Compiles transpiled C source code using gcc.')

    parser.add_argument('--exec', action='store_true',
                        help='Execute compiled program. Implicitly enables '
                             '--gcc flag.')

    args = parser.parse_args()

    with open(args.file, "r") as file_obj:
        token_stream = get_token_stream(file_obj)

        if args.token_stream:
            try:
                while True:
                    print("Line %-4d: %s" % next(token_stream))
            except StopIteration:
                exit(0)

        parse_result = parse(token_stream)

    if args.parse_tree:
        parse_result.parse_tree.print()
        exit(0)

    if args.ast:
        parse_result.ast.print()
        exit(0)

    if args.stdout:
        import sys
        transpile_parsed(parse_result, sys.stdout)
        print()
        exit(0)


    if args.gcc or args.exec:
        from .utils import c_compile, exec_file

        output_file = "a.out" if args.output is None else args.output

        status = c_compile(parse_result, output_file)

        if status == 0 and args.exec:
            exec_file(f"./{output_file}")

    else:
        output_file = "out.c" if args.output is None else args.output
        with open(output_file, "w") as file_obj:
            transpile_parsed(parse_result, file_obj)

if __name__ == "__main__":
    main()