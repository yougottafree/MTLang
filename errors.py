"""
    Author: Tam Duong & Linh Ta (Group 21)
    This file will define the errors and the printing of error
    to stderr
"""

import sys

def print_error(message):
    """
        this function will print the message to the stderr
    """
    print(f"ERROR: {message}", file=sys.stderr)


class MTLSyntaxError(Exception):
    def __init__(self, line, message="SYNTAX ERROR"):
        self.line = line
        self.message = f"{line}:{message}"
        super().__init__(self.message)

class MTLVariableNotInitialized(Exception):
    def __init__(self, variable):
        self.message = f"{variable} not initialized"
        super().__init__(self.message)

class MTLRuntimeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)