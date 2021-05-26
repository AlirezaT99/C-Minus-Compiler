import utils


class CodeGenerator:
    def __init__(self):
        pass

    def call_routine(self, name):
        self.__getattribute__(name[1:])()
