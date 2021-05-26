""" Authors:
        - Alireza Tajmirriahi - 97101372
        - Erfan Faravani - 97102174
"""
from scanner import Scanner
from parse_tools import Parser  # python already has a parser package, so...
import utils


def run_compiler():
    parser = Parser(Scanner(INPUT_PATH))
    parser.run()

    utils.save_program(parser.code_generator)


INPUT_PATH = 'samples_p3/T1/input.txt'

if __name__ == '__main__':
    run_compiler()
