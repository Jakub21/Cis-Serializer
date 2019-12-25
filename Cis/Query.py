from math import ceil, log
from Cis.Const import *

# Integer to bytes
itob = lambda x: x.to_bytes((x.bit_length() + 7) // 8, byteorder='big') or b'\x00'

class Query:
  def __init__(self, key, **params):
    self.key = key
    self.params = params

  def addParam(self, key, val):
    self.params[key] = val

  def get(self, key):
    return self.params[key]

  def build(self):
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
    result = []
    for c in str(word):
      if c in range(ord('a'), ord('z')+1): result += [ord(c) - ord('a')]
      elif c in range(ord('A'), ord('Z')+1): result += [ord(c) - ord('A') + 26]
      else:
        try: result += [Chars.index(c) + 52]
        except ValueError:
          raise ValueError(f'Cis strings can not contain character "{c}"')
    return [i+LTR for i in result]

  def __repr__(self):
    return self.__str__()
  def __str__(self):
    s = f'<Query {self.key}>' + ' {\n'
    for key, val in self.params.items():
      s += f'  {key}: {val}\n'
    return s + '}'
