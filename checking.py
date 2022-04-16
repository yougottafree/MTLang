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

def validStringAssignment(rightSide, nameSpace):
    if validString(rightSide):
        return True
    if not validVariable(rightSide):
        raise MTLSyntaxError(rightSide, "is not a valid variable")
        return False
    if rightSide not in nameSpace:
        raise MTLVariableNotInitialized(rightSide)
        return False
    if nameSpace[rightSide] != Type.String or nameSpace[rightSide] != Type.ConstantString:
        raise MTLSyntaxError(rightSide, "is not String")
        return False
    return True
        
def validIntegerAssignment(rightSide, nameSpace):
    if validInteger(rightSide):
        return True
    normalizeOp = rightSide.replace("-", "+").replace("*", "+").replace("/", "+").replace("%", "+").replace("^", "+").replace("(", "").replace(")", "")
    allElement = normalizeOp.split("+")
    for element in allElement:
        element = element.strip()
        if validInteger(element):
            continue
        elif not validVariable(element):
            raise MTLSyntaxError(element, "is not a valid variable")
        elif element not in nameSpace:
            raise MTLVariableNotInitialized(element)
            return False
        elif nameSpace[element] != Type.Integer and nameSpace[element] != Type.ConstantInteger:
            raise MTLSyntaxError(element, "is not an integer")
            return False
    return True

def validRealAssignment(rightSide, nameSpace):
    if validInteger(rightSide):
        return True
    normalizeOp = rightSide.replace("-", "+").replace("*", "+").replace("/", "+").replace("%", "+").replace("^", "+").replace("(", "").replace(")", "")
    allElement = normalizeOp.split("+")
    for element in allElement:
        element = element.strip()
        if validInteger(element):
            continue
        elif not validVariable(element):
            raise MTLSyntaxError(element, "is not a valid variable")
        elif element not in nameSpace:
            raise MTLVariableNotInitialized(element)
            return False
        elif nameSpace[element] != Type.Integer and nameSpace[element] != Type.ConstantInteger \
        and nameSpace[element] != Type.Real and nameSpace[element] != Type.ConstantReal:
            raise MTLSyntaxError(element, "is not a real number")
            return False
    return True
