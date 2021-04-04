class TokenRepository:
    def __init__(self):
        self.tokens = {}

    def add_token(self, token, line_no):
        if token:
            if self.tokens.get(str(line_no), None):
                self.tokens.get(str(line_no)).append(token)
            else:
                self.tokens[str(line_no)] = [token]

    def has_any(self):
        return len(self.tokens) > 0

    def __str__(self):
        output = ''
        for key, values in self.tokens.items():
            values_string = ""
            for value in values:
                values_string += f"({value[0]}, {value[1]}) "
            output += f"{key}.\t{values_string.strip()}\n"
        return output
