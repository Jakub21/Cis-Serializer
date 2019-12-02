# [Parsing] Parser instruction prefixes
PRS = 0 # Parser instruction
DGT = pow(2, 7) # Digit
LTR = pow(2, 6) + pow(2, 7) # Letter

# [Parsing] Parser instructions
BGN = 0 # Begin query
END = 1 # End query
PRM = 3 # Start query parameter name
VAL = 4 # Start query parameter value
NEG = 5 # Make number negative
DOT = 6 # Decimal point

# [Numbers] Max digits after decimal point
fractionPrecision = 2
