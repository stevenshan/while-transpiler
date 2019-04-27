# WHILE Language Transpiler

Transpiler written in Python to convert WHILE source code to C.

## Language Rules

```
Block ::= "{" Statement "}"

Statement ::= x "=" Expression
          |   "skip"
          |   Statement; Statement
          |   "if" "(" Condition ")" Block "else" Block
          |   "while" "(" Condition ")" Block
          |   "print" Expression
          |   "//" Comment

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
