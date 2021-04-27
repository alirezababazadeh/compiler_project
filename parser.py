from buffer import Buffer
from compiler import Tokenizer
from consts import EPSILON, KEYWORDS
from error_handler import ErrorHandler
from procedures import PROCEDURES, START, TERMINALS, Procedure, ProductionRule
from symbol_table import SymbolTable
from token_repo import TokenRepository
from tree import FlatTree, tree_render, fold


class Parser:
    def __init__(self, procedure_repository):
        self.procedure_repository = procedure_repository

    def parse(self):
        self.procedure_repository.run_procedure(self.procedure_repository.start)
        tree_render(fold(self.procedure_repository.tree.tree))


class ProcedureRepository:
    def __init__(self, tokenizer, procedures, start_name, terminals):
        self.procedures = procedures
        self.start = start_name
        self.tokenizer = tokenizer
        self.terminals = terminals
        self.lookahead = tokenizer.get_next_token()
        self.tree = FlatTree()
        self.temp_tree = []

    def run_procedure(self, procedure_name):
        procedure = self.procedures[procedure_name]
        self.temp_tree.append(procedure.name)
        has_matched = False
        for production_rule in procedure.production_rules:
            if self.lookahead[1] in production_rule.first:
                has_matched = True
                for alphabet in production_rule.sentence:
                    if alphabet in self.terminals:
                        self.match(production_rule.first)
                    else:
                        self.run_procedure(self.procedures[alphabet].name)
        if not has_matched:
            if self.lookahead[1] in procedure.follow:
                if not procedure.has_epsilon_in_first:
                    print(f'missing {procedure.name} on line {self.tokenizer.buffer.line_number}')
            else:
                print(f'illegal lookahead on line {self.tokenizer.buffer.line_number}')
                self.lookahead = self.tokenizer.get_next_token()
                self.run_procedure(procedure.name)
        self.temp_tree.pop()

    def match(self, expected_tokens):
        if self.lookahead[1] in expected_tokens:
            self.lookahead = self.tokenizer.get_next_token()
            self.tree.add_node(self.temp_tree.copy())
        else:
            print(f'missing expected_token on line {self.tokenizer.buffer.line_number}')


output_path = ''
input_path = 'input.txt'


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
