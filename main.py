import sys
import enum
from checking import * 
from errors import MTLSyntaxError, MTLVariableNotInitialized

class Type(enum.Enum):
    String = 1
    Integer = 2
    Real = 3
    Boolean = 4
    ConstantString = 5
    ConstantInteger = 6
    ConstantReal = 7

def main():
    if len(sys.argv) < 2:
        raise Exception("Please provide an input file")
    fileName = sys.argv[1]
    file = open(fileName, 'r')
    fileLines = file.readlines()
    file.close()
    readFile(fileLines)
    print(validIntegerAssignment(" 1 + 2 + a", {"a":Type.Real}))

def handleAssignment(line, tabCount):
    lineSplited = line.split("->", 1)
    



def handlePrint(line, tabCount):
    tabs = '\t'*tabCount
    print(f"{tabs}print({line[4:len(line)-1]})")

# def handleLine(file, lineNumber, tabCount):
    

def readFile(file):
    tabCount = 0
    nameSpace = {}
    for i in range(len(file)):
        line = file[i].strip()
        if not line:
            continue
        
    

if __name__ == "__main__":
    main()