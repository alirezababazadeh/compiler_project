import os

from buffer import Buffer
from compiler import ProcedureRepository, Parser
from consts import KEYWORDS
from error_handler import LexicalErrorHandler
from grammar import Grammar
from procedures import START, PROCEDURES, TERMINALS
from scanner import Tokenizer
from symbol_table import SymbolTable
from token_repo import TokenRepository
from tree import TreeRenderer

dir_path = os.path.join(os.path.dirname(__file__))

common_input_dir = f'{dir_path}/resources/Phase2-ParserTests'


def run_parser(program_text):
    buffer = Buffer(program_text)
    symbol_table = SymbolTable(KEYWORDS)
    error_handler = LexicalErrorHandler()
    token_repository = TokenRepository()
    tokenizer = Tokenizer(buffer, token_repository, error_handler, symbol_table)
    grammar = Grammar(START, PROCEDURES, TERMINALS)
    procedure_repo = ProcedureRepository(tokenizer, grammar)
    parser = Parser(procedure_repo, False, False, False)
    parser.parse(None, None, None)
    return procedure_repo


def test_1():
    current_test_dir = f"{common_input_dir}/T1"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    actual_output = TreeRenderer(procedure_repo.tree_generator.tree).get_tree()
    open(f"{dir_path}/temp_tree.txt", "w", encoding="utf-8").write(actual_output)
    assert open(f"{dir_path}/temp_tree.txt", 'r', encoding="utf-8").read().rstrip() == open(
        f'{current_test_dir}/parse_tree.txt',
        encoding="utf-8").read().rstrip()
    assert str(procedure_repo.error_handler) == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()


def test_2():
    current_test_dir = f"{common_input_dir}/T2"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    actual_output = TreeRenderer(procedure_repo.tree_generator.tree).get_tree()
    open(f"{dir_path}/temp_tree.txt", "w", encoding="utf-8").write(actual_output)
    assert open(f"{dir_path}/temp_tree.txt", 'r', encoding="utf-8").read().rstrip() == open(
        f'{current_test_dir}/parse_tree.txt',
        encoding="utf-8").read().rstrip()
    assert str(procedure_repo.error_handler) == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()


def test_3():
    current_test_dir = f"{common_input_dir}/T3"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    actual_output = TreeRenderer(procedure_repo.tree_generator.tree).get_tree()
    open(f"{dir_path}/temp_tree.txt", "w", encoding="utf-8").write(actual_output)
    assert open(f"{dir_path}/temp_tree.txt", 'r', encoding="utf-8").read().rstrip() == open(
        f'{current_test_dir}/parse_tree.txt',
        encoding="utf-8").read().rstrip()
    assert str(procedure_repo.error_handler) == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()


def test_4():
    current_test_dir = f"{common_input_dir}/T4"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    actual_output = TreeRenderer(procedure_repo.tree_generator.tree).get_tree()
    open(f"{dir_path}/temp_tree.txt", "w", encoding="utf-8").write(actual_output)
    assert open(f"{dir_path}/temp_tree.txt", 'r', encoding="utf-8").read().rstrip() == open(
        f'{current_test_dir}/parse_tree.txt',
        encoding="utf-8").read().rstrip()
    assert str(procedure_repo.error_handler).rstrip() == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()


def test_5():
    current_test_dir = f"{common_input_dir}/T5"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    actual_output = TreeRenderer(procedure_repo.tree_generator.tree).get_tree()
    open(f"{dir_path}/temp_tree.txt", "w", encoding="utf-8").write(actual_output)
    assert open(f"{dir_path}/temp_tree.txt", 'r', encoding="utf-8").read().rstrip() == open(
        f'{current_test_dir}/parse_tree.txt',
        encoding="utf-8").read().rstrip()
    assert str(procedure_repo.error_handler).rstrip() == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()


def test_6():
    current_test_dir = f"{common_input_dir}/T6"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    actual_output = TreeRenderer(procedure_repo.tree_generator.tree).get_tree()
    open(f"{dir_path}/temp_tree.txt", "w", encoding="utf-8").write(actual_output)
    assert open(f"{dir_path}/temp_tree.txt", 'r', encoding="utf-8").read().rstrip() == open(
        f'{current_test_dir}/parse_tree.txt',
        encoding="utf-8").read().rstrip()
    assert str(procedure_repo.error_handler).strip() == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()


def test_7():
    current_test_dir = f"{common_input_dir}/T7"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    actual_output = TreeRenderer(procedure_repo.tree_generator.tree).get_tree()
    open(f"{dir_path}/temp_tree.txt", "w", encoding="utf-8").write(actual_output)
    assert open(f"{dir_path}/temp_tree.txt", 'r', encoding="utf-8").read().rstrip() == open(
        f'{current_test_dir}/parse_tree.txt',
        encoding="utf-8").read().rstrip()
    assert str(procedure_repo.error_handler).strip() == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()


def test_8():
    current_test_dir = f"{common_input_dir}/T8"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    actual_output = TreeRenderer(procedure_repo.tree_generator.tree).get_tree()
    open(f"{dir_path}/temp_tree.txt", "w", encoding="utf-8").write(actual_output)
    assert open(f"{dir_path}/temp_tree.txt", 'r', encoding="utf-8").read().rstrip() == open(
        f'{current_test_dir}/parse_tree.txt',
        encoding="utf-8").read().rstrip()
    assert str(procedure_repo.error_handler).strip() == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()


def test_9():
    current_test_dir = f"{common_input_dir}/T9"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    actual_output = TreeRenderer(procedure_repo.tree_generator.tree).get_tree()
    open(f"{dir_path}/temp_tree.txt", "w", encoding="utf-8").write(actual_output)
    assert open(f"{dir_path}/temp_tree.txt", 'r', encoding="utf-8").read().rstrip() == open(
        f'{current_test_dir}/parse_tree.txt',
        encoding="utf-8").read().rstrip()
    assert str(procedure_repo.error_handler).strip() == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()


def test_10():
    current_test_dir = f"{common_input_dir}/T10"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    actual_output = TreeRenderer(procedure_repo.tree_generator.tree).get_tree()
    open(f"{dir_path}/temp_tree.txt", "w", encoding="utf-8").write(actual_output)
    assert open(f"{dir_path}/temp_tree.txt", 'r', encoding="utf-8").read().rstrip() == open(
        f'{current_test_dir}/parse_tree.txt',
        encoding="utf-8").read().rstrip()
    assert str(procedure_repo.error_handler).strip() == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()
