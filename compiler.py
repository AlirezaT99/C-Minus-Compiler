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

    utils.save_syntax_errors(parser)
    utils.save_parse_tree(parser)


INPUT_PATH = 'input.txt'

if __name__ == '__main__':
    run_compiler()
