from compiler import INPUT_PATH
from utils import *


class Scanner:
    lines = None

    line_number = 0
    cursor = 0
    STATE = 0  # 0 in DFA

    @staticmethod
    def get_next_token():
        if Scanner.cursor == len(Scanner.lines[Scanner.line_number]):
            Scanner.cursor = 0
            Scanner.line_number += 1  # EOF is checked already

        # lexeme_beginning = (Scanner.line_number, Scanner.cursor)
        line = Scanner.lines[Scanner.line_number]
        char = line[Scanner.cursor]

        if char in [' ', '\t', '\n', '\r', '\v', '\f']:  # WHITESPACE
            pass  # TODO

        elif char in [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<']:  # SYMBOL
            if char == '=':
                if Scanner.cursor < len(line) - 1 and line[Scanner.cursor + 1] == '=':  # ==
                    Scanner.cursor += 2
                    return Scanner.line_number, 'SYMBOL', '=='
            Scanner.cursor += 1
            return Scanner.line_number, 'SYMBOL', char

        elif char.isdigit():  # NUM
            pass  # TODO

        elif char.isalnum():  # ID / KEYWORD
            pass  # TODO

        elif char == '/':  # COMMENT
            pass  # TODO

        else:  # invalid
            lexical_errors.append((Scanner.line_number, char, 'Invalid input'))
            Scanner.cursor += 1

    @staticmethod
    def read_all_tokens():
        with open(INPUT_PATH, 'r') as f:
            Scanner.lines = [line.strip() for line in f.readlines()]

        while True:
            if Scanner.eof_reached():
                break
            tokens.add(Scanner.get_next_token())

    @staticmethod
    def eof_reached():  # TODO mind that line_number and cursor start from 0 not 1
        return Scanner.line_number >= len(Scanner.lines) \
               and Scanner.cursor >= len(Scanner.lines[-1])
