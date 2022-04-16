import sys

def print_error(message):
    print(message, file=sys.stderr)


class MTLSyntaxError(Exception):
    def __init__(self, line, message="SYNTAX ERROR"):
        self.line = line
        self.message = f"{line}:{message}"
        super().__init__(self.message)

class MTLVariableNotInitialized(Exception):
    def __init__(self, variable):
        self.message = f"{variable} not initialized"
        super().__init__(self.message)