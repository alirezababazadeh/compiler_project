from symbol_table import SymbolTable


class CodeGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.semantic_stack = []
        self.program_block = []
        self.temp_pointer = 500
        self.semantic_routines = {'ptype': self.ptype,
                                  'pid': self.pid,
                                  'pop': self.pop,
                                  'pnum': self.pnum,
                                  'save_array': self.save_array,
                                  'save': self.save,
                                  'jpf_save': self.jpf_save,
                                  'jp': self.jp,
                                  'label': self.label,
                                  'while': self.iter,
                                  'assign': self.assign,
                                  'array_index': self.array_index,
                                  'poperator': self.poperator,
                                  'relop': self.relop,
                                  'addop': self.addop,
                                  'mult': self.mult,
                                  'neg': self.neg,
                                  'output': self.output
                                  }

    def find_address(self, token_input):
        return self.symbol_table.get_lexeme(token_input).address

    def get_temp(self):
        pointer = self.temp_pointer
        self.temp_pointer += 4
        return pointer

    def generate_code(self, action_symbol, args=None):
        self.semantic_routines[action_symbol](args)
