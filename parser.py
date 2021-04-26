from compiler import Tokenizer
from consts import EPSILON


class Parser:
    def __init__(self, tokenizer, procedure_repository):
        self.tokenizer = tokenizer
        self.procedure_repository = procedure_repository

    def parse(self):
        lookahead = self.tokenizer.get_next_token()
        self.procedure_repository.run_procedure(self.procedure_repository.start)


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
    def __init__(self, procedures, start, terminals, tokenizer):
        self.procedures = procedures
        self.start = start
        self.tokenizer = tokenizer
        self.terminals = terminals
        self.lookahead = tokenizer.get_next_token()

    def run_procedure(self, procedure):
        for production_rule in procedure.production_rules:
            if self.lookahead in production_rule.first:
                for alphabet in production_rule.sentence:
                    if alphabet in self.terminals:
                        self.match(production_rule.first)
                    else:
                        self.run_procedure(self.procedures[alphabet])
            elif self.lookahead in production_rule.follow:
                if EPSILON in production_rule.follow:
                    return
                else:
                    print(f'missing {procedure.name} on line {self.lookahead.line_no}')
            else:
                print(f'illegal lookahead on line {self.lookahead.line_no}')
                self.lookahead = self.tokenizer.get_next_token()
                self.run_procedure(procedure)

    def match(self, expected_tokens):
        if self.lookahead in expected_tokens:
            self.lookahead = self.tokenizer.get_next_token()
        else:
            print(f'missing expected_token on line {self.lookahead.line_no}')
