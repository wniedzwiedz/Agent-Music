import random
from cell import *
from rule import *

class PercussionRule():
	DRUMS = {
			'Kick': 36,
			'Snare': 38,
			'Hi-Hat': 42,
			'Crash': 49,
			'Tom': 41
		}
	def __init__(self):
		pass

	def getDrumKey(name):
		return PercussionRule.DRUMS[name]

class EveryNthRule(PercussionRule):
	def __init__(self, drum_name, step, shift):
        self.drum_key = EveryNthRule.getDrumKey(drum_name)
        self.my_notes = []
        self.n = step
        self.s = shift

    def evaluate(self, notes, current_index):
        self.my_notes = []
        #Every nth-note
        if (current_index - s) % n == 0:
            self.my_notes.append(Cell(self.drum_key)) 
            return self.my_notes
        #Rest
        else:
            return self.my_notes