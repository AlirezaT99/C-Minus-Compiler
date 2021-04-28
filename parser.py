import utils
from anytree import Node, RenderTree


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.lookahead = None
        utils.init_grammar()

    def get_next_token(self):
        token = self.scanner.get_next_token()
        while not token:  # Could've returned False due to lexical error
            token = self.scanner.get_next_token()
        return token

    def run(self):
        self.lookahead = self.get_next_token()
        program = Node("Program")
        print(program)
        print(RenderTree(program))
        # self.call_procedure(program.name)

