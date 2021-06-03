from symbol_table import SymbolTable


class CodeGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.semantic_stack = []
        self.program_block = []
        self.data_pointer = 1000 - 4
        self.temp_pointer = 500
        self.i = 0
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

    def write_to_file(self, address):
        log = ''
        for i, program in enumerate(self.program_block):
            log += f'{i}\t{program}\n'
        log = log[:-1]
        with open(f'output/{address}', 'w') as file:
            file.write(log)

    def ptype(self, arg=None):
        self.semantic_stack.append(arg)

    def get_data(self):
        self.data_pointer += 4
        return self.data_pointer

    def pid(self, arg=None):
        if arg in self.symbol_table:
            address = self.find_address(arg)
            self.semantic_stack.append(address)
        elif arg != 'output':
            address = self.get_data()
            self.symbol_table[arg] = {'address': address, 'type': self.semantic_stack.pop(), 'length': 0}
            self.program_block.append(f'(ASSIGN, #0, {address}, )')
            self.i += 1
            self.semantic_stack.append(address)

    def pop(self, arg=None):
        self.semantic_stack.pop()

    def pnum(self, arg=None):
        self.semantic_stack.append('#' + arg)

    def save_array(self, arg=None):
        number = int(self.semantic_stack.pop()[1:])
        id_address = self.semantic_stack.pop()
        # id = next((key for key, val in self.symbol_table.items() if val['address'] == id_address), None)
        # self.symbol_table[id]['length'] = number
        for i in range(number - 1):
            address = self.get_data()
            self.program_block.append(f'(ASSIGN, #0, {address}, )')
            self.i += 1

    def save(self, arg=None):
        self.semantic_stack.append(self.i)
        self.program_block.append('')
        self.i += 1

    def jpf_save(self, arg=None):
        index = self.semantic_stack.pop()
        self.program_block[index] = f'(JPF, {self.semantic_stack.pop()}, {self.i + 1}, )'
        self.semantic_stack.append(self.i)
        self.i += 1
        self.program_block.append('')

    def jp(self, arg=None):
        self.program_block[self.semantic_stack.pop()] = f'(JP, {self.i}, , )'

    def label(self, arg=None):
        self.semantic_stack.append(self.i)

    def iter(self, arg=None):
        index = self.semantic_stack.pop()
        self.program_block[index] = f'(JPF, {self.semantic_stack.pop()}, {self.i + 1}, )'
        self.program_block.append(f'(JP, {self.semantic_stack.pop()}, , )')
        self.i += 1

    def assign(self, arg=None):
        rhs = self.semantic_stack.pop()
        lhs = self.semantic_stack.pop()
        self.program_block.append(f'(ASSIGN, {rhs}, {lhs}, )')
        self.i += 1
        self.semantic_stack.append(lhs)

    def array_index(self, arg=None):
        temp_address = self.get_temp()
        index = self.semantic_stack.pop()
        id = self.semantic_stack.pop()
        self.program_block.append(f'(MULT, {index}, #4, {temp_address})')
        self.program_block.append(f'(ADD, #{id}, {temp_address}, {temp_address})')
        self.semantic_stack.append('@' + str(temp_address))
        self.i += 2

    def poperator(self, arg=None):
        self.semantic_stack.append(arg)

    def relop(self, arg=None):
        op2 = self.semantic_stack.pop()
        operator = self.semantic_stack.pop()
        op1 = self.semantic_stack.pop()

        temp_address = self.get_temp()
        if operator == '<':
            self.program_block.append(f'(LT, {op1}, {op2}, {temp_address})')
        elif operator == '==':
            self.program_block.append(f'(EQ, {op1}, {op2}, {temp_address})')
        self.i += 1
        self.semantic_stack.append(temp_address)

    def addop(self, arg=None):
        op2 = self.semantic_stack.pop()
        operator = self.semantic_stack.pop()
        op1 = self.semantic_stack.pop()

        temp_address = self.get_temp()
        if operator == '+':
            self.program_block.append(f'(ADD, {op1}, {op2}, {temp_address})')
        elif operator == '-':
            self.program_block.append(f'(SUB, {op1}, {op2}, {temp_address})')
        self.i += 1
        self.semantic_stack.append(temp_address)

    def mult(self, arg=None):
        op2 = self.semantic_stack.pop()
        op1 = self.semantic_stack.pop()

        temp_address = self.get_temp()
        self.program_block.append(f'(MULT, {op1}, {op2}, {temp_address})')
        self.i += 1
        self.semantic_stack.append(temp_address)

    def neg(self, arg=None):
        op = self.semantic_stack.pop()
        temp_address = self.get_temp()
        self.program_block.append(f'(SUB, #0, {op}, {temp_address})')
        self.i += 1
        self.semantic_stack.append(temp_address)

    def output(self, arg=None):
        id = self.semantic_stack.pop()
        self.program_block.append(f'(PRINT, {id}, , )')
        self.i += 1
        self.semantic_stack.append(None)
