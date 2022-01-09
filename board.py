from rule import *
from cell import *

class Board:
    def __init__(self):
        # notes: [ column1 [ note1, note2 ], column2 [ note1 ], column3 [], ... ]
        self.notes = []
        self.lowestKey = None
        self.highestKey = None

    def generateCells(self, length, rule):
        for i in range(length):
            self.notes.append([])
            columnNotes = rule.evaluate(self.notes, i)
            for n in columnNotes:
                if not self.lowestKey:
                    self.lowestKey = n.key
                if not self.highestKey:
                    self.highestKey = n.key + 1

                if n.key < self.lowestKey:
                    self.lowestKey = n.key
                if n.key > self.highestKey:
                    self.highestKey = n.key

                self.notes[i].append(n)

    def getNote(self, col, key):
        if col < 0 or col >= len(self.notes):
            return None
        for n in self.notes[col]:
            if n.key == key:
                return n
        return None

