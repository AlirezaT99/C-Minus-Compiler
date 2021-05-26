import utils


class CodeGenerator:
    def __init__(self):
        self.SS = list()
        self.PB = dict()
        self.index = 1
        self.temp_address = 1000 - 4

    def call_routine(self, name, lookahead):
        self.__getattribute__(name[1:])(lookahead)

    def insert_code(self, part1, part2, part3='', part4=''):
        self.PB[self.index] = f'({part1}, {part2}, {part3}, {part4})'
        self.index += 1

    def get_temp(self):
        address = str(self.temp_address)
        self.insert_code('ASSIGN', '#0', address)

        self.temp_address += 4
        return address

    def hi(self, token):
        print('hi')

    @staticmethod
    def find_address(item):
        return None  # TODO
