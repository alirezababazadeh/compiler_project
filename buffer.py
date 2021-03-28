class Buffer:
    def __init__(self, program_text):
        self.text = program_text
        self.pointer = 0
        self.line_number = 1

    def has_next(self):
        return self.pointer < len(self.text)

    def get_current_char(self):
        return self.text[self.pointer]

    def push_forward(self, length=1):
        self.pointer += length

    def take_back(self, length=1):
        self.pointer -= length

    def increase_line_number(self):
        self.line_number += 1

    def decrease_line_number(self):
        self.line_number -= 1

    def get_text(self, start, end):
        return self.text[start:end]

    def get_char_at(self, index):
        return self.text[index]
