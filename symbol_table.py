class SymbolTable:
    def __init__(self, keywords=None):
        if keywords is None:
            keywords = []
        self.tokens = dict()
        self.scope_stack = list()
        self.data_pointer = 100
        for keyword in keywords:
            self.add_lexeme_if_absent(keyword)

    def add_lexeme_if_absent(self, token):
        if token in self.tokens.keys():
            return
        lexeme = Lexeme(len(self.tokens) + 1, token, self.data_pointer)
        self.tokens[token] = lexeme
        self.data_pointer += 4

    def get_lexeme(self, token_str):
        return self.tokens[token_str]

    def contains(self, token_str):
        return token_str in self.tokens.keys()

    def __str__(self):
        output = "".join(f"{lexeme.index}.\t{lexeme.name}\n" for lexeme in self.tokens.values())
        output = output[:-1]
        return output

    def start_scope(self):
        self.scope_stack.append([])

    def end_scope(self):
        current_scope = self.scope_stack.pop()
        for token in current_scope:
            self.tokens.pop(token, None)


class Lexeme:
    def __init__(self, index, name, address, data_type=None):
        self.index = index
        self.name = name
        self.address = address
        self.data_type = data_type

    def update_lexeme(self, address, data_type):
        self.address = address
        self.data_type = data_type

    def __repr__(self):
        return f"{self.index}: {self.name}"
