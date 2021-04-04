from symbol import *

create_basic_symbol_table()

path = 'PA1_sample_programs\\T10\\input.txt'
text = open(path).read()
pointer = 0
line_no = 1
lexical_errors = {}
tokens = {}


class Tokenizer:

    @staticmethod
    def tokenize_id_keyword():
        global pointer
        global line_no
        global text
        started_point = pointer
        for char in text[started_point:]:
            if char.isalnum():
                pointer += 1
            else:
                break
        # check token is a identifier or keyword or lexical error
        if len(text) <= pointer or check_regex(' \n\r\f\v\t\n/;:,[](){}+-*=<', text[pointer]):
            lexeme = find_lexeme_or_add(text[started_point:pointer])
            add_token(lexeme)
            return lexeme
        else:
            pointer += 1
            add_lexical_error((text[started_point:pointer], 'Invalid input'))

    @staticmethod
    def tokenize_number():
        global pointer
        global line_no
        global text
        started_point = pointer
        for char in text[started_point:]:
            if char.isdigit():
                pointer += 1
            else:
                break
        # check token is a number or lexical error
        if len(text) <= pointer or check_regex(' \n\r\f\v\t\n/;:,[](){}+-*=<', text[pointer]):
            number = 'NUM', text[started_point:pointer]
            add_token(number)
            return number
        else:
            pointer += 1
            add_lexical_error((text[started_point:pointer], 'Invalid number'))

    @staticmethod
    def tokenize_symbol():
        global pointer
        global line_no
        global text
        # check symbol is == or =
        if text[pointer] == '=':
            if len(text) > pointer and text[pointer + 1] == '=':
                symbol = 'SYMBOL', text[pointer: pointer + 2]
                pointer += 2
                add_token(symbol)
                return symbol
            else:
                symbol = 'SYMBOL', text[pointer]
                pointer += 1
                add_token(symbol)
                return symbol
        # check symbol is an */ (unmatched comment) or *
        elif text[pointer] == '*' and len(text) > pointer + 1 and text[pointer + 1] == '/':
            pointer += 2
            add_lexical_error(('*/', 'Unmatched comment'))
        else:
            symbol = 'SYMBOL', text[pointer]
            pointer += 1
            add_token(symbol)
            return symbol

    @staticmethod
    def ignore_comment():
        global pointer
        global line_no
        global text
        # check comment is //
        if len(text) > pointer + 1 and text[pointer + 1] == '/':
            pointer += 2
            started_point = pointer
            for char in text[started_point:]:
                pointer += 1
                if char == '\n':
                    line_no += 1
                    break
        # check comment is /*
        elif len(text) > pointer + 1 and text[pointer + 1] == '*':
            pointer += 2
            started_point = pointer
            for char in text[started_point:]:
                pointer += 1
                if char == '*' and text[pointer] == '/':
                    pointer += 1
                    break
            # check comment is an unclosed comment
            if pointer == len(text) and text[pointer - 2] != '*' and text[pointer - 1] != '/':
                add_lexical_error((f"/*{text[started_point: started_point + 5]}...", 'Unclosed comment'))
        # none of // or /*, so it is lexical error
        else:
            add_lexical_error((text[pointer], 'Invalid input'))
            pointer += 1


def find_lexeme_or_add(name):
    for lexeme in symbol_table:
        if lexeme.name == name:
            if lexeme.index >= STARTED_ID_INDEX:
                return 'ID', name
            else:
                return 'KEYWORD', name
    symbol_table.append(Lexeme.create_lexeme(name))
    return 'ID', name


def add_lexical_error(lexical_error):
    if lexical_errors.get(str(line_no), None):
        lexical_errors.get(str(line_no)).append(lexical_error)
    else:
        lexical_errors[str(line_no)] = [lexical_error]


def add_token(token):
    if token:
        if tokens.get(str(line_no), None):
            tokens.get(str(line_no)).append(token)
        else:
            tokens[str(line_no)] = [token]


def check_regex(regex: str, character):
    for char in regex:
        if character == char:
            return True
    return False


def get_next_token():
    global pointer
    global line_no
    global text
    while pointer != len(text):
        # ID and KEYWORD
        if text[pointer].isalpha():
            output = Tokenizer.tokenize_id_keyword()
            if output:
                return output
        # NUMBER
        elif text[pointer].isdigit():
            output = Tokenizer.tokenize_number()
            if output:
                return output
        # SYMBOL
        elif check_regex(';:,[](){}+-*=<', text[pointer]):
            output = Tokenizer.tokenize_symbol()
            if output:
                return output
        # COMMENT
        elif text[pointer] == '/':
            Tokenizer.ignore_comment()
        # END OF LINE
        elif text[pointer] == '\n':
            pointer += 1
            line_no += 1
        # WHITESPACE
        elif check_regex(' \t\f\r\v', text[pointer]):
            pointer += 1
        else:
            add_lexical_error((text[pointer], 'Invalid input'))
            pointer += 1


def write_tokens():
    tokens_file = ""
    if not tokens:
        tokens_file = "There is no token."
    else:
        for key, values in tokens.items():
            values_string = ""
            for value in values:
                values_string += f"({value[0]}, {value[1]}) "
            tokens_file += f"{key}.\t{values_string.strip()}\n"
    open('tokens.txt', 'w').write(tokens_file)


def write_lexical_errors():
    lexical_file = ""
    if not lexical_errors:
        lexical_file = "There is no lexical error."
    else:
        for key, values in lexical_errors.items():
            values_string = ""
            for value in values:
                values_string += f"({value[0]}, {value[1]}) "
            lexical_file += f"{key}.\t{values_string.strip()}\n"
    open('lexical_errors.txt', 'w').write(lexical_file)


def write_symbol_table():
    symbol_table_file = "".join(f"{value.index}.\t{value.name}\n" for value in symbol_table)
    open('symbol_table.txt', 'w').write(symbol_table_file)


# test
if __name__ == '__main__':
    while pointer != len(text):
        get_next_token()
    write_tokens()
    write_lexical_errors()
    write_symbol_table()
