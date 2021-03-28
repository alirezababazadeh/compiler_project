from buffer import Buffer
from symbol import *
from consts import *


class Tokenizer:
    def __init__(self, program_buffer):
        self.buffer = program_buffer

    def get_next_token(self):
        while self.buffer.has_next():
            current_char = self.buffer.get_current_char()
            # ID and KEYWORD
            if str.isalpha(current_char):
                output = self.tokenize_id_keyword()
                if output:
                    return output
            # NUMBER
            elif str.isdigit(current_char):
                output = self.tokenize_number()
                if output:
                    return output
            # SYMBOL
            elif current_char in SYMBOLS:
                output = self.tokenize_symbol()
                if output:
                    return output
            # COMMENT
            elif current_char in COMMENTS:
                self.ignore_comment()
            # END OF LINE
            elif current_char == '\n':
                self.buffer.push_forward()
                self.buffer.increase_line_number()
            # WHITESPACE
            elif current_char in SPACES:
                self.buffer.push_forward()
            else:
                add_lexical_error((current_char, 'Invalid input'), self.buffer.line_number)
                self.buffer.push_forward()

    def tokenize_id_keyword(self):
        started_point = self.buffer.pointer
        for char in self.buffer.text[started_point:]:
            if char.isalnum():
                self.buffer.push_forward()
            else:
                break
        # check token is a identifier or keyword or lexical error
        current_char = self.buffer.get_current_char()
        if current_char in SYMBOLS or current_char in SPACES:
            lexeme = find_lexeme_or_add(self.buffer.get_text(started_point, self.buffer.pointer))
            add_token(lexeme, self.buffer.line_number)
            return lexeme
        else:
            self.buffer.push_forward()
            add_lexical_error((self.buffer.get_text(started_point, self.buffer.pointer), 'Invalid input'),
                              self.buffer.line_number)

    def tokenize_number(self):
        started_point = self.buffer.pointer
        for char in self.buffer.text[started_point:]:
            if char.isdigit():
                self.buffer.push_forward()
            else:
                break
        # check token is a number or lexical error
        current_char = self.buffer.get_current_char()
        if current_char in SYMBOLS or current_char in SPACES:
            number = 'NUM', self.buffer.get_text(started_point, self.buffer.pointer)
            add_token(number, self.buffer.line_number)
            return number
        else:
            self.buffer.push_forward()
            add_lexical_error((self.buffer.get_text(started_point, self.buffer.pointer), 'Invalid number'),
                              self.buffer.line_number)

    def tokenize_symbol(self):
        # check symbol is == or =
        current_char = self.buffer.get_current_char()
        if current_char == '=':
            next_char = self.buffer.get_char_at(self.buffer.pointer + 1)
            if next_char == '=':
                symbol = 'SYMBOL', self.buffer.get_text(self.buffer.pointer, self.buffer.pointer + 2)
                self.buffer.push_forward(2)
                add_token(symbol, self.buffer.line_number)
                return symbol
            else:
                symbol = 'SYMBOL', current_char
                self.buffer.push_forward()
                add_token(symbol, self.buffer.line_number)
                return symbol
        # check symbol is an */ (unmatched comment) or *
        elif current_char == '*' and self.buffer.get_char_at(self.buffer.pointer + 1) == '/':
            self.buffer.push_forward(2)
            add_lexical_error(('*/', 'Unmatched comment'), self.buffer.line_number)
        else:
            symbol = 'SYMBOL', current_char
            self.buffer.push_forward()
            add_token(symbol, self.buffer.line_number)
            return symbol

    def ignore_comment(self):
        next_char = self.buffer.get_char_at(self.buffer.pointer + 1)
        # check comment is //
        if next_char == '/':
            self.buffer.push_forward(2)
            started_point = self.buffer.pointer
            for char in self.buffer.text[started_point:]:
                self.buffer.push_forward()
                if char == '\n':
                    self.buffer.increase_line_number()
                    break
        # check comment is /*
        elif next_char == '*':
            self.buffer.push_forward(2)
            started_point = self.buffer.pointer
            for char in self.buffer.text[started_point:]:
                self.buffer.push_forward()
                if char == '*' and self.buffer.get_current_char() == '/':
                    self.buffer.push_forward()
                    break
            # check comment is an unclosed comment
            text = self.buffer.text
            pointer = self.buffer.pointer
            if pointer == len(text) and text[pointer - 2] != '*' and text[pointer - 1] != '/':
                add_lexical_error((f"/*{text[started_point: started_point + 5]}...", 'Unclosed comment'),
                                  self.buffer.line_number)
        # none of // or /*, so it is lexical error
        else:
            add_lexical_error((self.buffer.get_current_char(), 'Invalid input'), self.buffer.line_number)
            self.buffer.push_forward()


def find_lexeme_or_add(name):
    for lexeme in symbol_table:
        if lexeme.name == name:
            if lexeme.name not in KEYWORDS:
                return 'ID', name
            else:
                return 'KEYWORD', name
    symbol_table.append(Lexeme.create_lexeme(name))
    return 'ID', name


def add_lexical_error(lexical_error, line_no):
    if lexical_errors.get(str(line_no), None):
        lexical_errors.get(str(line_no)).append(lexical_error)
    else:
        lexical_errors[str(line_no)] = [lexical_error]


def add_token(token, line_no):
    if token:
        if tokens.get(str(line_no), None):
            tokens.get(str(line_no)).append(token)
        else:
            tokens[str(line_no)] = [token]


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
    open('out\\tokens.txt', 'w').write(tokens_file)


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
    open('out\\lexical_errors.txt', 'w').write(lexical_file)


def write_symbol_table():
    symbol_table_file = "".join(f"{value.index}.\t{value.name}\n" for value in symbol_table)
    open('out\\symbol_table.txt', 'w').write(symbol_table_file)


# test
if __name__ == '__main__':

    create_basic_symbol_table()
    path = 'PA1_sample_programs\\T10\\input.txt'
    program_text = open(path).read()

    buffer = Buffer(program_text)
    tokenizer = Tokenizer(buffer)
    lexical_errors = {}
    tokens = {}
    while buffer.has_next():
        tokenizer.get_next_token()

    write_tokens()
    write_lexical_errors()
    write_symbol_table()
