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
		if (current_index - self.s) % self.n == 0:
			self.my_notes.append(Cell(self.drum_key)) 
			return self.my_notes
		#Rest
		else:
			return self.my_notes

class CombineRule(Rule):
	def __init__(self, rules):
		self.rules = rules
		self.length = len(rules)
		self.my_notes = []

	def evaluate(self, notes, current_index):
		self.my_notes = []
		for rule in self.rules:
			tmp_notes = rule.evaluate(notes,current_index)
			for note in tmp_notes:
				self.my_notes.append(Cell(note.key))
		return self.my_notes

class RandomRythmRule(PercussionRule):
	def __init__(self, drum_name, spacing, error):
		self.drum_key = RandomRythmRule.getDrumKey(drum_name)
		self.seq_length = random.randint(1,4)
		self.seq_dens = random.randint(1,4)
		self.spacing = spacing
		self.error = error
		self.len_cnt = 0
		self.my_notes = []

	def checkDistance(notes, current_index, distance):
		if distance == 1:
			return True
		else:
			for i in range(1, distance):
				if current_index - i <= 0:
					return True
				elif notes[current_index - i]:
					return False
			return True

	def evaluate(self, notes, current_index):
		self.my_notes = []
		miss = random.randint(0,100)
		new_seq = random.randint(0,100)
		new_dens = random.randint(0,100)
		if miss > 80:
			self.len_cnt += 1
			return self.my_notes
		elif new_seq < 7 or self.len_cnt == self.seq_length:
			self.seq_length = random.randint(1,4)
			self.seq_dens = random.randint(1,4)
			self.len_cnt = 0
		elif new_dens < self.error * 3:
			if RandomRythmRule.checkDistance(notes, current_index, self.seq_dens):
				self.my_notes.append(Cell(self.drum_key))
				return self.my_notes
		elif self.len_cnt == 0:
			self.my_notes.append(Cell(self.drum_key)) 
			self.len_cnt += 1
			return self.my_notes

		#Every other case
		if RandomRythmRule.checkDistance(notes, current_index, self.spacing):
			self.my_notes.append(Cell(self.drum_key))
			self.len_cnt += 1 
			return self.my_notes
		else:
			self.len_cnt += 1
			return self.my_notes