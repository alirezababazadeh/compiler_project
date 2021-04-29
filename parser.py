from buffer import Buffer
from scanner import Tokenizer
from consts import EPSILON, KEYWORDS
from error_handler import ErrorHandler
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


class ProcedureRepository:
    def __init__(self, tokenizer, procedures, start_name, terminals):
        self.procedures = procedures
        self.start = start_name
        self.tokenizer = tokenizer
        self.terminals = terminals
        self.lookahead = tokenizer.get_next_token()
        self.tree_generator = TreeGenerator()

    def run_procedure(self, procedure_name):
        procedure = self.procedures[procedure_name]
        self.tree_generator.add_node(procedure_name)
        has_matched = False
        for production_rule in procedure.production_rules:
            if (self.lookahead[1] in TERMINALS and self.lookahead[1] in production_rule.first) or \
                    self.lookahead[0] in production_rule.first:
                has_matched = True
                for alphabet in production_rule.sentence:
                    if alphabet in self.terminals:
                        self.match(alphabet)
                    else:
                        self.run_procedure(self.procedures[alphabet].name)
        if not has_matched:
            if (self.lookahead[1] in TERMINALS and self.lookahead[1] in procedure.follow) or \
                    self.lookahead[0] in procedure.follow:
                if not procedure.has_epsilon_in_first:
                    print(f'missing {procedure.name} on line {self.tokenizer.buffer.line_number}')
                else:
                    self.tree_generator.add_node("epsilon")
                    self.tree_generator.level_up()
            else:
                print(f'illegal lookahead on line {self.tokenizer.buffer.line_number}')
                self.lookahead = self.tokenizer.get_next_token()
                self.run_procedure(procedure.name)
        self.tree_generator.level_up()

    def match(self, expected_token):
        if (expected_token in TERMINALS and self.lookahead[1] == expected_token) or self.lookahead[0] == expected_token:
            self.tree_generator.add_node(f'({self.lookahead[0]}, {self.lookahead[1]}) ')
            self.tree_generator.level_up()
            self.lookahead = self.tokenizer.get_next_token()
        else:
            print(f'missing expected_token on line {self.tokenizer.buffer.line_number}')


output_path = ''
input_path = 'PA2_Resources/T7/input.txt'


def main():
    program_text = open(input_path).read()

    buffer = Buffer(program_text)
    symbol_table = SymbolTable(KEYWORDS)
    error_handler = ErrorHandler()
    token_repository = TokenRepository()
    tokenizer = Tokenizer(buffer, token_repository, error_handler, symbol_table)
    procedure_repo = ProcedureRepository(tokenizer, PROCEDURES, START, TERMINALS)
    parser = Parser(procedure_repo)
    parser.parse()


if __name__ == '__main__':
    main()
