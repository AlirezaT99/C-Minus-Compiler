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


class Scanner:
    def __init__(self, input_path):
        self.input_path = input_path
        self.lines = None

        self.line_number = 0
        self.cursor = 0

        self.current_token = ""
        self.STATE = 0  # 0 in DFA

    def get_next_token(self):
        char = self.get_next_char()

    def get_token_type(self, char):
        if char in [' ', '\t', '\n', '\r', '\v', '\f']:  # WHITESPACE
            return TokenType.WHITESPACE
        elif char in [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<']:  # SYMBOL
            if char == '=':
                if self.cursor < len(self.lines[self.line_number]) - 1 and self.lines[self.line_number][
                    self.cursor + 1] == '=':
                    self.cursor += 2
                    return self.line_number, 'SYMBOL', '=='
            self.cursor += 1
            return self.line_number, 'SYMBOL', char
        elif char.isdigit():  # NUM
            return TokenType.NUM
        elif char.isalnum():  # ID / KEYWORD
            return TokenType.ID_OR_KEYWORD
        elif char == '/':  # COMMENT
            return TokenType.COMMENT
        else:  # invalid
            lexical_errors.append((self.line_number, char, 'Invalid input'))

    def get_next_char(self):
        if self.cursor == len(self.lines[self.line_number]):
            self.cursor = 0
            self.line_number += 1  # EOF is checked already

        # lexeme_beginning = (Scanner.line_number, Scanner.cursor)
        char = self.lines[self.line_number][self.cursor]
        self.cursor += 1
        return char

    def number_token(self):
        pass

    def read_all_tokens(self):
        with open(self.input_path, 'r') as f:
            self.lines = [line.strip() for line in f.readlines()]

        while True:
            if self.eof_reached():
                break
            tokens.add(self.get_next_token())

    def eof_reached(self):  # TODO mind that line_number and cursor start from 0 not 1
        return self.line_number >= len(self.lines) \
               and self.cursor >= len(self.lines[-1])
