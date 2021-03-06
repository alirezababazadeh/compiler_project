class Buffer:
    def __init__(self, program_text):
        self.text = program_text
        self.pointer = 0
        self.line_number = 1

    def has_next(self, index=0):
        return self.pointer + index < len(self.text)

    def current_char(self):
        return self.text[self.pointer]

    def push_forward(self, length=1):
        self.pointer += length

    def increase_line_number(self, count=1):
        self.line_number += count

    def get_text(self, start, end):
        return self.text[start:end]

    def get_char_at(self, index):
        return self.text[index]
