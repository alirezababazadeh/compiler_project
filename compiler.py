from buffer import Buffer
from code_generator import CodeGenerator
from scanner import Tokenizer
from consts import EPSILON, KEYWORDS
from error_handler import LexicalErrorHandler, SyntaxErrorHandler
from procedures import PROCEDURES, START, TERMINALS, Procedure, ProductionRule
from symbol_table import SymbolTable
from token_repo import TokenRepository
from tree import Tree, InternalNode, TreeGenerator, TreeRenderer


class Parser:
    def __init__(self, procedure_repository):
        self.procedure_repository = procedure_repository

    def parse(self):
        self.procedure_repository.run_procedure(self.procedure_repository.start)
        TreeRenderer(self.procedure_repository.tree_generator.tree).write_to_file('parse_tree.txt')
        self.procedure_repository.error_handler.write_to_file('syntax_errors.txt')
        self.procedure_repository.code_generator.write_to_file('PA3_Resources/Tester/output.txt')


class ProcedureRepository:
    def __init__(self, tokenizer, procedures, start_name, terminals):
        self.procedures = procedures
        self.start = start_name
        self.tokenizer = tokenizer
        self.terminals = terminals
        self.lookahead = tokenizer.get_next_token()
        self.tree_generator = TreeGenerator()
        self.error_handler = SyntaxErrorHandler()
        self.EOP = False
        self.code_generator = CodeGenerator(self.tokenizer.symbol_table)

    def run_procedure(self, procedure_name):
        if self.lookahead[1] == '$' and self.EOP:
            return
        if self.lookahead[1] == ';' and procedure_name == 'Statement-list':
            print("Error")
        procedure = self.procedures[procedure_name]
        self.tree_generator.add_node(procedure_name)
        has_matched = False
        for production_rule in procedure.production_rules:
            if self.lookahead[1] in production_rule.first or self.lookahead[0] in production_rule.first:
                has_matched = True
                for alphabet in production_rule.sentence:
                    if alphabet.startswith("#"):
                        self.code_generator.generate_code(alphabet[1:], self.lookahead[1])
                    elif alphabet in self.terminals:
                        if self.lookahead[1] == '$' and self.EOP:
                            return
                        self.match(alphabet)
                    else:
                        if self.lookahead[1] == '$' and self.EOP:
                            return
                        self.run_procedure(self.procedures[alphabet].name)
            if has_matched:
                break
        if not has_matched:
            if self.lookahead[1] in procedure.follow or self.lookahead[0] in procedure.follow:
                if not procedure.has_epsilon_in_first:
                    self.tree_generator.delete_node()
                    self.error_handler.add_syntax_error(f"missing {procedure.name}", self.tokenizer.buffer.line_number)
                    return
                    # print(f'missing {procedure.name} on line {self.tokenizer.buffer.line_number}')
                else:
                    if procedure.has_epsilon_rule:
                        self.tree_generator.add_node("epsilon")
                        self.tree_generator.level_up()
                    else:
                        for production_rule in procedure.production_rules:
                            alphabet = production_rule.sentence[0]
                            if alphabet not in self.terminals and self.procedures[alphabet].has_epsilon_in_first:
                                for new_alphabet in production_rule.sentence:
                                    if self.lookahead[1] == '$' and self.EOP:
                                        return
                                    self.run_procedure(self.procedures[new_alphabet].name)
                                break
            else:
                self.tree_generator.delete_node()
                if self.lookahead[1] in TERMINALS:
                    if self.lookahead[1] == '$' and not self.EOP:
                        self.EOP = True
                        self.error_handler.add_syntax_error("unexpected EOF", self.tokenizer.buffer.line_number)
                        return
                    else:
                        self.error_handler.add_syntax_error(f"illegal {self.lookahead[1]}",
                                                            self.tokenizer.buffer.line_number)
                else:
                    self.error_handler.add_syntax_error(f"illegal {self.lookahead[0]}",
                                                        self.tokenizer.buffer.line_number)
                # print(f'illegal lookahead on line {self.tokenizer.buffer.line_number}')
                self.lookahead = self.tokenizer.get_next_token()
                if self.lookahead[1] == '$' and self.EOP:
                    return
                self.run_procedure(procedure.name)
                return
        self.tree_generator.level_up()

    def match(self, expected_token):
        if self.lookahead[1] == "$":
            self.tree_generator.add_node('$')
            self.tree_generator.level_up()
            self.lookahead = self.tokenizer.get_next_token()
        elif (expected_token in TERMINALS and self.lookahead[1] == expected_token) or \
                self.lookahead[0] == expected_token:
            self.tree_generator.add_node(f'({self.lookahead[0]}, {self.lookahead[1]}) ')
            self.tree_generator.level_up()
            self.lookahead = self.tokenizer.get_next_token()
        else:
            self.error_handler.add_syntax_error(f"missing {expected_token}", self.tokenizer.buffer.line_number)
            # print(f'missing expected_token on line {self.tokenizer.buffer.line_number}')


output_path = ''
input_path = 'PA3_Resources/T5/input.txt'


def main():
    program_text = open(input_path).read()

    buffer = Buffer(program_text)
    symbol_table = SymbolTable(KEYWORDS)
    error_handler = LexicalErrorHandler()
    token_repository = TokenRepository()
    tokenizer = Tokenizer(buffer, token_repository, error_handler, symbol_table)
    procedure_repo = ProcedureRepository(tokenizer, PROCEDURES, START, TERMINALS)
    parser = Parser(procedure_repo)
    parser.parse()


if __name__ == '__main__':
    main()
