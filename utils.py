from collections import defaultdict

symbol_table = dict()  # only keys are used for now
lexical_errors = list()  # (line_no, lexeme, error_type)
tokens = defaultdict(list)  # {line_no: [(type, lexeme),]}


def init_symbol_table():
    symbol_table.update(
        {'keywords': ['if', 'else', 'void', 'int', 'while', 'break', 'switch',
                      'default', 'case', 'return', 'for'],
         'ids': []})


def save_errors():
    with open('lexical_errors.txt', 'w') as f:
        f.write('\n'.join([f'{err[0] + 1}.\t({err[1]}, {err[2]})' for err in lexical_errors]))


def save_symbol_table():
    with open('symbol_table.txt', 'w') as f:
        f.write('\n'.join(
            [f'{idx + 1}.\t{symbol}' for idx, symbol in enumerate(symbol_table['keywords'] + symbol_table['ids'])]))


def save_tokens():
    with open('tokens.txt', 'w') as f:
        f.write('\n'.join([f'{line_no + 1}.\t' + ' '.join([f'({token[0]}, {token[1]})' for token in line_tokens])
                           for line_no, line_tokens in tokens.items()]))
