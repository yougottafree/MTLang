import sys

class MTLSyntaxException(Exception):
    def __init__(self, line, message="SYNTAX ERROR"):
        self.line = line
        self.message = "{line}:{message}"
        super().__init__(self.message)

def main():
    fileName = sys.argv[1]
    try:
        file = open(fileName, 'r')
    except FileNotFoundError:
        print(f"Cannot find file {fileName}")
        sys.exit(1)
    readFile(file)


def handleAssignment(line):
    

def readFile(file):
    for inputLine in file.readlines():
        line = inputLine.strip()
        if not line:
            continue
        if "->" in line:
            handleAssignment(line)
    

if __name__ == "__main__":
    main()