from rule import *
from cell import *

class Board:
    def __init__(self):
        self.notes = []

    def generateCells(self, length, rule):
        for i in range(length):
            note = rule.evaluate(self.notes, i)
            self.notes.append(note)

    def getNote(self, x, y):
        if x < 0 or x >= len(self.notes):
            return None
        if self.notes[x].pitch == y:
            return self.notes[x]
        return None

        
