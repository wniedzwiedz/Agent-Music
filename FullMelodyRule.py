import random
from cell import *
from rule import *

class FullMelodyRule():
	def __init__(self, root_key, scale, octave):
		self.keys_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
		self.octave = int(octave)
		self.root_key = FullMelodyRule.getRoot(root_key,self.octave,self.keys_list)
		self.scale = FullMelodyRule.getScale(scale)
		self.my_notes = []
		self.chord_length = 0
		self.chord_length_counter = 0

	def getRoot(name, octave, keys_list):
		root = 60 + len(keys_list) * octave + keys_list.index(name)
		return root

	def getScale(name):
		if name=='Major':
			scale_rule=[0,2,4,5,7,9,11]
		elif name=='minor':
			scale_rule=[0,2,3,5,7,8,10]
		else:
			scale_rule=[]
		return scale_rule
	
	def getKey(key,octave,scale,pos):
		tmp_octave = octave
		tmp_pos = pos
		if pos >= len(scale):
			tmp_octave = tmp_octave + 1
			tmp_pos = tmp_pos % len(scale)
		elif pos < 0:
			tmp_octave = tmp_octave - 1
			tmp_pos = tmp_pos % len(scale)
		return key + 12*tmp_octave + scale[tmp_pos]

	def evaluate(self, notes, current_index):
		self.my_notes = []
		miss = random.randint(0,100)
		harmony = random.randint(0,100)

		# First chord root in octave
		if current_index == 0:
			rnd = random.randint(0,6)
			self.chord_length = random.randint(2,6)
			self.chord_length_counter = 1
			# Base note - root in lower octave
			self.my_notes.append(Cell(FullMelodyRule.getKey(self.root_key,self.octave - 1,self.scale, rnd)))
			# Root chord
			for i in range(rnd, rnd + 6, 2):
				self.my_notes.append(Cell(FullMelodyRule.getKey(self.root_key,self.octave,self.scale, i)))
			# Top sound - if appears, higher octave
			if miss > 70:
				rnd = random.randint(0,6)
				self.my_notes.append(Cell(FullMelodyRule.getKey(self.root_key,self.octave + 2, self.scale, rnd)))

			return self.my_notes

		elif self.chord_length_counter % self.chord_length == 0:
			self.chord_length_counter = 1
			self.chord_length = random.randint(2,6)
			if harmony > 30:
				rnd = random.randint(0, 6)
				# Mid chord
				previous = notes[current_index - 1]
				previous_root = previous[1].key
				tmp_key = FullMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)
				while abs(tmp_key - previous_root) > 5 or abs(tmp_key - previous_root) == 0:
					rnd = random.randint(0, 6)
					tmp_key = FullMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)
				for i in range(rnd, rnd + 6, 2):
					self.my_notes.append(Cell(FullMelodyRule.getKey(self.root_key, self.octave, self.scale, i)))
				# Base note
				mid_root = self.my_notes[0].key
				self.my_notes.insert(0, Cell(mid_root - len(self.keys_list)))
					
			else:
				rnd = random.randint(0, 6)
				# Mid chord
				previous = notes[current_index - 1]
				previous_root = previous[1].key
				tmp_key = FullMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)
				while abs(tmp_key - previous_root) == 0:
					rnd = random.randint(0, 6)
					tmp_key = FullMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)
				for i in range(rnd, rnd + 6, 2):
					self.my_notes.append(Cell(FullMelodyRule.getKey(self.root_key, self.octave, self.scale, i)))
				# Base note
				mid_root = self.my_notes[0].key
				self.my_notes.insert(0, Cell(mid_root - len(self.keys_list)))

			# Top note - if happens, new note in harmony 
			if miss > 50:
				rnd = random.randint(0, 6)
				if len(notes[current_index - 1]) <= 4:
					self.my_notes.append(Cell(FullMelodyRule.getKey(self.root_key, self.octave + 2, self.scale, rnd)))
				else:
					while FullMelodyRule.getKey(self.root_key, self.octave + 2, self.scale, rnd) == notes[current_index - 1][-1].key:
						rnd = random.randint(0, 6)
					self.my_notes.append(Cell(FullMelodyRule.getKey(self.root_key, self.octave + 2, self.scale, rnd)))
			return self.my_notes

		else:
			self.chord_length_counter += 1
			# Bass and mid chord keys from previous state
			for i in range(0,4):
				self.my_notes.append(notes[current_index - 1][i])
			# Top  - if happens, new note
			if miss > 50:
				rnd = random.randint(0, 6)
				if len(notes[current_index - 1]) <= 4:
					self.my_notes.append(Cell(FullMelodyRule.getKey(self.root_key, self.octave + 2, self.scale, rnd)))
				else:
					while FullMelodyRule.getKey(self.root_key, self.octave + 2, self.scale, rnd) == notes[current_index - 1][-1].key:
						rnd = random.randint(0, 6)
					self.my_notes.append(Cell(FullMelodyRule.getKey(self.root_key, self.octave + 2, self.scale, rnd)))
			return self.my_notes
