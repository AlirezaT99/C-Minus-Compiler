import utils


class CodeGenerator:
    def __init__(self):
        self.SS = list()
        self.PB = dict()
        self.index = 0
        self.temp_address = 1000

        self.operations_dict = {'+': 'ADD', '-': 'SUB', '<': 'LT', '==': 'EQ'}

    @staticmethod
    def find_address(item):
        for record in utils.symbol_table['ids'][::-1]:
            if item == record[0]:
                return record[2]

    def call_routine(self, name, lookahead):
        self.__getattribute__(name[1:])(lookahead)

    def insert_code(self, part1, part2, part3='', part4=''):
        self.PB[self.index] = f'({part1}, {part2}, {part3}, {part4})'
        self.index += 1

    def get_temp(self, count=1):
        address = str(self.temp_address)
        for _ in range(count):
            self.insert_code('ASSIGN', '#0', self.temp_address)
            self.temp_address += 4
        return address

    def define_variable(self, lookahead):
        var_id = self.SS.pop()
        address = self.get_temp()
        utils.symbol_table['ids'].append((var_id, 'int', address))

    def define_array(self, lookahead):
        array_size, array_id = int(self.SS.pop()[1:]), self.SS.pop()
        address = self.get_temp()
        array_space = self.get_temp(array_size)

        self.insert_code('ASSIGN', f'#{array_space}', address)
        utils.symbol_table['ids'].append((array_id, 'int*', address))

    def push_id(self, lookahead):
        self.SS.append(lookahead[2])

    def push_id_address(self, lookahead):
        self.SS.append(CodeGenerator.find_address(lookahead[2]))

    def push_num(self, lookahead):
        self.SS.append(f'#{lookahead[2]}')

    def push_operator(self, lookahead):
        self.SS.append(lookahead[2])

    def save_operation(self, lookahead):
        operand_2 = self.SS.pop()
        operator = self.SS.pop()
        operand_1 = self.SS.pop()

        address = self.get_temp()
        self.insert_code(self.operations_dict[operator], operand_1, operand_2, address)

    def assign_operation(self, lookahead):
        self.insert_code('ASSIGN', self.SS[-1], self.SS[-2])
        self.SS.pop()
