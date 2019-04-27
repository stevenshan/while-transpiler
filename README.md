# WHILE Language Transpiler

Transpiler written in Python to convert WHILE source code to C.

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
           |   "(" Expression ")"
           |   Expression arithmetic_op Expression

binary_op  ::= "and" | "or"
comparison_op ::= "<" | "<=" | "==" | ">" | ">=" | "!="
arithmetic_op ::= "+" | "-" | "*" | "/" | "<<" | ">>" | "%"
```

## Features

### Token Stream

Prints list of tokens and corresponding line numbers that were parsed from source code. Include the `--token-stream` flag.
```
python -m while_transpiler --token-stream file.w
```


### Parse Tree

Print the parse tree for WHILE source code. Include the `--parse-tree` flag.
```
python -m while_transpiler --parse-tree file.w
```

