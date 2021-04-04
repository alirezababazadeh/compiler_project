from buffer import Buffer
from error_handler import ErrorHandler
from symbol_table import SymbolTable
from consts import *
from token_repo import TokenRepository


class Tokenizer:
    def __init__(self, program_buffer, token_repository, error_handler, symbol_table):
        self.buffer = program_buffer
        self.token_repository = token_repository
        self.error_handler = error_handler
        self.symbol_table = symbol_table

    def get_next_token(self):
        while self.buffer.has_next():
            current_char = self.buffer.current_char()
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
            elif current_char in LINE_BREAKS:
                self.buffer.push_forward()
                self.buffer.increase_line_number()
            # WHITESPACE
            elif current_char in SPACES:
                self.buffer.push_forward()
            else:
                self.error_handler.add_lexical_error((current_char, 'Invalid input'), self.buffer.line_number)
                self.buffer.push_forward()

    def tokenize_id_keyword(self):
        started_point = self.buffer.pointer
        for char in self.buffer.text[started_point:]:
            if char.isalnum():
                self.buffer.push_forward()
            else:
                break
        # check token is a identifier or keyword or lexical error
        current_char = self.buffer.current_char()
        if current_char in SYMBOLS or current_char in SPACES or current_char in COMMENTS:
            lexeme = self.find_lexeme_or_add(self.buffer.get_text(started_point, self.buffer.pointer))
            self.token_repository.add_token(lexeme, self.buffer.line_number)
            return lexeme
        else:
            self.buffer.push_forward()
            self.error_handler.add_lexical_error(
                (self.buffer.get_text(started_point, self.buffer.pointer), 'Invalid input'),
                self.buffer.line_number)

    def tokenize_number(self):
        started_point = self.buffer.pointer
        for char in self.buffer.text[started_point:]:
            if char.isdigit():
                self.buffer.push_forward()
            else:
                break
        # check token is a number or lexical error
        current_char = self.buffer.current_char()
        if current_char in SYMBOLS or current_char in SPACES or current_char in COMMENTS:
            number = 'NUM', self.buffer.get_text(started_point, self.buffer.pointer)
            self.token_repository.add_token(number, self.buffer.line_number)
            return number
        else:
            self.buffer.push_forward()
            self.error_handler.add_lexical_error(
                (self.buffer.get_text(started_point, self.buffer.pointer), 'Invalid number'),
                self.buffer.line_number)

    def tokenize_symbol(self):
        # check symbol is == or =
        current_char = self.buffer.current_char()
        if current_char == '=':
            next_char = self.buffer.get_char_at(self.buffer.pointer + 1)
            if next_char == '=':
                symbol = 'SYMBOL', self.buffer.get_text(self.buffer.pointer, self.buffer.pointer + 2)
                self.buffer.push_forward(2)
                self.token_repository.add_token(symbol, self.buffer.line_number)
                return symbol
            else:
                symbol = 'SYMBOL', current_char
                self.buffer.push_forward()
                self.token_repository.add_token(symbol, self.buffer.line_number)
                return symbol
        # check symbol is an */ (unmatched comment) or *
        elif current_char == '*' and self.buffer.get_char_at(self.buffer.pointer + 1) == '/':
            self.buffer.push_forward(2)
            self.error_handler.add_lexical_error(('*/', 'Unmatched comment'), self.buffer.line_number)
        else:
            symbol = 'SYMBOL', current_char
            self.buffer.push_forward()
            self.token_repository.add_token(symbol, self.buffer.line_number)
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
                if char == '*' and self.buffer.current_char() == '/':
                    self.buffer.push_forward()
                    break
            # check comment is an unclosed comment
            text = self.buffer.text
            pointer = self.buffer.pointer
            if pointer == len(text) and text[pointer - 2] != '*' and text[pointer - 1] != '/':
                self.error_handler.add_lexical_error(
                    (f"/*{text[started_point: started_point + 5]}...", 'Unclosed comment'),
                    self.buffer.line_number)
        # none of // or /*, so it is lexical error
        else:
            self.error_handler.add_lexical_error((self.buffer.current_char(), 'Invalid input'),
                                                 self.buffer.line_number)
            self.buffer.push_forward()

    def find_lexeme_or_add(self, name):
        self.symbol_table.add_lexeme_if_absent(name)
        if name not in KEYWORDS:
            return 'ID', name
        else:
            return 'KEYWORD', name


def write_tokens(token_repository):
    tokens_file = ""
    if token_repository.has_any():
        tokens_file = str(token_repository)
    else:
        tokens_file = "There is no token."
    open('out\\tokens.txt', 'w').write(tokens_file)


def write_lexical_errors(error_handler):
    lexical_file = ""
    if error_handler.has_any_error():
        lexical_file = str(error_handler)
    else:
        lexical_file = "There is no lexical error."

    open('out\\lexical_errors.txt', 'w').write(lexical_file)


def write_symbol_table(symbol_table):
    open('out\\symbol_table.txt', 'w').write(str(symbol_table))


def main():
    path = 'PA1_sample_programs\\T10\\input.txt'
    program_text = open(path).read()

    buffer = Buffer(program_text)
    symbol_table = SymbolTable(KEYWORDS)
    error_handler = ErrorHandler()
    token_repository = TokenRepository()
    tokenizer = Tokenizer(buffer, token_repository, error_handler, symbol_table)
    while buffer.has_next():
        tokenizer.get_next_token()

    write_tokens(token_repository)
    write_lexical_errors(error_handler)
    write_symbol_table(symbol_table)


# test
if __name__ == '__main__':
    main()