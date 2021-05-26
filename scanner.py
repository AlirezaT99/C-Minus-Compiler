from utils import *


def get_from_table(name):
    if name in symbol_table['keywords']:
        return TokenType.KEYWORD
    else:
        if name not in symbol_table['ids']:
            # symbol_table['ids'].append(name)
            pass
        return TokenType.ID


def get_short_comment(comment):
    return comment[:7] + '...' if len(comment) >= 7 else comment


class Scanner:
    def __init__(self, input_path):
        init_symbol_table()

        self.input_path = input_path
        self.lines = None
        self.read_input()

        self.line_number = 1
        self.cursor = 0

    def read_input(self):
        with open(self.input_path, 'r') as f:
            self.lines = ''.join([line for line in f.readlines()])

    def get_next_token(self):
        if self.eof_reached():
            return self.line_number, TokenType.DOLLAR, '$'

        char = self.get_current_char()
        token_type = get_token_type(char)

        if token_type == TokenType.WHITESPACE:
            if char == '\n':
                self.line_number += 1
            self.cursor += 1
            return self.get_next_token()

        elif token_type == TokenType.SYMBOL:
            if char == '=':
                if self.cursor < len(self.lines) - 1 \
                        and self.lines[self.cursor + 1] == '=':
                    self.cursor += 2
                    return self.line_number, TokenType.SYMBOL, '=='
            elif char == '*':
                if self.cursor < len(self.lines) - 1 \
                        and self.lines[self.cursor + 1] == '/':
                    self.cursor += 2
                    lexical_errors[self.line_number].append(('*/', 'Unmatched comment'))
                    return False
            self.cursor += 1
            return self.line_number, TokenType.SYMBOL, char

        elif token_type == TokenType.NUM:
            number, has_error = self.number_token()
            if not has_error:
                return self.line_number, TokenType.NUM, number
            lexical_errors[self.line_number].append((number, 'Invalid number'))

        elif token_type == TokenType.ID_OR_KEYWORD:
            name, has_error = self.find_id_or_keyword()
            if not has_error:
                return self.line_number, get_from_table(name), name
            lexical_errors[self.line_number].append((name, 'Invalid input'))

        elif token_type == TokenType.COMMENT:
            self.find_comment()

        elif token_type == TokenType.INVALID:
            lexical_errors[self.line_number].append((char, 'Invalid input'))
            self.cursor += 1

    def find_comment(self):
        beginning_line_number = self.line_number

        lexeme = self.get_current_char()
        if self.cursor + 1 == len(self.lines):
            lexical_errors[self.line_number].append((lexeme, 'Invalid input'))  # last char is /
            self.cursor += 1
            return None, True

        next_char = self.lines[self.cursor + 1]
        if next_char not in ['/', '*']:
            lexical_errors[self.line_number].append(
                (lexeme + (next_char if next_char != '\n' else ''), 'Invalid input'))  # /
            if next_char == '\n':  # Pure tof to fix the minor bug
                self.line_number += 1
            self.cursor += 2
            return None, True

        is_multiline = next_char == '*'

        while self.cursor + 1 < len(self.lines):
            self.cursor += 1
            temp_char = self.get_current_char()

            if temp_char == '\n' and not is_multiline:
                self.line_number += 1
                break
            if is_multiline:
                if self.cursor + 1 < len(self.lines):
                    if temp_char == '*' and self.lines[self.cursor + 1] == '/':
                        self.cursor += 2
                        return lexeme + '*/', False
                else:
                    lexeme += self.lines[-1]
                    self.cursor += 1
                    lexical_errors[beginning_line_number].append((get_short_comment(lexeme), 'Unclosed comment'))
                    return None, True

            if temp_char == '\n':
                self.line_number += 1
            lexeme += temp_char

        self.cursor += 1
        return lexeme, False

    def get_current_char(self):
        return self.lines[self.cursor]

    def find_id_or_keyword(self):
        name = self.get_current_char()
        while self.cursor + 1 < len(self.lines):
            self.cursor += 1
            temp_char = self.get_current_char()
            temp_type = get_token_type(temp_char)

            if temp_type == TokenType.NUM or temp_type == TokenType.ID_OR_KEYWORD:
                name += temp_char
            elif temp_type == TokenType.WHITESPACE or temp_type == TokenType.SYMBOL:
                return name, False
            else:
                name += temp_char
                self.cursor += 1
                return name, True

        self.cursor += 1
        return name, False

    def number_token(self):
        num = self.get_current_char()
        while self.cursor + 1 < len(self.lines):
            self.cursor += 1
            temp_char = self.get_current_char()
            temp_type = get_token_type(temp_char)

            if temp_type == TokenType.NUM:
                num += temp_char
            elif temp_type == TokenType.WHITESPACE or temp_type == TokenType.SYMBOL:
                return num, False
            else:
                num += temp_char
                self.cursor += 1
                return num, True

        self.cursor += 1
        return num, False

    def read_all_tokens(self):
        while True:
            if self.eof_reached():
                break
            token = self.get_next_token()
            if token:
                tokens[token[0]].append(token[1:])

    def eof_reached(self):
        return self.cursor >= len(self.lines)
