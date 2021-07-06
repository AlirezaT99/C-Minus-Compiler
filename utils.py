import json
from collections import defaultdict

from anytree import RenderTree

from parse_tools import Parser

symbol_table = dict()  # only keys are used for now
lexical_errors = defaultdict(list)  # {line_no: [lexeme, error_type]}
semantic_errors = []
tokens = defaultdict(list)  # {line_no: [(type, lexeme),]}

first = dict()  # {T: [First(T)]}
follow = dict()  # {T: [Follow(T)]}
predict = dict()  # {No: [First(Prod(No))]}
productions = dict()  # {T: [prod numbers]}
grammar = dict()  # {No: Prod}


class TokenType:
    SYMBOL = 'SYMBOL'
    NUM = 'NUM'
    ID = 'ID'
    KEYWORD = 'KEYWORD'
    COMMENT = 'COMMENT'
    WHITESPACE = 'WHITESPACE'
    ID_OR_KEYWORD = 'ID_OR_KEYWORD'
    INVALID = 'Invalid input'
    DOLLAR = '$'
    EPSILON = 'EPSILON'


def get_symbol_table_from_id(id):
    for i in symbol_table['ids']:
        if i[0] == id:
            return i


def get_token_type(char):
    if char in [' ', '\t', '\n', '\r', '\v', '\f']:  # WHITESPACE
        return TokenType.WHITESPACE
    elif char in [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<']:  # SYMBOL
        return TokenType.SYMBOL
    elif char.isdigit():  # NUM
        return TokenType.NUM
    elif char.isalnum():  # ID / KEYWORD
        return TokenType.ID_OR_KEYWORD
    elif char == '/':  # COMMENT (potentially)
        return TokenType.COMMENT
    else:  # Invalid input
        return TokenType.INVALID


def init_symbol_table():
    symbol_table.update(
        {'keywords': ['if', 'else', 'void', 'int', 'while', 'break', 'switch',
                      'default', 'case', 'return', 'for'],
         'ids': []})


def save_lexical_errors():
    with open('lexical_errors.txt', 'w') as f:
        if lexical_errors:
            f.write('\n'.join([f'{line_no + 1}.\t' + ' '.join([f'({err[0]}, {err[1]})' for err in line_errors])
                               for line_no, line_errors in lexical_errors.items()]))
        else:
            f.write('There is no lexical error.')


def save_symbol_table():
    with open('symbol_table.txt', 'w') as f:
        f.write('\n'.join(
            [f'{idx + 1}.\t{symbol}' for idx, symbol in enumerate(symbol_table['keywords'] + symbol_table['ids'])]))


def save_tokens():
    with open('tokens.txt', 'w') as f:
        f.write('\n'.join([f'{line_no + 1}.\t' + ' '.join([f'({token[0]}, {token[1]})' for token in line_tokens])
                           for line_no, line_tokens in tokens.items()]))


def save_syntax_errors(parser: Parser):
    with open('syntax_errors.txt', 'w') as f:
        if not parser.syntax_errors:
            f.write('There is no syntax error.\n')
        else:
            f.write('\n'.join(error for error in parser.syntax_errors))


def save_parse_tree(parser: Parser):
    with open('parse_tree.txt', 'w', encoding='utf-8') as f:
        for pre, fill, node in RenderTree(parser.root):
            f.write("%s%s\n" % (pre, node.name))


def init_grammar():
    with open('./assets/non_terminals_lines.json', 'r') as f:
        productions.update(json.load(f))
    with open('./assets/first.txt', 'r') as f:
        for line in f.readlines():
            line_parts = line.strip().split(' ')
            first[line_parts[0]] = line_parts[1:]
    with open('./assets/follow.txt', 'r') as f:
        for line in f.readlines():
            line_parts = line.strip().split(' ')
            follow[line_parts[0]] = line_parts[1:]
    with open('./assets/predict.txt', 'r') as f:
        for line in f.readlines():
            line_parts = line.strip().split(' ')
            predict[int(line_parts[0])] = line_parts[1:]
    with open('./assets/pa3grammar.txt', 'r') as f:
        for idx, line in enumerate(f.readlines()):
            rhs = line.strip().split('->')[1]  # right-hand side
            grammar[idx + 1] = rhs.strip().split(' ')


def save_semantic_errors():
    with open('semantic_errors.txt', 'w') as f:
        for idx in semantic_errors:
            f.write(f'{idx}\n')
    with open('output.txt', 'w') as f:
        f.write('The code has not been generated.')


def save_program(code_gen):
    with open('output.txt', 'w') as f:
        for idx in sorted(code_gen.PB.keys()):
            f.write(f'{idx}\t{code_gen.PB[idx]}\n')
