""" Authors:
        - Alireza Tajmirriahi - 97101372
        - Erfan Faravani - 97102174
"""
from parser import Parser
from scanner import Scanner
import utils


def run_compiler():
    parser = Parser(Scanner(INPUT_PATH))
    parser.run()

    utils.save_syntax_errors()
    utils.save_parse_tree()


INPUT_PATH = 'input.txt'

if __name__ == '__main__':
    run_compiler()
