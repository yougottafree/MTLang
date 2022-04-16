from errors import * 
from main import Type

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
    for char in splitted[1]:
        if not char.isdigit():
            return False
    return validInteger(splitted[0])

def validVariable(var):
    for char in var:
        if not char.isalpha():
            return False
    return True

def validStringAssignment(rightSide, nameSpace, printToErr=False):
    if validString(rightSide):
        return True
    if not validVariable(rightSide):
        if printToErr:
            print_error(f"{rightSide} is not a valid variable")
        return False
    if rightSide not in nameSpace:
        if printToErr:
            print_error(f"{rightSide} not initialized")
        return False
    if nameSpace[rightSide] != Type.String or nameSpace[rightSide] != Type.ConstantString:
        if printToErr:
            print_error(f"{rightSide} is not String")
        return False
    return True
        
def validIntegerAssignment(rightSide, nameSpace, printToErr=False):
    if validInteger(rightSide):
        return True
    normalizeOp = rightSide.replace("-", "+").replace("*", "+").replace("/", "+").replace("%", "+").replace("^", "+").replace("(", "").replace(")", "")
    allElement = normalizeOp.split("+")
    for element in allElement:
        element = element.strip()
        if validInteger(element):
            continue
        elif not validVariable(element):
            if printToErr:
                print_error(f"{element} is not a valid variable")
        elif element not in nameSpace:
            if printToErr:
                print_error(f"{element} not initialized")
            return False
        elif nameSpace[element] != Type.Integer and nameSpace[element] != Type.ConstantInteger:
            if printToErr:
                print_error(f"{element} is not integer")
            return False
    return True

def validRealAssignment(rightSide, nameSpace, printToErr=False):
    if validInteger(rightSide):
        return True
    normalizeOp = rightSide.replace("-", "+").replace("*", "+").replace("/", "+").replace("%", "+").replace("^", "+").replace("(", "").replace(")", "")
    allElement = normalizeOp.split("+")
    for element in allElement:
        element = element.strip()
        if validInteger(element):
            continue
        elif not validVariable(element):
            if printToErr:
                print_error(f"{element} is not a valid variable")
            return False
        elif element not in nameSpace:
            if printToErr:    
                print_error(f"{element} not initialized")
            return False
        elif nameSpace[element] != Type.Integer and nameSpace[element] != Type.ConstantInteger \
        and nameSpace[element] != Type.Real and nameSpace[element] != Type.ConstantReal:
            if printToErr:
                print_error(f"{element} is not real number")
            return False
    return True

def validBoolean(boolExpress, nameSpace, printToErr=False):
    if boolExpress == "TRUE" or boolExpress == "FALSE":
        return True
    # the rest should be operation between 2 elements
    if "==" in boolExpress:
        equal = True
    normalizeEqual = boolExpress.replace("<=", "==").replace(">=", "==").replace("<", "==").replace(">", "==")
    split = boolExpress.split("==")
    if len(split) != 2:
        print_error(f"{boolExpress} is not a valid boolean expression")
    var1 = split[0].strip()
    var2 = split[1].strip()
    if var1 in ["TRUE", "FALSE"] and var2 in ["TRUE", "FALSE"]:
        return True
    if validRealAssignment(var1, nameSpace) and validRealAssignment(var2, nameSpace):
        return True
    if validStringAssignment(var1, nameSpace) and validStringAssignment(var2, nameSpace):
        return equal
    if not validVariable(var1):
        if printToErr:
            print_error(f"{var1} is not a valid variable")
        return False
    if not validVariable(var2):
        if printToErr:
            print_error(f"{var2} is not a valid variable")
        return False
    if var1 not in nameSpace:
        if printToErr:
            print_error(f"{var1} not initialized")
        return False
    if var2 not in nameSpace:
        if printToErr:
            print_error(f"{var2} not initialized")
        return False
    if nameSpace[var1] == Type.Boolean and nameSpace[var2] == Type.Boolean:
        return True
    return False
        
def stripNot(element):
    i = 0
    while i < len(element) and element[i] == "!":
        i += 1
    return element[i:]

def validBooleanAssignment(expression, printToErr=False):
    if validBoolean(expression):
        return True
    normalizeOp = boolExpress.replace("|", "&")
    allElement = boolExpress.split("&")
    for element in allElement:
        element = element.strip()
        newElement = stripNot(element)
        if not newElement:
            if printToErr:
                print_error(f"{element} is not a valid boolean")
            return False
        element = newElement
        if validBoolean(element, nameSpace):
            continue
        elif not validVariable(element):
            if printToErr:
                print_error(f"{element} is not a valid variable")
            return False
        elif element not in nameSpace:
            if printToErr:    
                print_error(f"{element} not initialized")
            return False
        elif nameSpace[element] != Type.Boolean:
            if printToErr:
                print_error(f"{element} is not real number")
            return False
    return True
    