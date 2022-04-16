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
    # nameSpace = {}
    # assignVariableInteger("var_int a -> 0", nameSpace, 0)
    # assignVariableString("var_str b -> \"slkdfjslkdj\"", nameSpace, 0)
    # assignVariableReal("var_real d -> ~5.0", nameSpace, 2)
    # assignVariableBool("var_bool c -> TRUE & a < d", nameSpace, 0)
    # handleWhile("while a < ~0^30 | !(10 > d) do", nameSpace, 0)
    # handleElse("else do" , nameSpace, 0)
    # print(nameSpace)

def assignVariableInteger(line, nameSpace, tabCount, constant=False):
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
    varType = nameSpace.get(var, "None")
    if varType in ["constantInt", "constantReal", "constantString"] :
        raise MTLRuntimeError(f"{var} is constant, cannot reassign")
    if not constant:
        nameSpace[var] = "int"
    else:
        nameSpace[var] = "constantInt"
    assignment = assignment.replace("~", "-").replace("^", "**").replace("/", "//")
    tabs = '\t' * tabCount
    print(f"{tabs}{var} = {assignment}")


def assignVariableReal(line, nameSpace, tabCount, constant=False):
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
    varType = nameSpace.get(var, "None")
    if varType in ["constantInt", "constantReal", "constantString"]  :
        raise MTLRuntimeError(f"{var} is constant, cannot reassign")
    assignment = assignment.replace("~", "-").replace("^", "**")
    if not constant:
        nameSpace[var] = "real"
    else:
        nameSpace[var] = "constantReal"
    tabs = '\t' * tabCount
    print(f"{tabs}{var} = {assignment}")

def assignVariableString(line, nameSpace, tabCount, constant=False):
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
    varType = nameSpace.get(var, "None")
    if varType in ["constantInt", "constantReal", "constantString"] :
        raise MTLRuntimeError(f"{var} is constant, cannot reassign")
    if not constant:
        nameSpace[var] = "string"
    else:
        nameSpace[var] = "constantString"
    
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
    varType = nameSpace.get(var, "None")
    if varType in ["constantInt", "constantReal", "constantString"] :
        raise MTLRuntimeError(f"{var} is constant, cannot reassign")
    nameSpace[var] = "bool"
    assignment = assignment.replace("!", " not ").replace("&", " and ").replace("|", " or ").replace("~", "-").replace("^", "**")
    tabs = '\t' * tabCount
    print(f"{tabs}{var} = {assignment}")

def handleWhile(line, nameSpace, tabCount):
    line = line.strip()
    splited = line.split()
    if len(splited) < 3 or splited[0] != "while" or splited[-1] != "do":
        raise MTLSyntaxError(line, "wrong while syntax")
    condition = line[5:len(line)-3].strip()
    if not validBooleanAssignment(condition, nameSpace):
        raise MTLSyntaxError(line, "condition is not valid boolean expression")
    condition = condition.replace("!", " not ").replace("&", " and ").replace("|", " or ").replace("~", "-").replace("^", "**")
    tabs = '\t' * tabCount
    print(f"{tabs}while {condition}:")

def handleIf(line, nameSpace, tabCount):
    line = line.strip()
    splited = line.split()
    if len(splited) < 3 or splited[0] != "if" or splited[-1] != "do":
        raise MTLSyntaxError(line, "wrong if syntax")
    condition = line[5:len(line)-3].strip()
    if not validBooleanAssignment(condition, nameSpace):
        raise MTLSyntaxError(line, "condition is not valid boolean expression")
    condition = condition.replace("!", " not ").replace("&", " and ").replace("|", " or ").replace("~", "-").replace("^", "**")
    tabs = '\t' * tabCount
    print(f"{tabs}if {condition}:")

def handleElse(line, nameSpace, tabCount):
    line = line.strip()
    if " ".join(line.split()) != "else do":
        raise MTLSyntaxError(line, "wrong syntax for else")
    tabs = '\t' * tabCount
    print(f"{tabs}else:")

def handlePrint(line, tabCount):
    tabs = '\t'*tabCount
    print(f"{tabs}print({line[4:len(line)-1]})")

# def handleLine(file, lineNumber, tabCount):
    

def readFile(file):
    indentStack = []
    nameSpace = {}
    for i in range(len(file)):
        line = file[i].strip()
        if not line:
            continue
        if line[:2] == "if":
            handleIf(line, nameSpace, len(indentStack))
            indentStack.append("if")
        elif line[:5] == "while":
            handleWhile(line, nameSpace, len(indentStack))
            indentStack.append("while")
        elif line[:4] == "else":
            if len(indentStack) == 0 or indentStack[-1] != "if":
                raise MTLSyntaxError(line, "No if block to call else")
            handleElse(line, nameSpace, len(indentStack)-1)
        elif line[:3] == "end":
            if len(indentStack) == 0:
                raise MTLRuntimeError("No if or while block to end")
            indentStack.pop()
        elif line[:7] == "var_int":
            assignVariableInteger(line, nameSpace, len(indentStack))
        elif line[:8] == "var_real":
            assignVariableReal(line, nameSpace, len(indentStack))
        elif line[:7] == "var_str":
            assignVariableString(line, nameSpace, len(indentStack))
        elif line[:9] == "const_int":
            assignVariableInteger(line, nameSpace, len(indentStack), constant=True)
        elif line[:10] == "const_real":
            assignVariableReal(line, nameSpace, len(indentStack), constant=True)
        elif line[:3] == "out":
            handlePrint(line, len(indentStack))
        else:
            raise MTLSyntaxError(line, "Cannot determine what this does")

if __name__ == "__main__":
    main()

#TODO: string " inside
#TODO: Boolean transform to python
#TODO: check for valid parentheses