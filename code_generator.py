from symbol_table import SymbolTable


class CodeGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.semantic_stack = []
        self.program_block = []
        self.data_cursor = 1000
        self.temp_cursor = 500
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
                                  'relop': self.relop,
                                  'addop': self.addop,
                                  'mult': self.mult,
                                  'sub': self.sub,
                                  'finish': self.finish
                                  }

    def get_temp(self):
        pointer = self.temp_cursor
        self.temp_cursor += 4
        return pointer

    def generate_code(self, action_symbol, *args):
        self.semantic_routines[action_symbol](*args)

    def write_to_file(self, address):
        output = ''
        for i, program in enumerate(self.program_block):
            output += f'{i}\t{program}\n'
        output = output[:-1]
        open(f'{address}', 'w').write(output)

    def ptype(self, *args):
        self.semantic_stack.append(args[0])

    def get_new_data_address(self):
        self.data_cursor += 4
        return self.data_cursor

    def pid(self, *args):
        if args[0] != 'finish':
            lexeme = self.symbol_table.get_lexeme(args[0])
            address = self.get_new_data_address()
            if lexeme.type is None:
                lexeme.update_lexeme(address, self.semantic_stack.pop())
                self.program_block.append(f'(ASSIGN, #0, {address}, )')
                self.semantic_stack.append(address)
            else:
                self.semantic_stack.append(lexeme.address)

    def pop(self, *args):
        self.semantic_stack.pop()

    def pnum(self, *args):
        self.semantic_stack.append('#' + args[0])

    def save_array(self, *args):
        count = int(self.semantic_stack.pop()[1:])
        self.pop()
        for i in range(count - 1):
            address = self.get_new_data_address()
            self.program_block.append(f'(ASSIGN, #0, {address}, )')

    def save(self, *args):
        self.semantic_stack.append(len(self.program_block))
        self.program_block.append('')

    def jpf_save(self, *args):
        index = self.semantic_stack.pop()
        self.program_block[index] = f'(JPF, {self.semantic_stack.pop()}, {len(self.program_block) + 1}, )'
        self.semantic_stack.append(len(self.program_block))
        self.program_block.append('')

    def jp(self, *args):
        self.program_block[self.semantic_stack.pop()] = f'(JP, {len(self.program_block)}, , )'

    def label(self, *args):
        self.semantic_stack.append(len(self.program_block))

    def iter(self, *args):
        index = self.semantic_stack.pop()
        self.program_block[index] = f'(JPF, {self.semantic_stack.pop()}, {len(self.program_block) + 1}, )'
        self.program_block.append(f'(JP, {self.semantic_stack.pop()}, , )')

    def assign(self, *args):
        left = self.semantic_stack.pop()
        right = self.semantic_stack.pop()
        self.program_block.append(f'(ASSIGN, {left}, {right}, )')
        self.semantic_stack.append(right)

    def array_index(self, *args):
        temp_address = self.get_temp()
        index = self.semantic_stack.pop()
        id = self.semantic_stack.pop()

        self.program_block.append(f'(MULT, {index}, #4, {temp_address})')
        self.program_block.append(f'(ADD, #{id}, {temp_address}, {temp_address})')
        self.semantic_stack.append('@' + str(temp_address))

    def relop(self, *args):
        op2 = self.semantic_stack.pop()
        operator = self.semantic_stack.pop()
        op1 = self.semantic_stack.pop()

        temp_address = self.get_temp()
        self.semantic_stack.append(temp_address)

        if operator == '<':
            self.program_block.append(f'(LT, {op1}, {op2}, {temp_address})')
        elif operator == '==':
            self.program_block.append(f'(EQ, {op1}, {op2}, {temp_address})')

    def addop(self, args=None):
        op2 = self.semantic_stack.pop()
        operator = self.semantic_stack.pop()
        op1 = self.semantic_stack.pop()

        temp_address = self.get_temp()
        if operator == '+':
            self.program_block.append(f'(ADD, {op1}, {op2}, {temp_address})')
        elif operator == '-':
            self.program_block.append(f'(SUB, {op1}, {op2}, {temp_address})')
        self.semantic_stack.append(temp_address)

    def mult(self, *args):
        op2 = self.semantic_stack.pop()
        op1 = self.semantic_stack.pop()

        temp_address = self.get_temp()
        self.program_block.append(f'(MULT, {op1}, {op2}, {temp_address})')
        self.semantic_stack.append(temp_address)

    def sub(self, *args):
        op = self.semantic_stack.pop()
        temp_address = self.get_temp()

        self.program_block.append(f'(SUB, #0, {op}, {temp_address})')
        self.semantic_stack.append(temp_address)

    def finish(self, *args):
        address = self.semantic_stack.pop()
        self.program_block.append(f'(PRINT, {address}, , )')
        self.semantic_stack.append(None)
