""" Authors:
        - Alireza Tajmirriahi - 97101372
        - Erfan Faravani - 97102174
"""
import utils
from parse_tools import Parser  # python already has a parser package, so...
from scanner import Scanner


def run_compiler():
    parser = Parser(Scanner(INPUT_PATH))
    parser.run()
    if len(utils.semantic_errors) > 0:
        utils.save_semantic_errors()
    else:
        utils.save_program(parser.code_generator)


INPUT_PATH = 'input.txt'

if __name__ == '__main__':
    run_compiler()
