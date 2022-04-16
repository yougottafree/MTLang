from checking import *
from errors import * 
from main import Type

assert(validIntegerAssignment("1+2 + 3 -4 /~5", {}) == True)
try:
    validIntegerAssignment("1+2 + 3 -4 /~", {})
except MTLSyntaxError:
    pass

assert(validIntegerAssignment("a + b / C + dsdsdf", {"a":Type.Integer, "b":Type.ConstantInteger, "C":Type.Integer, "dsdsdf":Type.Integer}) == True)

try:
    assert(validIntegerAssignment("a+b1 * c2 ^d", {"a":Type.Integer}))
except MTLSyntaxError:
    pass