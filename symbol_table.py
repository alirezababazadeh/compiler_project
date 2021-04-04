class SymbolTable:
    def __init__(self, keywords):
        self.table = list()
        self.tokens = set()
        for keyword in keywords:
            self.add_lexeme_if_absent(keyword)

    def add_lexeme_if_absent(self, token):
        if token in self.tokens:
            return
        lexeme = Lexeme(len(self.table) + 1, token)
        self.table.append(lexeme)
        self.tokens.add(token)

    def __str__(self):
        output = "".join(f"{lexeme.index}.\t{lexeme.name}\n" for lexeme in self.table)
        output = output[:-1]
        return output


class Lexeme:
    def __init__(self, index, name):
        self.index = index
        self.name = name

    def __repr__(self):
        return f"{self.index}: {self.name}"
