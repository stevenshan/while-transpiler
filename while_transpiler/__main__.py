import argparse
from . import lexer
from . import parser

parser = argparse.ArgumentParser(
    description='Transpile WHILE source code to C'
)

parser.add_argument('file', type=str,
                    help='Source code file to transpile.')

parser.add_argument('-o', '--output', type=str, default='out.c',
                    help='Output .c file to place transpiled code in.')

args = parser.parse_args()

with open(args.file, "r") as file_obj:
    symbol_stream = lexer.get_symbol_stream(file_obj)

    while True:
        print("%s" % next(symbol_stream))

