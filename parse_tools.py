import utils
from anytree import Node, RenderTree


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        utils.init_grammar()

        self.root = Node('Program')
        self.lookahead = None

    def get_next_token(self):
        token = self.scanner.get_next_token()
        while not token:  # Could've returned False due to lexical error
            token = self.scanner.get_next_token()
        return token

    def print_tree(self):
        for pre, fill, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name))

    def run(self):
        self.lookahead = self.get_next_token()
        self.call_procedure(self.root)
        self.print_tree()

    def call_procedure(self, non_terminal: Node):
        for rule_number in utils.productions[non_terminal.name]:
            if self.lookahead in utils.predict[rule_number]:  # selecting the appropriate production
                self.call_rule(non_terminal, rule_number)
                break
        else:  # is visited when no corresponding production was found
            if self.lookahead in utils.follow[non_terminal]:
                if 'EPSILON' not in utils.first[non_terminal]:  # missing T
                    pass  # TODO print error
                # TODO exit
            else:  # illegal character
                pass  # TODO print error and proceed

    def call_rule(self, parent, rule_number):
        pass

    def call_match(self, expected_token):
        pass
