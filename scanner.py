from compiler import INPUT_PATH
from utils import *


class Scanner:
    line_number = 0
    cursor = 0
    lines = None

    @staticmethod
    def get_next_token():
        return ()

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
