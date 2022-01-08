from cell import *

class Rule:
  def __init__(self):
    pass

  def evaluate(self, notes, current_index):
    return Cell(60)


class IncreaseRule(Rule):
  def __init__(self, base_pitch):
    self.base_pitch = base_pitch

  def evaluate(self, notes, current_index):
    if current_index == 0 or len(notes) == 0:
      return Cell(self.base_pitch)
    # np.nonzero(notes[current_index-1,:])[0]
    return Cell(notes[current_index-1].pitch + 1) 


class ElemCARule(Rule):
  def __init__(self, base_pitch, width, rule):
    self.base_pitch = base_pitch
    self.last_row = np.zeros((width), dtype = int)
    self.width = width
    self.notes = []
    self.rule = rule

  def nextCell(prev, mid, nxt, bin_rule):
    if(prev == mid == nxt ==1):
        mid =  int(bin_rule[0])
    elif prev == mid ==1 and nxt ==0:
        mid =  int(bin_rule[1])
    elif prev == nxt ==1 and mid==0:
        mid =  int(bin_rule[2])
    elif prev==1 and mid == nxt==0:
        mid =  int(bin_rule[3])
    elif prev==0 and mid == nxt==1:
        mid =  int(bin_rule[4])
    elif prev == nxt ==0 and mid ==1:
        mid =  int(bin_rule[5])
    elif prev == mid ==0 and nxt==1:
        mid =  int(bin_rule[6])
    elif prev == mid == nxt==0:
        mid = int(bin_rule[7])
    
    return mid

  def evaluate(self, notes, current_index):
    self.notes = []
    # First row always has one black cell in the middle 
    if current_index == 0 or len(notes) == 0:
      self.last_row[int(self.width/2)] = 1
      self.notes.append(Cell(self.base_pitch))
      return self.notes

    bin_rule = "{0:{fill}8b}".format(self.rule, fill='0')
    # First row always has one black cell in the middle 
    
    for j in range(0,self.width):
        nextRow = np.zeros(self.width, dtype = int)
        #Boundary conditions in range
        for i in range(1, self.width-1):
            nextRow[i] = ElemCARule.nextCell(self.last_row[i-1], self.last_row[i], self.last_row[i+1], bin_rule)
    self.last_row = nextRow
    
    for i in range(0,self.width):
      if self.last_row[i]==1:
        self.notes.append(Cell(int(self.base_pitch-self.width/2+2*i)))
    return self.notes 
