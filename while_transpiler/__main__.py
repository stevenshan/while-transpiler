import argparse
from .lexer import get_symbol_stream
from .parser import parse

parser = argparse.ArgumentParser(
    description='Transpile WHILE source code to C'
)

parser.add_argument('file', type=str,
                    help='Source code file to transpile.')

parser.add_argument('-o', '--output', type=str, default='out.c',
                    help='Output .c file to place transpiled code in.')

args = parser.parse_args()

with open(args.file, "r") as file_obj:
    symbol_stream = get_symbol_stream(file_obj)
    parse(symbol_stream)

