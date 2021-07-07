class MemoryManager:
    def __init__(self):
        self.data_cursor = 1000
        self.temp_cursor = 500

    def get_temp_address(self):
        pointer = self.temp_cursor
        self.temp_cursor += 4
        return pointer

    def get_new_data_address(self):
        self.data_cursor += 4
        return self.data_cursor
