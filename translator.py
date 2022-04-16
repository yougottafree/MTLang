"""
    Author: Tam Duong & Linh Ta (Group 21)
    
    This project will implement MTLang, which is a language we have created
    to run the program run the command
    
        python translator.py <input_file> > <output_python_file>

    which will generate a python file, which you can run by 

        python <output_python_file>

    The command line arguments support valid syntax for variable assignment,
    so if you want to pass in variable, do it like this
    
        python translator.py <input_file> <variable_assignment> <variable_assignment> ...

    where <variable_assignment> must be valid variable assignments inside "" like. 

    Example:    python main.py trial "var_int a -> 6" "var_int b -> 10" "var_int m -> 1950" > result.py

"""

import sys
from checking import * 
from errors import MTLSyntaxError, MTLRuntimeError

def main():
    if len(sys.argv) < 2:
        raise Exception("Please provide an input file")
    fileName = sys.argv[1]
    file = open(fileName, 'r')
    fileLines = file.readlines()
    file.close()
    nameSpace = {}
    addCommandLineArgument(nameSpace)
    readFile(fileLines, nameSpace)

def addCommandLineArgument(nameSpace):
    """
        this function will add all the commandline assignment
        @param nameSpace:   nameSpace is namespace of all the variable
    """
    for assignment in sys.argv[2:]:
        handleAssignment(assignment, nameSpace, 0)

def assignVariableInteger(line, nameSpace, tabCount, constant=False):
    """
        this function will perform the assignment of an integer into the
        variable
        @param line:        the line that can assign variable
        @param nameSpace:   the nameSpace of all the variable
        @param tabCount:    the count of Tabs that should be add to Python
        @param constant:    whether or not it is a constant assignment
    """
    # split variable between the first -> 
    lineSplit = line.split("->", 1)
    if len(lineSplit) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax, , did you use '=' instead of '->'?")
    firstPart = lineSplit[0].split()
    if len(firstPart) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    # check if the assignment is a valid integer assignment
    assignment = lineSplit[1].strip()
    if not validIntegerAssignment(assignment, nameSpace, printToErr = True):
        raise MTLSyntaxError(assignment, "assignment value is not integer")
    
    #check if var is not assigned constant before
    var = firstPart[1].strip()
    if not validVariable(var):
        raise MTLSyntaxError(line, f"{var} is not a valid variable")
    varType = nameSpace.get(var, "None")
    if varType in ["constantInt", "constantReal", "constantString"] :
        raise MTLRuntimeError(f"{var} is constant, cannot reassign")
    
    # assign the variable to the type
    if not constant:
        nameSpace[var] = "int"
    else:
        nameSpace[var] = "constantInt"
    
    # convert from MTLang to Python Syntax
    assignment = assignment.replace("~", "-").replace("^", "**").replace("/", "//")
    tabs = '\t' * tabCount
    print(f"{tabs}{var} = {assignment}")


def assignVariableReal(line, nameSpace, tabCount, constant=False):
    """
        this function will perform the assignment of an real number into the
        variable
        @param line:        the line that can assign variable
        @param nameSpace:   the nameSpace of all the variable
        @param tabCount:    the count of Tabs that should be add to Python
        @param constant:    whether or not it is a constant assignment
    """
    #split between the first -> 
    lineSplit = line.split("->", 1)
    if len(lineSplit) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax, , did you use '=' instead of '->'?")
    firstPart = lineSplit[0].split()
    if len(firstPart) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    
    # check for assignment
    assignment = lineSplit[1].strip()
    if not validRealAssignment(assignment, nameSpace, printToErr = True):
        raise MTLSyntaxError(assignment, "assignment value is not real number")
    var = firstPart[1].strip()
    if not validVariable(var):
        raise MTLSyntaxError(line, f"{var} is not a valid variable")

    # make sure the variable is constant
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
    """
        this function will perform the assignment of an string into the
        variable
        @param line:        the line that can assign variable
        @param nameSpace:   the nameSpace of all the variable
        @param tabCount:    the count of Tabs that should be add to Python
        @param constant:    whether or not it is a constant assignment
    """
    # split between first -> 
    lineSplit = line.split("->", 1)
    if len(lineSplit) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax, did you use '=' instead of '->'?")
    firstPart = lineSplit[0].split()
    if len(firstPart) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")
    
    # check if assignment is correct
    assignment = lineSplit[1].strip()
    if not validStringAssignment(assignment, nameSpace, printToErr = True):
        raise MTLSyntaxError(assignment, "assignment value is not String")
    var = firstPart[1].strip()
    if not validVariable(var):
        raise MTLSyntaxError(line, f"{var} is not a valid variable")

    #check if variable is already assigned constant
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
    """
        this function will perform the assignment of an boolean into the
        variable
        @param line:        the line that can assign variable
        @param nameSpace:   the nameSpace of all the variable
        @param tabCount:    the count of Tabs that should be add to Python
        @param constant:    whether or not it is a constant assignment
    """
    #split at first -> 
    lineSplit = line.split("->", 1)
    if len(lineSplit) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax, did you use '=' instead of '->'?")
    firstPart = lineSplit[0].split()
    if len(firstPart) != 2:
        raise MTLSyntaxError(line, "wrong assignment syntax")

    #check if assignment is valid
    assignment = lineSplit[1].strip()
    if not validBooleanAssignment(assignment, nameSpace, printToErr = True):
        raise MTLSyntaxError(assignment, "assignment value is not valid boolean expression")
    
    #check if varible is already assigned to constant
    var = firstPart[1].strip()

    if not validVariable(var):
        raise MTLSyntaxError(line, f"{var} is not a valid variable")

    varType = nameSpace.get(var, "None")
    if varType in ["constantInt", "constantReal", "constantString"] :
        raise MTLRuntimeError(f"{var} is constant, cannot reassign")
    nameSpace[var] = "bool"
    assignment = assignment.replace("!", " not ").replace("&", " and ").replace("|", " or ").replace("~", "-").replace("^", "**").replace("TRUE", "True").replace("FALSE", "False")
    tabs = '\t' * tabCount
    print(f"{tabs}{var} = {assignment}")

def handleWhile(line, nameSpace, tabCount):
    """
        this function will perform the check and convert of while loop
        from MTLang to Python
        @param line:        the line that represent the while loop in MTLang
        @param nameSpace:   the nameSpace of all the variable
        @param tabCount:    the count of Tabs that should be add to Python
    """
    line = line.strip()
    splited = line.split()
    
    # check if while is valid
    if len(splited) < 3 or splited[0] != "while" or splited[-1] != "do":
        raise MTLSyntaxError(line, "wrong while syntax")
    
    # check if the condition in while is valid boolean assignment
    condition = line[5:len(line)-3].strip()
    if not validBooleanAssignment(condition, nameSpace):
        raise MTLSyntaxError(line, f"{condition} is not valid boolean expression")
    condition = condition.replace("!", " not ").replace("&", " and ").replace("|", " or ").replace("~", "-").replace("^", "**").replace("TRUE", "True").replace("FALSE", "False")
    tabs = '\t' * tabCount
    print(f"{tabs}while {condition}:")

def handleIf(line, nameSpace, tabCount):
    """
        this function will perform the check and convert of if statement
        from MTLang to Python
        @param line:        the line that represent the if statement in MTLang
        @param nameSpace:   the nameSpace of all the variable
        @param tabCount:    the count of Tabs that should be add to Python
    """
    line = line.strip()
    splited = line.split()
    # check if while is valid
    if len(splited) < 3 or splited[0] != "if" or splited[-1] != "do":
        raise MTLSyntaxError(line, "wrong if syntax")
    condition = line[2:len(line)-3].strip()
    
    # check if the condition in while is valid boolean assignment
    if not validBooleanAssignment(condition, nameSpace):
        raise MTLSyntaxError(line, f"{condition} is not valid boolean expression")
    condition = condition.replace("!", " not ").replace("&", " and ").replace("|", " or ").replace("~", "-").replace("^", "**").replace("TRUE", "True").replace("FALSE", "False")
    tabs = '\t' * tabCount
    print(f"{tabs}if {condition}:")

def handleElse(line, nameSpace, tabCount):
    """
        this function will perform the check and convert else statement
        from MTLang to Python
        @param line:        the line that represent the else statement in MTLang
        @param nameSpace:   the nameSpace of all the variable
        @param tabCount:    the count of Tabs that should be add to Python
    """
    line = line.strip()
    if " ".join(line.split()) != "else do":
        raise MTLSyntaxError(line, "wrong syntax for else")
    tabs = '\t' * tabCount
    print(f"{tabs}else:")

def handlePrint(line, tabCount):
    """
        this function will perform the check and convert print statement
        from MTLang to Python
        @param line:        the line that represent the print in MTLang
        @param tabCount:    the count of Tabs that should be add to Python
    """
    tabs = '\t'*tabCount
    print(f"{tabs}print({line[4:len(line)-1]}, end=\"\")")

def handleAssignment(line, nameSpace, tabCount):
    """
        this function will route the variable assignment to the appropriate
        assignment handler
        @param line:        the line that represent the assignment in MTLang
        @param nameSpace:   the nameSpace of all the variable
        @param tabCount:    the count of Tabs that should be added to Python
    """
    if line[:7] == "var_int":
        assignVariableInteger(line, nameSpace, tabCount)
    elif line[:8] == "var_real":
        assignVariableReal(line, nameSpace, tabCount)
    elif line[:7] == "var_str":
        assignVariableString(line, nameSpace, tabCount)
    elif line[:9] == "const_int":
        assignVariableInteger(line, nameSpace, tabCount, constant=True)
    elif line[:10] == "const_real":
        assignVariableReal(line, nameSpace, tabCount, constant=True)
    elif line[:8] == "var_bool":
        assignVariableBool(line, nameSpace, tabCount)
    else:
        raise MTLSyntaxError(line, "cannot find that assignment syntax")

def readFile(file, nameSpace):
    """
        this function will route the line in the file to the appropriate
        handler to convert to Python syntax
        @param file:        the file of MTLang we want to convert to Python
        @param nameSpace:   the nameSpace of all the variable
        @param tabCount:    the count of Tabs that should be added to Python
    """
    indentStack = []
    for i in range(len(file)):
        line = file[i].strip()
        if not line:
            continue
        if line[0] == "$":
            print(line.replace("$", "#", 1))
        elif line[:2] == "if":
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
        elif line[:3] == "var":
            handleAssignment(line, nameSpace, len(indentStack))
        elif line[:3] == "out":
            handlePrint(line, len(indentStack))
        else:
            raise MTLSyntaxError(line, "Cannot determine what this does")
    
    if indentStack:
        raise MTLSyntaxError("", "forgot to add end to an if or while block")

if __name__ == "__main__":
    main()
