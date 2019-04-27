from .tokens import Tokens
from .radix import RadixReader

TOKEN_LIST = [getattr(Tokens, x)
              for x in dir(Tokens) if not x.startswith("_")]

def is_digit(c):
    return c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

def is_letter(c):
    return c.isalpha()

def valid_first_char(c):
    """
    returns True if c is ok to use as the first character in a variable name
    """
    return is_letter(c) or c == "_"

def valid_string_char(c):
    """
    returns True if c is a valid character to use in a variable name as long as
    it is not the first character
    """
    return is_letter(c) or is_digit(c) or c == "_"

def is_stop_char(c):
    return c in (" " , "\n", "\r", "\t")

def get_symbol_stream(file_obj):
    """
    returns generator for stream of symbols read from IO object

    :param file_obj: io-like object with read method
    :returns: generator that returns Token objects
    """

    token_reader = RadixReader.from_list(TOKEN_LIST)

    rollover = False
    read_buffer = []
    test = {"reads": 0}

    def read_char():
        if len(read_buffer) == 0:
            test["reads"] += 1
            return file_obj.read(1)
        else:
            return read_buffer.pop(0)

    def read_while(read_buffer, char_buffer, pred):
        while True:
            c = read_char()
            if c == "" or not pred(c):
                break

            char_buffer.append(c)

        return [c] + read_buffer

    def maybe_implicit_token(string, token_class):
        token_reader.reset()
        if (not token_reader.add(string) or
                token_reader.last_string != string):
            return token_class(string)
        return string

    while True:
        c = read_char()

        if c == "":
            break

        if is_stop_char(c):
            continue

        # read variable names
        if is_letter(c):
            char_buffer = [c]
            read_buffer = read_while(
                    read_buffer, char_buffer, valid_string_char)

            yield maybe_implicit_token("".join(char_buffer), Tokens._Variable)
            continue

        # read numbers
        if is_digit(c):
            char_buffer = [c]
            read_buffer = read_while(read_buffer, char_buffer, is_digit)

            yield maybe_implicit_token("".join(char_buffer), Tokens._Number)
            continue

        accepted_any = False
        token_reader.reset()
        while token_reader.add(c):
            accepted_any = True
            c = read_char()
            if c == "":
                break

        if not accepted_any:
            yield c
        else:
            read_buffer = token_reader.unmatched + [c] + read_buffer

            result = token_reader.last_string
            if result == "":
                continue

            yield result

            if result == Tokens.BEGIN_COMMENT:
                # read in rest of comment
                char_buffer = []
                last_two = ("", "")
                while last_two[0] != "*" or last_two[1] != "/":
                    c = read_char()
                    char_buffer.append(c)
                    if c == "":
                        break

                    last_two = last_two[1], c


                yield maybe_implicit_token(
                    "".join(char_buffer[:-2]),
                    Tokens._Comment
                )
                yield Tokens.END_COMMENT

