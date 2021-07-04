import os

dir_path = os.path.join(os.path.dirname(__file__))


def test_1():
    input = open(dir_path + "resources/Phase1-ScannerTests/T01/input.txt").read()

    expected_lexical_errors = open(dir_path + "resources/Phase1-ScannerTests/T01/lexical_errors.txt").read()
    expected_symbol_table = open(dir_path + "resources/Phase1-ScannerTests/T01/symbol_table.txt").read()
    expected_tokens = open(dir_path + "resources/Phase1-ScannerTests/T01/tokens.txt").read()


def test_2():
    pass


def test_3():
    pass


def test_4():
    pass


def test_5():
    pass


def test_6():
    pass


def test_7():
    pass


def test_8():
    pass


def test_9():
    pass


def test_10():
    pass
