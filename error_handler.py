class ErrorHandler:
    def __init__(self):
        self.errors = {}

    def add_lexical_error(self, lexical_error, line_no):
        if self.errors.get(str(line_no), None):
            self.errors.get(str(line_no)).append(lexical_error)
        else:
            self.errors[str(line_no)] = [lexical_error]

    def __str__(self):
        output = ""
        for key, values in self.errors.items():
            values_string = ""
            for value in values:
                values_string += f"({value[0]}, {value[1]}) "
            output += f"{key}.\t{values_string.strip()}\n"
        return output

    def has_any_error(self):
        return len(self.errors) > 0
