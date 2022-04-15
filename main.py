import sys
import enum

class Type(enum.Enum):
    String = 1
    Integer = 2
    Real = 3
    Boolean = 4
    ConstantString = 5
    ConstantInteger = 6
    ConstantReal = 7


class MTLSyntaxError(Exception):
    def __init__(self, line, message="SYNTAX ERROR"):
        self.line = line
        self.message = f"{line}:{message}"
        super().__init__(self.message)

class MTLVariableNotInitialized(Exception):
    def __init__(self, variable):
        self.message = f"{variable} not initialized"
        super().__init__(self.message)


def main():
    fileName = sys.argv[1]
    file = open(fileName, 'r')
    fileLines = file.readlines()
    file.close()
    readFile(file)

def validString(str):
    if str[0] != "\"" or str[-1] != "\"":
        return False
    for i in range(1, len(str)-1):
        if str[i] == "\"":
            return False
    return True

def validInteger(integer):
    i = 0
    while i < len(integer)-1 and integer[i] == "~":
        i += 1
    while i < len(integer):
        if not integer[i].isdigit():
            return False
        i+=1
    return True

def validReal(real):
    splitted = real.split(".")
    if len(splitted) != 2:
        return False
    return validInteger(splitted[0]) and validInteger(splitted[1])

def validVariable(var):
    for char in var:
        if not char.isalpha():
            return False
    return True

def validStringAssignment(rightSide, nameSpace):
    if validString(rightSide):
        return True
    if not validVariable(rightSide):
        raise MTLSyntaxError(rightSide, "is not a valid variable")
    if rightSide not in nameSpace:
        raise MTLVariableNotInitialized(rightSide)
    if nameSpace[rightSide] != Type.String or nameSpace[rightSide] != Type.ConstantString:
        raise MTLSyntaxError(rightSide, "is not String")
    return True
        
def validIntegerAssignment(rightSide, nameSpace):
    if isValidInteger(rightSide):
        return True
    normalizeOp = rightSide.replace("-", "+").replace("*", "+").replace("/", "+").replace("%", "+").replace("^", "+")
    allElement = normalizeOp.split("+")
    for element in allElement:
        error = False
        if not validInteger(element):
            error = True
            break
        if element

def handleAssignment(line, tabCount):
    lineSplited = line.split("->", 1)
    



def handlePrint(line, tabCount):
    tabs = '\t'*tabCount
    print(f"{tabs}print({line[4:len(line)-1]})")

def handleLine(file, lineNumber, tabCount):
    

def readFile(file):
    tabCount = 0
    nameSpace = {}
    for i in range(len(file)):
        line = file[i].strip()
        if not line:
            continue
        
    

if __name__ == "__main__":
    main()