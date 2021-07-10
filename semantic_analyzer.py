from symbol_table import SymbolTable


class SemanticAnalyzer:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.errors = []

    def report_error(self, err_type, *args):
        prefix = f'#{args[0]} : Semantic Error!'
        if err_type == 'notDefined':
            self.errors.append(f"{prefix} '{args[0]}' is not defined.")
        elif err_type == 'argumentCountMismatch':
            self.errors.append(f'{prefix} Mismatch in numbers of arguments of "{args[1]}".')
        elif err_type == 'argumentTypeMismatch':
            self.errors.append(
                f"{prefix} Mismatch in type of argument {args[1]} of '{args[2]}'. Expected '{args[3]}' but got '{args[4]}' instead.")

    def get_result(self):
        output = ""
        for error in self.errors:
            output += error + "\n"

        if len(output) == 0:
            output = "The input program is semantically correct."
        return output

    def has_any_error(self):
        return len(self.errors) > 0

    def write_to_file(self, path):
        open(path, 'w', encoding='utf-8').write(self.get_result())
