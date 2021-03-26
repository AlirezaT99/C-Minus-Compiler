""" Authors:
        - Alireza Tajmirriahi - 97101372
        - Erfan Faravani - 97102174
"""
from self import self
import utils


def run_compiler():
    utils.init_symbol_table()
    self.read_all_tokens()


INPUT_PATH = './samples/T01/input.txt'

if __name__ == '__main__':
    run_compiler()
