from compiler import INPUT_PATH
from utils import *


class Scanner:
    line_number = 0
    cursor = 0
    lines = None

    @staticmethod
    def get_next_token():
        return (), True

    @staticmethod
    def read_all_tokens():
        with open(INPUT_PATH, 'r') as f:
            Scanner.lines = [line.strip() for line in f.readlines()]

        while True:
            token, eof = Scanner.get_next_token()
            if eof:
                break
            tokens.add(token)
