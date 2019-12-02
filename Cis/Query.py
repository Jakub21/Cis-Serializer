from Cis.Const import *

class Query:
  def __init__(self, key, **params):
    self.key = key
    self.params = params

  def addParam(self, key, val):
    self.params[key] = val

  def get(self, key):
    return self.params[key]

  def build(self):
    globals().update(self.plugin.cnf.__dict__)
    result = []
    result += [PRS + BGN]
    result += self.__buildWord__(self.key)
    for key, val in self.params.items():
      result += [PRS + PRM]
      result += self.__buildWord__(key)
      result += [PRS + VAL]
      if type(val) in (int, float): result += self.__buildNumber__(val)
      else: result += self.__buildWord__(val)
    result += [PRS + END]
    result = [itob(int(x)) for x in result]
    result = b''.join(result)
    return result

  def __buildNumber__(self, number):
    globals().update(self.plugin.cnf.__dict__)
    base = 64
    result = []
    TEMPNUMBER = number
    if number < 0:
      result.append(PRS + NEG)
      number *= -1
    remaining = number
    try: exponent = ceil(log(number, base))
    except ValueError: return [DGT]
    if exponent < 0:
      result.append(PRS + DOT)
      result += [DGT] * -exponent
    while remaining >= pow(base, -fractionPrecision):
      exponent -= 1
      if exponent == -1: result.append(PRS + DOT)
      power = pow(base, exponent)
      try: amount = remaining // power
      except ZeroDivisionError:
        result += [DGT]
        break
      remaining -= amount * power
      result.append(DGT + amount)
    if not len([x for x in result if x not in [DGT, PRS+NEG, PRS+DOT]]):
      result = [DGT]
    return result

  def __buildWord__(self, word):
    globals().update(self.plugin.cnf.__dict__)
    result = []
    for c in str(word):
      c = c.upper()
      if c < 'A' or c > 'Z':
        if c == '_': result += 26
        else: print(f'Error "{c}"'); raise ValueError('Letter index out of range')
      result += [ord(c) - ord('A')]
    return [i+LTR for i in result]

  def __repr__(self):
    return self.__str__()
  def __str__(self):
    s = f'<Query {self.key}>' + ' {\n'
    for key, val in self.params.items():
      s += f'  {key}: {val}\n'
    return s + '}'