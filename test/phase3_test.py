import os
import subprocess
import sys

from buffer import Buffer
from consts import KEYWORDS
from error_handler import LexicalErrorHandler
from grammar import Grammar
from parser_repo import ProcedureRepository, Parser
from procedures import START, PROCEDURES, TERMINALS
from scanner import Tokenizer
from symbol_table import SymbolTable
from token_repo import TokenRepository

dir_path = os.path.join(os.path.dirname(__file__))

common_input_dir = f'{dir_path}/resources/Phase3-CodeGeneratorTests'


def run_parser(program_text):
    buffer = Buffer(program_text)
    symbol_table = SymbolTable(KEYWORDS)
    error_handler = LexicalErrorHandler()
    token_repository = TokenRepository()
    tokenizer = Tokenizer(buffer, token_repository, error_handler, symbol_table)
    grammar = Grammar(START, PROCEDURES, TERMINALS)
    procedure_repo = ProcedureRepository(tokenizer, grammar)
    parser = Parser(procedure_repo, False, True, False)
    parser.parse(None, None, None)
    return procedure_repo


def test_1():
    current_test_dir = f"{common_input_dir}/T1"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    procedure_repo = run_parser(input_txt)

    tester_path = f"{dir_path}/resources/Tester/tester_Windows.exe"
    print(tester_path)
    actual_output = procedure_repo.code_generator.get_result()
    open(f"{dir_path}/resources/Tester/output.txt", "w", encoding="utf-8").write(actual_output)
    b = subprocess.Popen([sys.executable, '-c', tester_path],).communicate()[0]
    c= subprocess.run(tester_path)
    b= 10
    # assert open(f"{dir_path}/output.txt", 'r', encoding="utf-8").read().rstrip() == open(
    #     f'{current_test_dir}/parse_tree.txt',
    #     encoding="utf-8").read().rstrip()
    # assert str(procedure_repo.error_handler) == open(f'{current_test_dir}/syntax_errors.txt').read().rstrip()


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


if __name__ == '__main__':
    test_1()
