import utils


def search_in_symbol_table(item, scope_num=0):
    for record in utils.symbol_table['ids'][::-1]:
        if item == record[0] and record[3] <= scope_num:
            return record[2]
    return False


class CodeGenerator:
    def __init__(self):
        self.SS = list()
        self.PB = dict()
        self.break_stack = list()
        self.current_scope = 0
        self.index = 0
        self.temp_address = 500
        self.operations_dict = {'+': 'ADD', '-': 'SUB', '<': 'LT', '==': 'EQ'}

        self.id_type = 'void'

    @staticmethod
    def find_address(item):
        if item == 'output':
            return item
        for record in utils.symbol_table['ids'][::-1]:
            if item == record[0]:
                return record[2]

    def call_routine(self, name, lookahead):
        # if len(self.PB)>1:
        #     print(name,lookahead)
        #     print(self.PB)
        self.__getattribute__(name[1:])(lookahead)

    def insert_code(self, part1, part2, part3='', part4=''):
        self.PB[self.index] = f'({part1}, {part2}, {part3}, {part4})'
        self.index += 1

    def get_temp(self, count=1):
        address = str(self.temp_address)
        for _ in range(count):
            self.insert_code('ASSIGN', '#0', str(self.temp_address))
            self.temp_address += 4
        return address

    def define_variable(self, lookahead):
        var_id = self.SS.pop()
        self.void_check(var_id)

        address = self.get_temp()
        utils.symbol_table['ids'].append((var_id, 'int', address, self.current_scope))

    def define_array(self, lookahead):
        array_size, array_id = int(self.SS.pop()[1:]), self.SS.pop()
        self.void_check(array_id)

        address = self.get_temp()
        array_space = self.get_temp(array_size)

        self.insert_code('ASSIGN', f'#{array_space}', address)
        utils.symbol_table['ids'].append((array_id, 'int*', address, self.current_scope))

    def get_id_type(self, lookahead):
        self.id_type = lookahead

    def push_id(self, lookahead):
        self.SS.append(lookahead[2])

    def push_id_address(self, lookahead):
        self.scope_check(lookahead)
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

        self.SS.append(address)

    def assign_operation(self, lookahead):
        self.insert_code('ASSIGN', self.SS[-1], self.SS[-2])
        self.SS.pop()

    def multiply(self, lookahead):
        result_address = self.get_temp()

        self.insert_code('MULT', self.SS[-1], self.SS[-2], result_address)
        self.SS.pop()
        self.SS.pop()
        self.SS.append(result_address)

    def array_index(self, lookahead):
        idx, array_address = self.SS.pop(), self.SS.pop()

        temp, result = self.get_temp(), self.get_temp()
        self.insert_code('MULT', '#4', idx, temp)
        self.insert_code('ASSIGN', f'{array_address}', result)
        self.insert_code('ADD', result, temp, result)

        self.SS.append(f'@{result}')

    def implicit_output(self, lookahead):
        if self.SS[-2] == 'output':
            self.insert_code('PRINT', self.SS.pop())

    def save(self, lookahead):
        self.SS.append(self.index)
        self.index += 1

    def label(self, lookahead):
        self.SS.append(self.index)

    def jpf_save(self, lookahead):
        dest = self.SS.pop()
        src = self.SS.pop()
        self.PB[dest] = f'(JPF, {src}, {self.index + 1}, )'
        self.SS.append(self.index)
        self.index += 1

    def jump(self, lookahead):
        dest = int(self.SS.pop())
        self.PB[dest] = f'(JP, {self.index}, , )'

    def while_jumps(self, lookahead):
        self.PB[int(self.SS[-1])] = f'(JPF, {self.SS[-2]}, {self.index + 1}, )'
        self.PB[self.index] = f'(JP, {self.SS[-3]}, , )'
        self.index += 1
        self.SS.pop(), self.SS.pop(), self.SS.pop()

    def negate_factor(self, lookahead):
        result = self.get_temp()
        factor_value = self.SS.pop()
        self.insert_code('SUB', '#0', factor_value, result)
        self.SS.append(result)

    def clean_up(self, lookahead):
        self.SS.pop()

    # Phase IV routines
    def get_temp_save(self, lookahead):
        temp = self.get_temp()
        self.SS.append(temp)
        self.insert_code('ASSIGN', f'#{self.index + 3}', temp)
        temp_2 = self.get_temp()
        self.SS.append(temp_2)
        self.SS.append(self.index)
        self.index += 1

    def for_statement(self, lookahead):
        self.insert_code('ADD', self.SS[-3], '#2', self.SS[-3])
        self.insert_code('JP', f'@{self.SS[-3]}')
        self.PB[self.SS[-1]] = f'(JP, {self.index}, , )'
        self.SS.pop(), self.SS.pop(), self.SS.pop()

    def assign_jump(self, lookahead):
        self.insert_code('ASSIGN', self.SS[-1], self.SS[-2])
        self.insert_code('JP', f'@{self.SS[-4]}')
        self.SS.pop()

    def jump_fill_save(self, lookahead):
        self.PB[int(self.SS[-2])] = f'(ASSIGN, #{self.index + 1}, {self.SS[-3]}, )'
        self.SS.pop(), self.SS.pop()
        self.SS.append(self.index)
        self.index += 1

    # Break statement
    def break_loop(self, lookahead):
        self.break_check(lookahead)
        """saves i to be later filled with a jump to after the scope"""
        self.break_stack.append(self.index)
        self.index += 1

    def new_break(self, lookahead):
        """makes sure that break-stmt breaks the deepest breakable scope"""
        self.break_stack.append('>>>')

    def end_break(self, lookahead):
        """fills PB[saved i] with a jump to current i and ends the scope"""
        latest_block = len(self.break_stack) - self.break_stack[::-1].index('>>>') - 1
        for item in self.break_stack[latest_block + 1:]:
            self.PB[item] = f'(JP, {self.index}, , )'
        self.break_stack = self.break_stack[:latest_block]

    def push_scope(self, lookahead):
        self.current_scope += 1

    def pop_scope(self, lookahead):
        for record in utils.symbol_table['ids'][::-1]:
            if record[3] == self.current_scope:
                del utils.symbol_table['ids'][-1]
        self.current_scope -= 1

    # semantic checks
    def scope_check(self, lookahead):
        if search_in_symbol_table(lookahead[2], self.current_scope):
            return
        utils.semantic_errors.append(f'#{lookahead[0]} : Semantic Error! {lookahead[2]} is not defined')

    def void_check(self, var_id):
        if self.id_type[2] == 'void':
            utils.semantic_errors.append(f'#{self.id_type[0]} : Semantic Error! Illegal type of void for {var_id}')

    def break_check(self, lookahead):
        if len(self.break_stack) > 0 and ['>>>' in self.break_stack]:
            return
        utils.semantic_errors.append(f'#{lookahead[0]} : Semantic Error! No "while" or "switch" found for "break"')

    def type_mismatch(self, lookahead):
        pass
