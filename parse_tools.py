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

        self.print_tree()
        self.call_procedure(self.root)

    def call_procedure(self, non_terminal):
        # productions =
        pass

    def call_match(self, expected_token):
        pass
