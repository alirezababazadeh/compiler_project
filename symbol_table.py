from consts import KEYWORDS


class SymbolTable:
    def __init__(self, keywords=None):
        if keywords is None:
            keywords = []
        self.tokens = dict()
        self.scope_stack = []
        for keyword in keywords:
            self.add_lexeme_if_absent(keyword)
        self.func_to_set_params = None

    def add_lexeme_if_absent(self, token):
        scope = len(self.scope_stack)
        if (scope, token) in self.tokens.keys():
            return
        lexeme = Lexeme(len(self.tokens) + 1, token, scope)
        if token in KEYWORDS:
            lexeme.data_type = 'keyword'
        for i in range(len(self.scope_stack)):
            if (i, lexeme.name) in self.tokens.keys():
                lexeme.address = self.tokens[(i, lexeme.name)].address
                lexeme.is_declared = self.tokens[(i, lexeme.name)].is_declared
                break
        self.tokens[(scope, token)] = lexeme
        if self.func_to_set_params is not None:
            self.func_to_set_params.func_params.append(lexeme)

    def get_lexeme(self, scope, token_str):
        while True:
            if (scope, token_str) in self.tokens.keys():
                return self.tokens[(scope, token_str)]
            if scope == 0:
                break
            scope -= 1
        return None

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
                del item

    def get_current_scope(self):
        return len(self.scope_stack)

    def get_lexeme_by_address(self, address):
        for lexeme in self.tokens.values():
            if lexeme.address == address:
                return lexeme

    def get_lexeme_by_index(self, index):
        for lexeme in self.tokens.values():
            if lexeme.index == index:
                return lexeme


class Lexeme:
    def __init__(self, index, name, scope):
        self.index = index
        self.name = name
        self.address = None
        self.data_type = None
        self.is_declared = False
        self.scope = scope
        self.func_params = []
        self.array_length = 0
        self.is_param = False

    def update_lexeme(self, address, data_type, is_declare=None):
        self.address = address
        self.data_type = data_type
        self.is_declared = self.is_declared if is_declare is None else is_declare

    def __repr__(self):
        return f"{self.index}: {self.name}"
