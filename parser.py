from compiler import Tokenizer


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse(self):
        lookahead = self.tokenizer.get_next_token()


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
    def __init__(self, procedures):
        self.procedures = procedures

    def run_procedure(self, procedure):
        pass

    def match(self):
        pass
