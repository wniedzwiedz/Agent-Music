from cell import *
from MelodyRule import *

class Rule:
  def __init__(self):
    pass

  def evaluate(self, notes, current_index):
    return Cell(60)


class IncreaseRule(Rule):
    def __init__(self, base_key):
        self.base_key = base_key
        self.my_notes = []

    def evaluate(self, notes, current_index):
        self.my_notes = []
        if current_index == 0 or len(notes) == 0:
            self.my_notes.append(Cell(self.base_key))
            return self.my_notes
        else:
            previous = notes[current_index - 1]
            self.my_notes.append(Cell(previous[0].key + 1)) 
            return self.my_notes


class ElemCARule(Rule):
    def __init__(self, base_key, width, rule):
        self.base_key = base_key
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
            self.notes.append(Cell(self.base_key))
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
                self.notes.append(Cell(int(self.base_key-self.width/2+2*i)))
        return self.notes 
