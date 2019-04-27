from while_transpiler import parser, lexer

with open("test.w", "r") as file_obj:
    token_stream = lexer.get_token_stream(file_obj)

    parse_result = parser.parse(token_stream)

test=  parse_result.ast
