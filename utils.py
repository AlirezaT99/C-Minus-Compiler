def init_symbol_table(symbol_table):
    symbol_table.update(
        {'if': None, 'else': None, 'void': None, 'int': None, 'while': None, 'break': None, 'switch': None,
         'default': None, 'case': None, 'return': None, 'for': None})


def save_errors(lexical_errors):
    with open('lexical_errors.txt', 'w') as f:
        for err in lexical_errors:
            f.write(f'{err[0]}.\t({err[1]}, {err[2]})\n')


def save_symbol_table(symbol_table):
    with open('symbol_table.txt', 'w') as f:
        for idx, symbol in enumerate(symbol_table):
            f.write(f'{idx + 1}.\t{symbol}\n')


def save_tokens(tokens):
    pass
