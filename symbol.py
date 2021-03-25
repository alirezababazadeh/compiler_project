symbol_table = list()
STARTED_ID_INDEX = 12


class Lexeme:
    def __repr__(self):
        return f"{self.index}: {self.name}"

    @staticmethod
    def create_lexeme(name):
        global symbol_table
        instance = Lexeme()
        instance.index = len(symbol_table) + 1
        instance.name = name
        return instance


def create_basic_symbol_table():
    basic_symbols_names = ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'for']
    global symbol_table
    for name in basic_symbols_names:
        symbol_table.append(Lexeme.create_lexeme(name))
