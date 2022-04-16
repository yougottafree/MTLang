"""
    This file is for testing the funtion, you can ignore this
"""

from checking import *
from errors import * 

assert(validIntegerAssignment("1+2 + 3 -4 /~5", {}) == True)
assert(validIntegerAssignment("1+2 + 3 -4 /~", {}) == False)
assert(validIntegerAssignment("   1   ", {}) == True)
assert(validIntegerAssignment(" 33  ", {}) == True)


assert(validIntegerAssignment("a + b / C + dsdsdf", {"a":"int", "b":"constantInt", "C":"int", "dsdsdf":"int"}) == True)

assert(validIntegerAssignment("a+b1 * c2 ^d", {"a":"int"}) == False)


assert(validBoolean("TRUE", {}) == True)
assert(validBoolean("FALSE", {}) == True)
assert(validBoolean("1 < 3", {}) == True)
assert(validBoolean("1 >= 4", {}) == True)
assert(validBooleanAssignment("TRUE & a < d", {'a': "int", 'b': "string", 'c': "string", 'd': "real"}, True) == True)
assert(validBooleanAssignment("a & 1 + 3 < 4 + 6+7/4 | you", {"a": "bool", "you":"bool"}, True) == True)
# assert(validString("") == True)
assert(validString("\"asldjflaskdfjlkasjdflkjsd  asdlklkbn asf\t aosdiflkasdjflkja \d asdifjadslfj \n\"") == True)
assert(validString("\"bc") == False)