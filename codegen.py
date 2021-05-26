import utils


class CodeGenerator:
    def __init__(self):
        self.memory = dict()
        self.temp_address = 1000 - 4

    def call_routine(self, name):
        self.__getattribute__(name[1:])()

    def get_temp(self):
        self.temp_address += 4
        self.memory[self.temp_address] = None
        return self.temp_address

    def find_address(self, item):
        return None  # TODO

