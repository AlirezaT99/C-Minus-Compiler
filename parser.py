import utils


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.lookahead = None
        utils.init_grammar()

    def run(self):
        pass
