from collections import defaultdict

from parser import Parser

symbol_table = dict()  # only keys are used for now
lexical_errors = defaultdict(list)  # {line_no: [lexeme, error_type]}
tokens = defaultdict(list)  # {line_no: [(type, lexeme),]}


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
    pass


def save_parse_tree(parser: Parser):
    pass


def init_grammar():
    return None
