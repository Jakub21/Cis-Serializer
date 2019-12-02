'''Simple FIFO Queue based on a list'''

class Queue:
  def __init__(self):
    self.data = []

  def push(self, elm):
    self.data += [elm]

  def pop(self):
    first = self.data[0]
    self.data = self.data[1:]
    return first

  def empty(self):
    return not len(self.data)

  def size(self):
    return len(self.data)
