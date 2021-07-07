class SymbolTable:
    def __init__(self, keywords=None):
        if keywords is None:
            keywords = []
        self.tokens = dict()
        self.scope_stack = [0]
        for keyword in keywords:
            self.add_lexeme_if_absent(keyword)

    def add_lexeme_if_absent(self, token):
        scope = self.scope_stack[-1]
        if (scope, token) in self.tokens.keys():
            return
        lexeme = Lexeme(len(self.tokens) + 1, token, scope)
        self.tokens[(scope, token)] = lexeme

    def get_lexeme(self, scope, token_str):
        return self.tokens[(scope, token_str)]

    def contains(self, scope, token_str):
        return (scope, token_str) in self.tokens.keys()

    def __str__(self):
        output = "".join(f"{lexeme.index}.\t{lexeme.name}\n" for lexeme in self.tokens.values())
        output = output[:-1]
        return output

    def start_scope(self):
        self.scope_stack.append(len(self.tokens))

    def end_scope(self):
        current_scope = self.scope_stack.pop()
        for item in self.tokens.keys():
            if self.tokens[item].index >= current_scope:
                self.tokens.pop(item)

    def get_current_scope(self):
        return len(self.scope_stack) - 1


class Lexeme:
    def __init__(self, index, name, scope):
        self.index = index
        self.name = name
        self.address = None
        self.data_type = None
        self.is_declared = False
        self.scope = scope
        # self.parameters
        # self.arraysize

    def update_lexeme(self, address, data_type, is_declare=None):
        self.address = address
        self.data_type = data_type
        self.is_declared = self.is_declared if is_declare is None else is_declare

    def __repr__(self):
        return f"{self.index}: {self.name}"
