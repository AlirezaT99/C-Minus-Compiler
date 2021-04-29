import utils
from anytree import Node


def is_non_terminal(word):
    return word in utils.productions.keys()


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        utils.init_grammar()

        self.root = Node('Program')
        self.lookahead = None
        self.syntax_errors = []

    def get_next_token(self):
        token = self.scanner.get_next_token()
        while not token:  # Could've returned False due to lexical error
            token = self.scanner.get_next_token()
        # print(token)
        return token

    def run(self):
        self.lookahead = self.get_next_token()
        self.call_procedure(self.root)

    def call_procedure(self, non_terminal: Node):
        print(self.lookahead)
        if non_terminal.name=='Expression-stmt':
            print(1000)
        for rule_number in utils.productions[non_terminal.name]:
            if self.lookahead[2] in utils.predict[rule_number] or self.lookahead[1] in utils.predict[rule_number]:  # selecting the appropriate production
                self.call_rule(non_terminal, rule_number)
                break
        else:  # is visited when no corresponding production was found
            if self.lookahead[2] in utils.follow[non_terminal.name]:
                if utils.TokenType.EPSILON not in utils.first[non_terminal.name]:  # missing T
                    self.syntax_errors.append(f'#{self.lookahead[0]} : Syntax Error, Missing Params')  # print error
                return  # exit
            else:  # illegal token
                self.syntax_errors.append(f'#{self.lookahead[0]} : syntax error, illegal {self.lookahead[2]}')
                self.lookahead = self.get_next_token()
                self.call_procedure(non_terminal)

    def call_rule(self, parent, rule_number):
        for part in utils.grammar[rule_number]:
            if is_non_terminal(part):
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
            self.syntax_errors.append(f'#{self.lookahead[0]} : Syntax Error, Missing Params')
