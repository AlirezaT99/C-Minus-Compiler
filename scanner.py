from utils import *


class TokenType(enumerate):
    SYMBOL = "SYMBOL"
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    ID_OR_KEYWORD = "ID_OR_KEYWORD"
    INVALID = "Invalid input"


def get_token_type(char):
    if char in [' ', '\t', '\n', '\r', '\v', '\f']:  # WHITESPACE
        return TokenType.WHITESPACE
    elif char in [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<']:  # SYMBOL
        return TokenType.SYMBOL
    elif char.isdigit():  # NUM
        return TokenType.NUM
    elif char.isalnum():  # ID / KEYWORD
        return TokenType.ID_OR_KEYWORD
    elif char == '/':  # COMMENT
        return TokenType.COMMENT
    else:  # invalid
        return TokenType.INVALID


def get_from_table(name):
    if name in symbol_table['keywords']:
        return TokenType.KEYWORD
    elif name in symbol_table['ids']:
        return TokenType.ID
    else:
        ids = symbol_table['ids']
        ids.append(name)
        symbol_table.update({'ids': ids})
        return TokenType.ID


class Scanner:
    def __init__(self, input_path):
        self.input_path = input_path
        self.lines = None

        self.line_number = 0
        self.cursor = 0

        self.current_token = ""
        self.STATE = 0  # 0 in DFA

    def get_next_token(self):
        if self.eof_reached():
            return False

        char = self.get_current_char()
        token_type = get_token_type(char)

        if token_type == TokenType.WHITESPACE:
            if char == '\n':
                self.line_number += 1
            self.cursor += 1
            return self.get_next_token()

        elif token_type == TokenType.SYMBOL:
            if char == '=':
                if self.cursor < len(self.lines) - 1 \
                        and self.lines[self.cursor + 1] == '=':
                    self.cursor += 2
                    return self.line_number, TokenType.SYMBOL, '=='
            self.cursor += 1
            return self.line_number, TokenType.SYMBOL, char

        elif token_type == TokenType.NUM:
            number, has_error = self.number_token()
            if not has_error:
                return self.line_number, TokenType.NUM, number
            lexical_errors.append((self.line_number, char, 'Invalid number'))

        elif token_type == TokenType.ID_OR_KEYWORD:
            name, has_error = self.find_id_or_keyword()
            if not has_error:
                type = get_from_table(name)
                return self.line_number, type, name
            lexical_errors.append((self.line_number, char, 'Invalid number'))

        elif token_type == TokenType.COMMENT:
            pass

        elif token_type == TokenType.INVALID:
            lexical_errors.append((self.line_number, char, 'Invalid input'))
            self.cursor += 1

    def get_current_char(self):
        char = self.lines[self.cursor]
        return char

    def find_id_or_keyword(self):
        name = self.get_current_char()
        while self.cursor + 1 < len(self.lines):
            self.cursor += 1
            temp_char = self.get_current_char()
            temp_type = get_token_type(temp_char)

            if temp_type == TokenType.NUM or temp_type == TokenType.ID_OR_KEYWORD:
                name += temp_char

            elif temp_type == TokenType.WHITESPACE or temp_type == TokenType.SYMBOL:

                return name, False

            else:
                name += temp_char
                self.cursor += 1
                return name, True
        self.cursor += 1
        return name, False
        # print('error handling for keys',self.cursor,len(self.lines),self.get_current_char(),self.eof_reached())

    def number_token(self):
        num = self.get_current_char()
        while self.cursor + 1 < len(self.lines):
            self.cursor += 1
            temp_char = self.get_current_char()
            temp_type = get_token_type(temp_char)

            if temp_type == TokenType.NUM:
                num += temp_char

            elif temp_type == TokenType.WHITESPACE or temp_type == TokenType.SYMBOL:
                return num, False

            else:
                num += temp_char
                self.cursor += 1
                return num, True

        self.cursor += 1
        return num, False

    def read_all_tokens(self):
        with open(self.input_path, 'r') as f:
            self.lines = "".join([line for line in f.readlines()])

        while True:
            if self.eof_reached():
                break
            token = self.get_next_token()
            if token:
                print(token)

    def eof_reached(self):  # TODO mind that cursor start from 0 not 1
        return self.cursor >= len(self.lines)

# s = Scanner('input.txt')
# s.read_all_tokens()
