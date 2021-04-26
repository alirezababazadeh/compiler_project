from buffer import Buffer
from compiler import Tokenizer
from consts import EPSILON, KEYWORDS
from error_handler import ErrorHandler
from symbol_table import SymbolTable
from token_repo import TokenRepository


class Parser:
    def __init__(self, procedure_repository):
        self.procedure_repository = procedure_repository

    def parse(self):
        self.procedure_repository.run_procedure(self.procedure_repository.start)
        print(self.procedure_repository.tree)


class Procedure:
    def __init__(self, name, production_rules, follow):
        self.name = name
        self.production_rules = production_rules
        self.follow = follow


class ProductionRule:
    def __init__(self, first, sentence):
        self.first = first
        self.sentence = sentence


class ProcedureRepository:
    def __init__(self, procedures, start, terminals, tokenizer, flat_tree):
        self.procedures = procedures
        self.start = start
        self.tokenizer = tokenizer
        self.terminals = terminals
        self.lookahead = tokenizer.get_next_token()
        self.tree = flat_tree
        self.temp_tree = []

    def run_procedure(self, procedure):
        self.temp_tree.append(procedure.name)
        for production_rule in procedure.production_rules:
            if self.lookahead in production_rule.first:
                for alphabet in production_rule.sentence:
                    if alphabet in self.terminals:
                        self.match(production_rule.first)
                    else:
                        self.run_procedure(self.procedures[alphabet])
            elif self.lookahead in production_rule.follow:
                if EPSILON not in production_rule.follow:
                    print(f'missing {procedure.name} on line {self.lookahead.line_no}')
            else:
                print(f'illegal lookahead on line {self.lookahead.line_no}')
                self.lookahead = self.tokenizer.get_next_token()
                self.run_procedure(procedure)
        self.temp_tree.pop()

    def match(self, expected_tokens):
        if self.lookahead in expected_tokens:
            self.lookahead = self.tokenizer.get_next_token()
            self.tree.add_node(self.temp_tree)
        else:
            print(f'missing expected_token on line {self.lookahead.line_no}')


output_path = ''
input_path = 'input.txt'


def main():
    program_text = open(input_path).read()

    buffer = Buffer(program_text)
    symbol_table = SymbolTable(KEYWORDS)
    error_handler = ErrorHandler()
    token_repository = TokenRepository()
    tokenizer = Tokenizer(buffer, token_repository, error_handler, symbol_table)
    procedure_repo = ProcedureRepository()
    parser = Parser()


if __name__ == '__main__':
    main()
