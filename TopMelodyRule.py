import random
from cell import *
from rule import *

class TopMelodyRule():
	def __init__(self, root_key, scale, octave):
		self.keys_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
		self.octave = int(octave)
		self.root_key = TopMelodyRule.getRoot(root_key,self.octave,self.keys_list)
		self.scale = TopMelodyRule.getScale(scale)
		self.my_notes = []

	def getRoot(name, octave, keys_list):
		root = 60 + 12*octave + keys_list.index(name)
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
		double = random.randint(0,100)
		harmony = random.randint(0,100)
		# First chord root in octave
		if current_index % 32 == 0 or len(notes) == 0:
			rnd = random.randint(0,6)
			self.my_notes.append(Cell(TopMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)))
			return self.my_notes

		elif miss > 60:
			return self.my_notes

		elif double < 20:
			self.my_notes = notes[current_index - 1]
			return self.my_notes

		else:
			previous = notes[current_index - 1]
			if previous:
				previous_root = previous[0].key
				rnd = random.randint(0,6)
				if harmony > 20:
					tmp_key = TopMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)
					while abs(tmp_key - previous_root) > 5 or abs(tmp_key - previous_root) == 0:
						rnd = random.randint(0, 6)
						tmp_key = TopMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)
					self.my_notes.append(Cell(TopMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)))
					return self.my_notes
				else:
					tmp_key = TopMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)
					while abs(tmp_key - previous_root) == 0:
						rnd = random.randint(0, 6)
						tmp_key = TopMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)
					self.my_notes.append(Cell(TopMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)))
					return self.my_notes
			else:
				rnd = random.randint(0,6)
				self.my_notes.append(Cell(TopMelodyRule.getKey(self.root_key,self.octave,self.scale,rnd)))
				return self.my_notes

