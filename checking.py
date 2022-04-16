from errors import * 

def validParentheses(line):
    open = 0
    for i in range(len(line)):
        if line[i] == "(":
            open.append(i)
        if line[i] == ")":
            if open==0:
                return False
            open-=1
    return open == 0
    

def validString(string):
    if len(string) < 2:
        return False
    if string[0] != "\"" or string[-1] != "\"":
        return False
    for i in range(1, len(string)-1):
        if string[i] == "\"":
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
    if nameSpace[rightSide] != "string" or nameSpace[rightSide] != "constantString":
        if printToErr:
            print_error(f"{rightSide} is not String")
        return False
    return True
        
def validIntegerAssignment(rightSide, nameSpace, printToErr=False):
    if not validParentheses(rightSide):
        if printToErr:
            print_error(f"{rightSide} has unvalid parentheses")
        return False
    if validInteger(rightSide):
        return True
    normalizeOp = rightSide.replace("-", "+").replace("*", "+").replace("/", "+").replace("%", "+").replace("^", "+").replace("(", " ").replace(")", " ")
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
        elif nameSpace[element] != "int" and nameSpace[element] != "constantInt":
            if printToErr:
                print_error(f"{element} is not integer")
            return False
    return True

def validRealAssignment(rightSide, nameSpace, printToErr=False):
    if not validParentheses(rightSide):
        if printToErr:
            print_error(f"{rightSide} has unvalid parentheses")
        return False
    if validIntegerAssignment(rightSide, nameSpace):
        return True
    if validReal(rightSide):
        return True
    normalizeOp = rightSide.replace("-", "+").replace("*", "+").replace("/", "+").replace("%", "+").replace("^", "+").replace("(", "").replace(")", "")
    allElement = normalizeOp.split("+")
    for element in allElement:
        element = element.strip()
        if validInteger(element):
            continue
        if validReal(element):
            continue
        elif not validVariable(element):
            if printToErr:
                print_error(f"{element} is not a valid variable")
            return False
        elif element not in nameSpace:
            if printToErr:    
                print_error(f"{element} not initialized")
            return False
        elif nameSpace[element] != "int" and nameSpace[element] != "constantInt" \
        and nameSpace[element] != "real" and nameSpace[element] != "constantReal":
            if printToErr:
                print_error(f"{element} is not real number")
            return False
    return True

def validBoolean(boolExpress, nameSpace, printToErr=False):
    if boolExpress == "TRUE" or boolExpress == "FALSE":
        return True
    if boolExpress in nameSpace and nameSpace[boolExpress] == "bool":
        return True
    # the rest should be operation between 2 elements
    if "==" in boolExpress:
        equal = True
    normalizeEqual = boolExpress.replace("!=", "==").replace("<=", "==").replace(">=", "==").replace("<", "==").replace(">", "==")
    split = normalizeEqual.split("==")
    if len(split) != 2:
        if printToErr:
            print_error(f"{boolExpress} is not a valid boolean expression")
        return False
    var1 = split[0].strip()
    var2 = split[1].strip()
    if var1 in ["TRUE", "FALSE"] and var2 in ["TRUE", "FALSE"]:
        return True
    if validRealAssignment(var1, nameSpace) and validRealAssignment(var2, nameSpace):
        return True
    if validStringAssignment(var1, nameSpace) and validStringAssignment(var2, nameSpace):
        return equal
    if var1 in ["TRUE", "FALSE"]:
        return validBoolean(var2, nameSpace)
    if var2 in ["TRUE", "FALSE"]:
        return validBoolean(var1, nameSpace)
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
    if nameSpace[var1] == "bool" and nameSpace[var2] == "bool":
        return True
    return False
        
def stripNot(element):
    i = 0
    while i < len(element) and element[i] == "!":
        i += 1
    return element[i:]

def validBooleanAssignment(expression, nameSpace, printToErr=False):
    if not validParentheses(expression):
        if printToErr:
            print_error(f"{expression} has unvalid parentheses")
        return False
    if validBoolean(expression, nameSpace):
        return True
    normalizeOp = expression.replace("|", "&")
    allElement = normalizeOp.split("&")
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
        elif nameSpace[element] != "bool":
            if printToErr:
                print_error(f"{element} is not real number")
            return False
    return True
    

    