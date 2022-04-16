"""
    Author: Tam Duong & Linh Ta (Group 21)
    This file will provide the function to verify
    that the variable is valid or not using the namespace
    and syntax validation
"""

from errors import * 


def validParentheses(line):
    """
        this function will check whether or not the parentheses
        of a statement is correct, otherwise it is invalid
        @param line: the line we want to check for balance parentheses
    """
    open = 0
    for i in range(len(line)):
        if line[i] == "(":
            open += 1
        if line[i] == ")":
            if open==0:
                return False
            open-=1
    return open == 0
    

def validString(string):
    """
        this will check whether or not a string is a valid string, 
        which is open and closed with " and contains to " inside it
        because it can make the string close earlier than intended
    """
    if len(string) < 2:
        return False
    if string[0] != "\"" or string[-1] != "\"":
        return False
    for i in range(1, len(string)-1):
        if string[i] == "\"":
            return False
    return True

def validInteger(integer):
    """
        this will check whether or not an integer is a valid integer, 
        which means it only contains digit, and may be preceeded by ~,
        which signify the negative number
    """
    i = 0
    while i < len(integer)-1 and integer[i] == "~":
        i += 1
    while i < len(integer):
        if not integer[i].isdigit():
            return False
        i+=1
    return True

def validReal(real):
    """
        this will check whether or not a number is a valid real number
        which means it is separated by a . and 2 valid integer on both side
        it can also be negative by the ~before it
    """
    splitted = real.split(".")
    if len(splitted) != 2:
        return False
    for char in splitted[1]:
        if not char.isdigit():
            return False
    return validInteger(splitted[0])

def validVariable(var):
    """
        validVariable will check whether a variable is valid,
        which means the variable only contains character
    """
    for char in var:
        if not char.isalpha():
            return False
    return True

def validStringAssignment(rightSide, nameSpace, printToErr=False):
    """
        this function will check the right side of the string assignment
        is valid string to assign
        @param rightSide:       the rightSide of the assignment
        @param nameSpace:       the namespace that contains all variable type
        @param printToErr:      Whether or not to print error to stderr
    """
    rightSide = rightSide.strip()
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
    if nameSpace[rightSide] != "string" and nameSpace[rightSide] != "constantString":
        if printToErr:
            print_error(f"{rightSide} is not String")
        return False
    return True
        
def validIntegerAssignment(rightSide, nameSpace, printToErr=False):
    """
        this function will check the right side of the integer assignment
        is valid interger to assign
        @param rightSide:       the rightSide of the assignment
        @param nameSpace:       the namespace that contains all variable type
        @param printToErr:      Whether or not to print error to stderr
    """
    rightSide = rightSide.strip()
    # check for valid parentheses
    if not validParentheses(rightSide):
        if printToErr:
            print_error(f"{rightSide} has unvalid parentheses")
        return False
    
    #check if it is already an integer
    if validInteger(rightSide):
        return True
    
    # normalize all the operation, so that we can split to get the tokens and number
    normalizeOp = rightSide.replace("-", "+").replace("*", "+").replace("/", "+").replace("%", "+").replace("^", "+").replace("(", " ").replace(")", " ")
    allElement = normalizeOp.split("+")
    
    # check each token/element to see if they are valid
    for element in allElement:
        element = element.strip()
        #check if element is already an integer
        if validInteger(element):
            continue
        elif not validVariable(element):
            # check if variable is valid
            if printToErr:
                print_error(f"{element} is not a valid variable")
            return False
        elif element not in nameSpace:
            #check if element is defined if it is variable
            if printToErr:
                print_error(f"{element} not initialized")
            return False
        elif nameSpace[element] != "int" and nameSpace[element] != "constantInt":
             # check if it is a variable  that it is an integer
            if printToErr:
                print_error(f"{element} is not integer")
            return False
    return True

def validRealAssignment(rightSide, nameSpace, printToErr=False):
    """
        this function will check the right side of the real number assignment
        is valid  or real number to assign
        @param rightSide:       the rightSide of the assignment
        @param nameSpace:       the namespace that contains all variable type
        @param printToErr:      Whether or not to print error to stderr
    """
    rightSide = rightSide.strip()
    #check if parentheses are valid
    if not validParentheses(rightSide):
        if printToErr:
            print_error(f"{rightSide} has unvalid parentheses")
        return False
    if validIntegerAssignment(rightSide, nameSpace):
        # if it is integer, it is a real number
        return True
    if validReal(rightSide):
        # check if it is already a real number
        return True
    # normalize all the operation to split to get the tokens/variable in the line
    normalizeOp = rightSide.replace("-", "+").replace("*", "+").replace("/", "+").replace("%", "+").replace("^", "+").replace("(", "").replace(")", "")
    allElement = normalizeOp.split("+")
    for element in allElement:
        element = element.strip()
        if validInteger(element):
            # if it is integer, it is a real number
            continue
        if validReal(element):
            # check if this is real number
            continue
        elif not validVariable(element):
            # if the variable is not valid, cannot do it
            if printToErr:
                print_error(f"{element} is not a valid variable")
            return False
        elif element not in nameSpace:
            # if element is not defined yet, cannot assign
            if printToErr:    
                print_error(f"{element} not initialized")
            return False
        elif nameSpace[element] != "int" and nameSpace[element] != "constantInt" \
        and nameSpace[element] != "real" and nameSpace[element] != "constantReal":
            # check if the variable is assigned to int to real
            if printToErr:
                print_error(f"{element} is not real number")
            return False
    return True

def validBoolean(boolExpress, nameSpace, printToErr=False):
    """
        this function will check if an expression is a valid boolean expression
        @param boolexpression:  the expression we want to check
        @param nameSpace:       the namespace that contains all variable type
        @param printToErr:      Whether or not to print error to stderr
    """
    # boolExpress is TRUE or FALSE
    if boolExpress == "TRUE" or boolExpress == "FALSE":
        return True
    # if bool is a variable that is bool
    if boolExpress in nameSpace and nameSpace[boolExpress] == "bool":
        return True
    # the rest should be operation between 2 elements
    if "==" in boolExpress:
        equal = True
    # normalize expression to split to get token
    normalizeEqual = boolExpress.replace("!=", "==").replace("<=", "==").replace(">=", "==").replace("<", "==").replace(">", "==")
    split = normalizeEqual.split("==")
    
    # should be between 2 elements
    if len(split) != 2:
        if printToErr:
            print_error(f"{boolExpress} is not a valid boolean expression")
        return False
    var1 = split[0].strip()
    var2 = split[1].strip()

    #check if both are valid boolean
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
    #check if var1 and var2 are initialized variable 
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
    #check if var1 and var2 are both boolean
    if nameSpace[var1] == "bool" and nameSpace[var2] == "bool":
        return True
    return False
        

def stripNot(element):
    """
        stripNot(element) will strip all the not that is at the beginning
        of the boolean expression
    """
    i = 0
    while i < len(element) and element[i] == "!":
        i += 1
    return element[i:]

def validBooleanAssignment(expression, nameSpace, printToErr=False):
    """
        this function will check the expression of the boolean assignment
        is valid boolean to assign
        @param expression:      the expression to consider
        @param nameSpace:       the namespace that contains all variable type
        @param printToErr:      Whether or not to print error to stderr
    """
    #check for parentheses
    if not validParentheses(expression):
        if printToErr:
            print_error(f"{expression} has unvalid parentheses")
        return False
    #check if it is a valid boolean expression
    if validBoolean(expression, nameSpace):
        return True
    # normalize operation to split for token
    normalizeOp = expression.replace("|", "&")
    allElement = normalizeOp.split("&")
    for element in allElement:
        # check tokens to see if they are valid
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
            # check if variable is valid
            if printToErr:
                print_error(f"{element} is not a valid variable")
            return False
        elif element not in nameSpace:
            #check if element is initialized
            if printToErr:    
                print_error(f"{element} not initialized")
            return False
        elif nameSpace[element] != "bool":
            # check if the variable is a boolean
            if printToErr:
                print_error(f"{element} is not boolean")
            return False
    return True
    

    