""" Authors:
        - Alireza Tajmirriahi - 97101372
        - Erfan Faravani - 97102174
"""
import sys
import scanner
import utils


def run_compiler():
    utils.init_symbol_table(symbol_table)
    scanner.read_all_tokens(INPUT_PATH)


INPUT_PATH = './input.txt'
symbol_table = dict()  # only keys are used for now
lexical_errors = list()  # (line_no, lexeme, error_type)

if __name__ == '__main__':
    # INPUT_PATH = sys.argv[-1] if len(sys.argv) > 1 else input()
    run_compiler()
