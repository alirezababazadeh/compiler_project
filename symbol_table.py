class SymbolTable:
    def __init__(self, keywords):
        self.tokens = dict()
        self.data_pointer = 100
        # for keyword in keywords:
        #     self.add_lexeme_if_absent(keyword)

    def add_lexeme_if_absent(self, token):
        if token in self.tokens.keys():
            return
        lexeme = Lexeme(len(self.tokens) + 1, token, self.data_pointer)
        self.tokens[token] = lexeme
        self.data_pointer += 4

    def get_lexeme(self, token_str):
        return self.tokens[token_str]

    def __str__(self):
        output = "".join(f"{lexeme.index}.\t{lexeme.name}\n" for token, lexeme in self.tokens)
        output = output[:-1]
        return output


class Lexeme:
    def __init__(self, index, name, address, type_=None):
        self.index = index
        self.name = name
        self.address = address
        self.type_ = type_

    def update_lexeme(self, address, type_):
        self.address = address
        self.type_ = type_

    def __repr__(self):
        return f"{self.index}: {self.name}"
