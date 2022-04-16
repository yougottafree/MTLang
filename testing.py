from checking import *
from errors import * 
from main import Type

assert(validIntegerAssignment("1+2 + 3 -4 /~5", {}) == True)
assert(validIntegerAssignment("1+2 + 3 -4 /~", {}) == False)
assert(validIntegerAssignment("   1   ", {}) == True)
assert(validIntegerAssignment(" 33  ", {}) == True)


assert(validIntegerAssignment("a + b / C + dsdsdf", {"a":Type.Integer, "b":Type.ConstantInteger, "C":Type.Integer, "dsdsdf":Type.Integer}) == True)

assert(validIntegerAssignment("a+b1 * c2 ^d", {"a":Type.Integer}) == False)


assert(validBoolean("TRUE", {}) == True)
assert(validBoolean("FALSE", {}) == True)
assert(validBoolean("1 < 3", {}) == True)
assert(validBoolean("1 >= 4", {}) == True)
assert(validBooleanAssignment("1 > 3 & 4 < 1", {}) == True)
assert(validBooleanAssignment("a & 1 + 3 < 4 + 6+7/4 | you", {"a": Type.Boolean, "you":Type.Boolean}, True) == True)