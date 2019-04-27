import argparse
from .lexer import get_token_stream
from .parser import parse

parser = argparse.ArgumentParser(
    description='Transpile WHILE source code to C'
)

parser.add_argument('file', type=str,
                    help='Source code file to transpile.')

parser.add_argument('-o', '--output', type=str, default='out.c',
                    help='Output .c file to place transpiled code in.')

parser.add_argument('--token-stream', action='store_true',
                    help='Print stream of parsed tokens.')

parser.add_argument('--parse-tree', action='store_true',
                    help='Print parse tree.')

args = parser.parse_args()

with open(args.file, "r") as file_obj:
    token_stream = get_token_stream(file_obj)

    if args.token_stream:
        try:
            while True:
                print("Line %-4d: %s" % next(token_stream))
        except StopIteration:
            exit(0)

    parsed = parse(token_stream)

if args.parse_tree:
    parsed.print()
    exit(0)

