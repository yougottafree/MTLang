import sys
import enum
from checking import * 
from errors import MTLSyntaxError, MTLVariableNotInitialized, MTLRuntimeError

# class Type(enum.Enum):
#     String = 1
#     Integer = 2
#     Real = 3
#     Boolean = 4
#     ConstantString = 5
#     ConstantInteger = 6
#     ConstantReal = 7

def main():
    if len(sys.argv) < 2:
        raise Exception("Please provide an input file")
    fileName = sys.argv[1]
    file = open(fileName, 'r')
    fileLines = file.readlines()
    file.close()
    readFile(fileLines)
    nameSpace = {}
    assignVariableInteger("var_int a -> 0", nameSpace, 0)
    assignVariableString("var_str b -> \"slkdfjslkdj\"", nameSpace, 0)
    assignVariableReal("var_real d -> ~5.0", nameSpace, 2)
    assignVariableBool("var_bool c -> TRUE & a < d", nameSpace, 0)
    print(nameSpace)

def assignVariableInteger(line, nameSpace, tabCount):
    lineSplit = line.split("->", 1)
    if len(lineSplit) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    firstPart = lineSplit[0].split()
    if len(firstPart) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    assignment = lineSplit[1].strip()
    if not validIntegerAssignment(assignment, nameSpace, printToErr = True):
        raise MTLSyntaxError(assignment, "assignment value is not integer")
    var = firstPart[1].strip()
    varType = nameSpace.get(var, None)
    if varType in ["constantInt", "constantReal", "constantString"] :
        raise MTLRuntimeError(f"{var} is constant, cannot reassign")
    nameSpace[var] = "int"
    tabs = '\t' * tabCount
    print(f"{tabs}{var} = {assignment}")


def assignVariableReal(line, nameSpace, tabCount):
    lineSplit = line.split("->", 1)
    if len(lineSplit) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    firstPart = lineSplit[0].split()
    if len(firstPart) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    assignment = lineSplit[1].strip()
    if not validRealAssignment(assignment, nameSpace, printToErr = True):
        raise MTLSyntaxError(assignment, "assignment value is not real number")
    var = firstPart[1].strip()
    varType = nameSpace.get(var, None)
    if varType in ["constantInt", "constantReal", "constantString"]  :
        raise MTLRuntimeError(f"{var} is constant, cannot reassign")
    assignment = assignment.replace("~", "-").replace("^", "**")
    nameSpace[var] = "real"
    tabs = '\t' * tabCount
    print(f"{tabs}{var} = {assignment}")

def assignVariableString(line, nameSpace, tabCount):
    lineSplit = line.split("->", 1)
    if len(lineSplit) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    firstPart = lineSplit[0].split()
    if len(firstPart) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    assignment = lineSplit[1].strip()
    if not validStringAssignment(assignment, nameSpace, printToErr = True):
        raise MTLSyntaxError(assignment, "assignment value is not String")
    var = firstPart[1].strip()
    varType = nameSpace.get(var, None)
    if varType in ["constantInt", "constantReal", "constantString"] :
        raise MTLRuntimeError(f"{var} is constant, cannot reassign")
    nameSpace[var] = "string"
    tabs = '\t' * tabCount
    print(f"{tabs}{var} = {assignment}")

def assignVariableBool(line, nameSpace, tabCount):
    lineSplit = line.split("->", 1)
    if len(lineSplit) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    firstPart = lineSplit[0].split()
    if len(firstPart) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    assignment = lineSplit[1].strip()
    if not validBooleanAssignment(assignment, nameSpace, printToErr = True):
        raise MTLSyntaxError(assignment, "assignment value is not valid boolean expression")
    var = firstPart[1].strip()
    varType = nameSpace.get(var, None)
    if varType in ["constantInt", "constantReal", "constantString"] :
        raise MTLRuntimeError(f"{var} is constant, cannot reassign")
    nameSpace[var] = "bool"
    tabs = '\t' * tabCount
    print(f"{tabs}{var} = {assignment}")

    

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