class MemoryManager:
    def __init__(self):
        self.initial_temp_pointer = 100
        self.initial_data_pointer = 1000
        self.data_pointer = self.initial_temp_pointer
        self.temp_pointer = self.initial_data_pointer

    def get_temp_address(self):
        pointer = self.temp_pointer
        self.temp_pointer += 4
        return pointer

    def get_new_data_address(self):
        pointer = self.data_pointer
        self.data_pointer += 4
        return pointer
