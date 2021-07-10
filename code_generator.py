import os

from buffer import Buffer
from memory_manager import MemoryManager
from semantic_analyzer import SemanticAnalyzer
from symbol_table import SymbolTable


class CodeGenerator:
    def __init__(self, symbol_table: SymbolTable, memory_manager: MemoryManager, buffer: Buffer,
                 semantic_analyzer: SemanticAnalyzer):
        self.semantic_analyzer = semantic_analyzer
        self.buffer = buffer
        self.memory_manager = memory_manager
        self.symbol_table = symbol_table
        self.semantic_stack = []
        self.program_block = []
        self.output_enable = False
        self.main_jump = None

    def get_temp(self):
        return self.memory_manager.get_temp_address()

    def get_new_data_address(self):
        return self.memory_manager.get_new_data_address()

    def generate_code(self, action_symbol, *args):
        if action_symbol == 'ptype':
            self.semantic_stack.append(args[0])

        elif action_symbol == 'pid':
            lexeme = self.symbol_table.get_lexeme(self.symbol_table.get_current_scope(), args[0])
            if args[0] == "output":
                self.output_enable = True
            elif lexeme is None or not lexeme.is_declared:
                self.semantic_analyzer.report_error('notDefined', self.buffer.line_number)
                new_address = self.memory_manager.get_new_data_address()
                self.semantic_stack.append(new_address)
            elif lexeme.address is not None:
                if self.semantic_stack[-1] == 'neg':
                    self.semantic_stack.pop()
                    temp_address = self.get_temp()
                    self.semantic_stack.append(f'{temp_address}')
                    self.program_block.append(f'(SUB, #0, {lexeme.address}, {temp_address})')
                else:
                    self.semantic_stack.append(lexeme.address)

        elif action_symbol == 'pop':
            self.semantic_stack.pop()

        elif action_symbol == 'pnum':
            if self.semantic_stack[-1] == 'neg':
                self.semantic_stack.pop()
                self.semantic_stack.append(f'#-{args[0]}')
            else:
                self.semantic_stack.append(f'#{args[0]}')

        elif action_symbol == 'declare_array':
            count = int(self.semantic_stack.pop()[1:])
            address = self.semantic_stack.pop()
            lexeme = self.symbol_table.get_lexeme_by_address(address)
            lexeme.array_length = count
            for i in range(count - 1):
                address = self.get_new_data_address()
                self.program_block.append(f'(ASSIGN, #0, {address}, )')

            new_address = self.get_new_data_address()
            self.program_block.append(f'(ASSIGN, #{address}, {new_address}, )')

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
            self.program_block[self.semantic_stack.pop()] = f'(JP, {len(self.program_block)}, , )'

        elif action_symbol == 'assign':
            right = self.semantic_stack.pop()
            left = self.semantic_stack.pop()
            self.program_block.append(f'(ASSIGN, {right}, {left}, )')
            self.semantic_stack.append(left)

        elif action_symbol == 'array_usage':
            temp_address = self.get_temp()
            index = self.semantic_stack.pop()
            address = self.semantic_stack.pop()
            self.program_block.append(f'(MULT, {index}, #4, {temp_address})')
            self.program_block.append(f'(ADD, #{address}, {temp_address}, {temp_address})')
            self.semantic_stack.append(f'@{temp_address}')

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

        elif action_symbol == 'mult':
            op2 = self.semantic_stack.pop()
            op1 = self.semantic_stack.pop()
            temp_address = self.get_temp()
            self.program_block.append(f'(MULT, {op1}, {op2}, {temp_address})')
            self.semantic_stack.append(temp_address)

        elif action_symbol == 'EOP':
            lexeme = self.symbol_table.get_lexeme(self.symbol_table.get_current_scope(), 'main')
            self.program_block[
                lexeme.program_block_start] = f'(ASSIGN, #{len(self.program_block)}, {lexeme.return_address}, )'

        elif action_symbol == 'func_start':
            if self.main_jump is None:
                self.main_jump = len(self.program_block)
                self.program_block.append('')
            address = self.semantic_stack[-1]
            lexeme = self.symbol_table.get_lexeme_by_address(address)
            if lexeme.name == 'main':
                self.program_block[self.main_jump] = f'(JP, {len(self.program_block)}, , )'
                lexeme.program_block_start = len(self.program_block)
                self.program_block.append('')
            self.semantic_stack.append(lexeme.name)
            self.semantic_stack.append('func_start')
            self.symbol_table.start_scope()
            self.symbol_table.func_to_set_params = lexeme
            return_address = self.get_temp()
            return_value = self.get_temp()
            lexeme.return_value = return_value
            lexeme.return_address = return_address

        elif action_symbol == 'func_def':
            func_start_req = self.semantic_stack.pop()
            if not func_start_req:
                return
            func_name = self.semantic_stack.pop()
            lexeme = self.symbol_table.get_lexeme(self.symbol_table.get_current_scope() - 1, func_name)
            lexeme.start_address = len(self.program_block)
            self.symbol_table.func_to_set_params = None
        elif action_symbol == 'declare':
            lexeme = self.symbol_table.get_lexeme(self.symbol_table.get_current_scope(), args[0])
            address = self.get_new_data_address()
            lexeme.update_lexeme(address, self.semantic_stack.pop(), True)
            self.program_block.append(f'(ASSIGN, #0, {address}, )')
            self.semantic_stack.append(address)

        elif action_symbol == 'loop_break':
            self.program_block.append(f'(JP, {len(self.program_block) + 2}, , )')
            self.program_block.append('')
            self.semantic_stack.append(len(self.program_block) - 1)
        elif action_symbol == 'push_op':
            assert args[0] in ['<', '==', '+', '-']
            self.semantic_stack.append(args[0])
        elif action_symbol == 'declare_param':
            if self.semantic_stack[-1] == "func_start":
                return
            address = self.semantic_stack.pop()
            lexeme = self.symbol_table.get_lexeme_by_address(address)
            lexeme.is_param = True
        elif action_symbol == 'start_func_call':
            self.semantic_stack.append('start_func_call')
        elif action_symbol == 'end_func_call':
            func_body_vars = []
            item = self.semantic_stack.pop()
            while item != "start_func_call":
                func_body_vars.insert(0, item)
                item = self.semantic_stack.pop()
            if self.output_enable:
                result = func_body_vars[-1]
                self.program_block.append(f'(PRINT, {result}, , )')
                self.output_enable = False
                self.semantic_stack.append('')
                return
            func_addr = self.semantic_stack.pop()
            lexeme = self.symbol_table.get_lexeme_by_address(func_addr)
            if len(lexeme.func_params) // 2 != len(func_body_vars):
                self.semantic_analyzer.report_error('argumentCountMismatch', self.buffer.line_number, lexeme.name)
            params_count = min(len(lexeme.func_params) // 2, len(func_body_vars))

            for i in range(params_count):
                if (str.isnumeric(str(func_body_vars[i])) and func_body_vars[
                    i] >= self.memory_manager.initial_temp_pointer) \
                        or '#' in str(func_body_vars[i]) or '@' in str(func_body_vars[i]):
                    arg_name = ''
                    arg_data_type = 'var'
                else:
                    lexeme = self.symbol_table.get_lexeme_by_address(func_body_vars[i])
                    arg_name = lexeme.name
                    arg_data_type = lexeme.data_type
                if lexeme.func_params[i * 2 + 1].is_param:
                    if arg_data_type not in ['var', 'parameter']:
                        self.semantic_analyzer.report_error('argumentTypeMismatch', self.buffer.line_number,
                                                            len(self.program_block) + 1, lexeme.name, "int", "array")
                    self.program_block.append(
                        f'(ASSIGN, {func_body_vars[i]}, {lexeme.func_params[2 * i + 1].address}, )')
                else:
                    if arg_data_type not in ['array', 'param_array']:
                        self.semantic_analyzer.report_error('argumentTypeMismatch', self.buffer.line_number,
                                                            len(self.program_block) + 1, lexeme.func_params[i].name,
                                                            "array", "int")
                    if arg_name != '':
                        arr_len = self.symbol_table.get_lexeme(self.symbol_table.get_current_scope(), arg_name)
                        self.program_block.append(
                            f'(ASSIGN, {func_body_vars[i] + arr_len * 4}, {lexeme.func_params[i].address}, )')

            start_address = lexeme.start_address
            return_addr = lexeme.return_address
            return_value = lexeme.return_value
            self.program_block.append(f'(ASSIGN, #{len(self.program_block) + 2}, {return_addr}, )')
            self.program_block.append(f'(JP, {start_address}, , )')
            temp_value = self.get_temp()
            self.program_block.append(f'(ASSIGN, {return_value}, {temp_value}, )')
            self.semantic_stack.append(temp_value)
        elif action_symbol == 'return':
            lexeme = self.symbol_table.get_lexeme_by_index(self.symbol_table.scope_stack[-1])
            return_value = lexeme.return_value
            return_addr = lexeme.return_address
            value = self.semantic_stack.pop()
            self.program_block.append(f'(ASSIGN, {value}, {return_value}, )')
            self.program_block.append(f'(JP, @{return_addr}, , )')
        elif action_symbol == 'func_end':
            lexeme = self.symbol_table.get_lexeme_by_index(self.symbol_table.scope_stack[-1])
            return_value = lexeme.return_value
            return_addr = lexeme.return_address
            self.program_block.append(f'(ASSIGN, #0, {return_value}, )')
            self.program_block.append(f'(JP, @{return_addr}, , )')
            self.symbol_table.end_scope()
        elif action_symbol == 'neg_fac':
            assert args[0] == '-'
            self.semantic_stack.append('neg')
        elif action_symbol == 'param_array':
            address = self.semantic_stack.pop()
            lexeme = self.symbol_table.get_lexeme_by_address(address)
            lexeme.data_type = 'array'
        elif action_symbol == 'break':
            self.program_block.append(f'(JP, {self.semantic_stack[-1]}, ,)')

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
