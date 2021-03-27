""" Authors:
        - Alireza Tajmirriahi - 97101372
        - Erfan Faravani - 97102174
"""
from scanner import Scanner
import utils


def run_compiler():
    utils.init_symbol_table()
    Scanner(INPUT_PATH).read_all_tokens()

    utils.save_errors()
    utils.save_symbol_table()
    utils.save_tokens()


INPUT_PATH = 'input.txt'

if __name__ == '__main__':
    run_compiler()
