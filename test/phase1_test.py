import os

from buffer import Buffer
from consts import KEYWORDS
from error_handler import LexicalErrorHandler
from scanner import Tokenizer
from symbol_table import SymbolTable
from token_repo import TokenRepository

dir_path = os.path.join(os.path.dirname(__file__))

common_input_dir = f'{dir_path}/resources/Phase1-ScannerTests'


def run_tokenizer(program_text):
    buffer = Buffer(program_text)
    symbol_table = SymbolTable(KEYWORDS)
    error_handler = LexicalErrorHandler()
    token_repository = TokenRepository()
    tokenizer = Tokenizer(buffer, token_repository, error_handler, symbol_table)
    while buffer.has_next():
        tokenizer.get_next_token()
    return symbol_table, token_repository, error_handler


def test_1():
    current_test_dir = f"{common_input_dir}/T01"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    symbol_table, token_repo, error_handler = run_tokenizer(input_txt)

    assert str(token_repo) == open(f'{current_test_dir}/tokens.txt').read().rstrip()
    assert str(symbol_table) == open(f'{current_test_dir}/symbol_table.txt').read().rstrip()
    assert str(error_handler) == open(f'{current_test_dir}/lexical_errors.txt').read().rstrip()


def test_2():
    current_test_dir = f"{common_input_dir}/T02"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    symbol_table, token_repo, error_handler = run_tokenizer(input_txt)

    assert str(token_repo) == open(f'{current_test_dir}/tokens.txt').read().rstrip()
    assert str(symbol_table) == open(f'{current_test_dir}/symbol_table.txt').read().rstrip()
    assert str(error_handler) == open(f'{current_test_dir}/lexical_errors.txt').read().rstrip()


def test_3():
    current_test_dir = f"{common_input_dir}/T03"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    symbol_table, token_repo, error_handler = run_tokenizer(input_txt)

    assert str(token_repo) == open(f'{current_test_dir}/tokens.txt').read().rstrip()
    assert str(symbol_table) == open(f'{current_test_dir}/symbol_table.txt').read().rstrip()
    assert str(error_handler) == open(f'{current_test_dir}/lexical_errors.txt').read().rstrip()


def test_4():
    current_test_dir = f"{common_input_dir}/T04"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    symbol_table, token_repo, error_handler = run_tokenizer(input_txt)

    assert str(token_repo) == open(f'{current_test_dir}/tokens.txt').read().rstrip()
    assert str(symbol_table) == open(f'{current_test_dir}/symbol_table.txt').read().rstrip()
    assert str(error_handler) == open(f'{current_test_dir}/lexical_errors.txt').read().rstrip()


def test_5():
    current_test_dir = f"{common_input_dir}/T05"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    symbol_table, token_repo, error_handler = run_tokenizer(input_txt)

    assert str(token_repo) == open(f'{current_test_dir}/tokens.txt').read().rstrip()
    assert str(symbol_table) == open(f'{current_test_dir}/symbol_table.txt').read().rstrip()
    assert str(error_handler) == open(f'{current_test_dir}/lexical_errors.txt').read().rstrip()


def test_6():
    current_test_dir = f"{common_input_dir}/T06"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    symbol_table, token_repo, error_handler = run_tokenizer(input_txt)

    assert str(token_repo) == open(f'{current_test_dir}/tokens.txt').read().rstrip()
    assert str(symbol_table) == open(f'{current_test_dir}/symbol_table.txt').read().rstrip()
    assert str(error_handler) == open(f'{current_test_dir}/lexical_errors.txt').read().rstrip()


def test_7():
    current_test_dir = f"{common_input_dir}/T07"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    symbol_table, token_repo, error_handler = run_tokenizer(input_txt)

    assert str(token_repo) == open(f'{current_test_dir}/tokens.txt').read().rstrip()
    assert str(symbol_table) == open(f'{current_test_dir}/symbol_table.txt').read().rstrip()
    assert str(error_handler) == open(f'{current_test_dir}/lexical_errors.txt').read().rstrip()


def test_8():
    current_test_dir = f"{common_input_dir}/T08"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    symbol_table, token_repo, error_handler = run_tokenizer(input_txt)

    assert str(token_repo) == open(f'{current_test_dir}/tokens.txt').read().rstrip()
    assert str(symbol_table) == open(f'{current_test_dir}/symbol_table.txt').read().rstrip()
    assert str(error_handler) == open(f'{current_test_dir}/lexical_errors.txt').read().rstrip()


def test_9():
    current_test_dir = f"{common_input_dir}/T09"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    symbol_table, token_repo, error_handler = run_tokenizer(input_txt)

    assert str(token_repo) == open(f'{current_test_dir}/tokens.txt').read().rstrip()
    assert str(symbol_table) == open(f'{current_test_dir}/symbol_table.txt').read().rstrip()
    assert str(error_handler) == open(f'{current_test_dir}/lexical_errors.txt').read().rstrip()


def test_10():
    current_test_dir = f"{common_input_dir}/T10"
    input_txt = open(f"{current_test_dir}/input.txt").read()
    symbol_table, token_repo, error_handler = run_tokenizer(input_txt)

    assert str(token_repo) == open(f'{current_test_dir}/tokens.txt').read().rstrip()
    assert str(symbol_table) == open(f'{current_test_dir}/symbol_table.txt').read().rstrip()
    assert str(error_handler) == open(f'{current_test_dir}/lexical_errors.txt').read().rstrip()
