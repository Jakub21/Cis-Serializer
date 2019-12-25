from Cis.Queue import Queue
from Cis.Query import Query
from Cis.Const import *

class Parser:
  def __init__(self):
    self.data = Queue()
    self.queries = Queue()

  def pushBytes(self, data):
    if type(data) != bytes:
      raise TypeError('Data pushed to Cis Parser must be of "bytes" type')
    for c in data:
      self.data.push(int(c))

  def parse(self):
    '''Sanitizes and splits data for parseSequence'''
    sequences = []
    current = []
    inSequence = False
    while True:
      try: x = self.data.pop()
      except IndexError: break
      if x == PRS + BGN: inSequence = True
      if x == PRS + END:
        inSequence = False
        sequences += [current+[x]]
        current = []
      if inSequence: current += [x]
    for x in current: # Re-add leftover instructions to queue
      self.data.push(x)
    for sequence in sequences:
      self.queries.push(self.parseSequence(sequence))

  def parseSequence(self, sequence):
    '''Proper Sequence parses, requires data to be properly cropped'''
    query = Query('')
    current = []
    phase, prevPhase = 'K', 'K'
    for index, entry in enumerate(sequence):
      if entry == PRS + PRM: phase = 'P'
      if entry == PRS + VAL: phase = 'V'
      if prevPhase == 'K' and (phase == 'P' or entry == PRS + END):
        query.key = self.decodeLetters(current[1:])
        current = []
      if prevPhase == 'V' and (phase == 'P' or entry == PRS + END):
        first = current[1]
        if first - (first % LTR) == LTR:
          value = self.decodeLetters(current[1:])
        elif first - (first % DGT) == DGT or first in (PRS + NEG, PRS + DOT):
          value = self.decodeNumber(current[1:])
        else:
          raise ValueError(f'Unrecognized sub-instruction {first}')
        query.addParam(crntParam, value)
        current = []
      if prevPhase == 'P' and phase == 'V':
        crntParam = self.decodeLetters(current[1:])
        self.crntParam = crntParam
        current = []
      current.append(entry)
      prevPhase = phase
    return query

  def decodeLetters(self, data):
    word = ''
    for i in data:
      i -= LTR
      if i < 26: word += chr(i+ord('a'))
      elif i < 26*2: word += chr(i+ord('A'))
      else: word += Chars[i-26*2]
      print(f'[CIS] {i} => {word[-1]}')
    return word

  def decodeNumber(self, data):
    result = 0
    isNegative = data[0] == PRS + NEG
    if isNegative: data = data[1:]
    try:
      exponent = data.index(PRS + DOT)
    except ValueError:
      exponent = len(data)
    base = 64
    for digit in data:
      if digit in (PRS + DOT, PRS + NEG): continue
      exponent -= 1
      digit -= DGT
      mult = pow(base, exponent)
      result += digit * mult
    if isNegative: result *= -1
    return result
