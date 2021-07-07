import os

from memory_manager import MemoryManager
from symbol_table import SymbolTable


class CodeGenerator:
    def __init__(self, symbol_table: SymbolTable, memory_manager: MemoryManager):
        self.memory_manager = memory_manager
        self.symbol_table = symbol_table
        self.semantic_stack = []
        self.program_block = []

    def get_temp(self):
        return self.memory_manager.get_temp_address()

    def get_new_data_address(self):
        return self.memory_manager.get_new_data_address()

    def generate_code(self, action_symbol, *args):
        if action_symbol == 'ptype':
            self.semantic_stack.append(args[0])

        elif action_symbol == 'pid':
            if args[0] != 'finish':
                lexeme = self.symbol_table.get_lexeme(self.symbol_table.get_current_scope(), args[0])
                address = self.get_new_data_address()
                if lexeme.data_type is None:
                    lexeme.update_lexeme(address, self.semantic_stack.pop())
                    self.program_block.append(f'(ASSIGN, #0, {address}, )')
                    self.semantic_stack.append(address)
                else:
                    self.semantic_stack.append(lexeme.address)

        elif action_symbol == 'pop':
            self.semantic_stack.pop()

        elif action_symbol == 'pnum':
            self.semantic_stack.append('#' + args[0])

        elif action_symbol == 'declare_array':
            count = int(self.semantic_stack.pop()[1:])
            self.semantic_stack.pop()
            for i in range(count - 1):
                address = self.get_new_data_address()
                self.program_block.append(f'(ASSIGN, #0, {address}, )')

        elif action_symbol == 'save':
            self.semantic_stack.append(len(self.program_block))
            self.program_block.append('')

        elif action_symbol == 'jpf_save':
            index = self.semantic_stack.pop()
            self.program_block[index] = f'(JPF, {self.semantic_stack.pop()}, {len(self.program_block) + 1}, )'
            self.semantic_stack.append(len(self.program_block))
            self.program_block.append('')

        elif action_symbol == 'jp':
            self.program_block[self.semantic_stack.pop()] = f'(JP, {len(self.program_block)}, , )'

        elif action_symbol == 'label':
            self.semantic_stack.append(len(self.program_block))

        elif action_symbol == 'while':
            index = self.semantic_stack.pop()
            self.program_block[index] = f'(JPF, {self.semantic_stack.pop()}, {len(self.program_block) + 1}, )'
            self.program_block.append(f'(JP, {self.semantic_stack.pop()}, , )')

        elif action_symbol == 'assign':
            left = self.semantic_stack.pop()
            right = self.semantic_stack.pop()
            self.program_block.append(f'(ASSIGN, {left}, {right}, )')
            self.semantic_stack.append(right)

        elif action_symbol == 'array_usage':
            temp_address = self.get_temp()
            index = self.semantic_stack.pop()
            id = self.semantic_stack.pop()

            self.program_block.append(f'(MULT, {index}, #4, {temp_address})')
            self.program_block.append(f'(ADD, #{id}, {temp_address}, {temp_address})')
            self.semantic_stack.append('@' + str(temp_address))

        elif action_symbol == 'relop':
            op2 = self.semantic_stack.pop()
            operator = self.semantic_stack.pop()
            op1 = self.semantic_stack.pop()

            temp_address = self.get_temp()
            self.semantic_stack.append(temp_address)

            if operator == '<':
                self.program_block.append(f'(LT, {op1}, {op2}, {temp_address})')
            elif operator == '==':
                self.program_block.append(f'(EQ, {op1}, {op2}, {temp_address})')

        elif action_symbol == 'add_or_sub':
            op2 = self.semantic_stack.pop()
            operator = self.semantic_stack.pop()
            op1 = self.semantic_stack.pop()

            temp_address = self.get_temp()
            if operator == '+':
                self.program_block.append(f'(ADD, {op1}, {op2}, {temp_address})')
            elif operator == '-':
                self.program_block.append(f'(SUB, {op1}, {op2}, {temp_address})')
            self.semantic_stack.append(temp_address)

            # op = self.semantic_stack.pop()
            # temp_address = self.get_temp()
            #
            # self.program_block.append(f'(SUB, #0, {op}, {temp_address})')
            # self.semantic_stack.append(temp_address)

        elif action_symbol == 'mult':
            op2 = self.semantic_stack.pop()
            op1 = self.semantic_stack.pop()

            temp_address = self.get_temp()
            self.program_block.append(f'(MULT, {op1}, {op2}, {temp_address})')
            self.semantic_stack.append(temp_address)

        elif action_symbol == 'EOP':
            address = self.semantic_stack.pop()
            self.program_block.append(f'(PRINT, {address}, , )')
            self.semantic_stack.append(None)
        elif action_symbol == 'func_start':
            pass
        elif action_symbol == 'func_def':
            pass
        elif action_symbol == 'declare':
            pass
        elif action_symbol == 'iteration_break':
            pass
        elif action_symbol == 'push_op':
            pass
        elif action_symbol == 'declare_param':
            pass
        elif action_symbol == 'start_func_call':
            pass
        elif action_symbol == 'end_func_call':
            pass
        elif action_symbol == 'return':
            pass

        else:
            print(action_symbol)
            exit()

    def write_to_file(self, address):
        output = self.get_result()
        os.makedirs(os.path.dirname(address), exist_ok=True)
        open(f'{address}', 'w').write(output)

    def get_result(self):
        output = ''
        for i, program in enumerate(self.program_block):
            output += f'{i}\t{program}\n'
        output = output[:-1]
        return output
