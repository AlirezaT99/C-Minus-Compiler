import utils
from codegen import CodeGenerator
from anytree import Node


def is_non_terminal(word):
    return word in utils.productions.keys()


def is_action_symbol(word: str):
    return word.startswith('#')


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.code_generator = CodeGenerator()

        utils.init_grammar()

        self.root = Node('Program')
        self.lookahead = None

        self.syntax_errors = []
        self.unexpected_eof_reached = False

    def get_next_token(self):
        token = self.scanner.get_next_token()
        while not token:  # Could've returned False due to lexical error
            token = self.scanner.get_next_token()
        return token

    def run(self):
        self.lookahead = self.get_next_token()
        self.call_procedure(self.root)

    def call_procedure(self, non_terminal: Node):
        for rule_number in utils.productions[non_terminal.name]:
            if self.lookahead[2] in utils.predict[rule_number] or \
                    self.lookahead[1] in utils.predict[rule_number]:  # selecting the appropriate production
                self.call_rule(non_terminal, rule_number)
                break
        else:  # is visited when no corresponding production was found
            if self.lookahead[2] in utils.follow[non_terminal.name]:
                if utils.TokenType.EPSILON not in utils.first[non_terminal.name]:  # missing T
                    self.syntax_errors.append(f'#{self.lookahead[0]} : Syntax Error, Missing {non_terminal.name}')
                non_terminal.parent = None  # Detach Node
                return  # exit
            else:  # illegal token
                if self.eof_reached():
                    self.syntax_errors.append(f'#{self.lookahead[0]} : syntax error, unexpected EOF')
                    self.unexpected_eof_reached = True
                    non_terminal.parent = None  # Detach Node
                    return
                # in samples, illegals are treated differently:
                illegal_lookahead = self.lookahead[2]
                if self.lookahead[1] in ['NUM', 'ID']:
                    illegal_lookahead = self.lookahead[1]
                #
                self.syntax_errors.append(f'#{self.lookahead[0]} : syntax error, illegal {illegal_lookahead}')
                self.lookahead = self.get_next_token()
                self.call_procedure(non_terminal)

    def call_rule(self, parent, rule_number):
        for part in utils.grammar[rule_number]:
            if self.unexpected_eof_reached:
                return
            if is_action_symbol(part):
                self.code_generator.call_routine(part, self.lookahead)
            elif is_non_terminal(part):
                node = Node(part, parent=parent)
                self.call_procedure(node)
            else:
                self.call_match(part, parent)

    def call_match(self, expected_token, parent):
        correct = False
        if expected_token in ['NUM', 'ID']:
            correct = self.lookahead[1] == expected_token
        elif (expected_token in utils.symbol_table['keywords']) \
                or (utils.get_token_type(expected_token) == utils.TokenType.SYMBOL or expected_token == '=='):
            correct = self.lookahead[2] == expected_token

        if correct:
            Node(f'({self.lookahead[1]}, {self.lookahead[2]})', parent=parent)
            self.lookahead = self.get_next_token()
        elif expected_token == utils.TokenType.EPSILON:
            Node('epsilon', parent=parent)
        elif expected_token == utils.TokenType.DOLLAR:
            Node('$', parent=parent)
        else:
            self.syntax_errors.append(f'#{self.lookahead[0]} : Syntax Error, Missing {expected_token}')

    def eof_reached(self):
        return self.lookahead[1] == utils.TokenType.DOLLAR
