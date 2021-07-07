from buffer import Buffer
from consts import KEYWORDS
from error_handler import LexicalErrorHandler
from grammar import Grammar
from parser_repo import ProcedureRepository, Parser
from procedures import PROCEDURES, START, TERMINALS
from scanner import Tokenizer
from symbol_table import SymbolTable
from token_repo import TokenRepository


def main(program_text, output_dir_path):
    buffer = Buffer(program_text)
    symbol_table = SymbolTable()
    error_handler = LexicalErrorHandler()
    token_repository = TokenRepository()
    tokenizer = Tokenizer(buffer, token_repository, error_handler, symbol_table)
    grammar = Grammar(START, PROCEDURES, TERMINALS)
    procedure_repo = ProcedureRepository(tokenizer, grammar)
    parser = Parser(procedure_repo, generate_parse_tree=False, generate_code=True, generate_syntax_error=False)
    parser.parse(f"{output_dir_path}/parse_tree.txt", f"{output_dir_path}/syntax_errors.txt",
                 f"{output_dir_path}/code_gen.txt")


output_dir = 'output/Phase3-CodeGeneratorTests/'
input_dir = 'test/resources/Phase4-SemanticAnalyzerTests'

if __name__ == '__main__':
    i = 1
    result = []
    while i < 11:
        input_test_sub_path = f"T{i}"
        path = f"{input_dir}/{input_test_sub_path}/input.txt"
        input_text = open(path).read()
        main(input_text, f"{output_dir}/T{i}")
        i += 1
    print(result)
