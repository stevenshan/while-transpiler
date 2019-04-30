# WHILE Language Transpiler

Transpiler written in Python to convert WHILE source code to C.

## Installation

### Build from source

1. Clone this repository.
2. Run `python setup.py install`.

## Usage

To compile WHILE source code file named `test.w`:
```
whiletranspiler test.w
```
The default output C source code file is `out.c`. This can be changed with the `-o` flag.

To compile the transpiled C source code, include the `--gcc` flag. To execute the program, include the `--exec` flag.

### Output Options

Command line flag options to control the output:

- Token Stream
    - `--token-stream`
- Parse Tree
    - `--parse-tree`
- Abstract Syntax Tree (AST)
    - `--ast`
- Display transpiled C source code
    - `--stdout`

## Testing

Run `pytest` to run test cases.

## Language Rules

```
Block ::= "{" Statement "}"

Statement ::= x "=" Expression
          |   "skip"
          |   Statement; Statement
          |   "if" "(" Condition ")" Block "else" Block Statement
          |   "while" "(" Condition ")" Block Statement
          |   "print" Expression
          |   "//" Comment "\n" Statement

Condition ::= "true"
          |   "false"
          |   "not" Condition
          |   "(" Condition ")"
          |   Condition binary_op Condition
          |   Expression comparison_op Expression

Expression ::= x
           |   n
           |   "-" Expression
           |   "(" Expression ")"
           |   Expression arithmetic_op Expression

binary_op  ::= "and" | "or"
comparison_op ::= "<" | "<=" | "==" | ">" | ">=" | "!="
arithmetic_op ::= "+" | "-" | "*" | "/" | "<<" | ">>" | "%"
```
Note that all variables in WHILE have global scope.

