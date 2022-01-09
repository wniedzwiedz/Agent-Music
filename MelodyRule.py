import random
from cell import *
from rule import *

class MelodyRule():
	def __init__(self, root_key, scale, octave):
		self.keys_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
		self.octave = int(octave)
		self.root_key = MelodyRule.getRoot(root_key,self.octave,self.keys_list)
		self.scale = MelodyRule.getScale(scale)
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
		# First chord root in octave
		if current_index == 0 or len(notes) == 0:
			rnd = random.randint(0,6)
			for i in range(rnd, rnd + 6, 2):
				self.my_notes.append(Cell(MelodyRule.getKey(self.root_key,self.octave,self.scale,i)))
			return self.my_notes
		else:
			rnd = random.randint(-2, 6)
			previous = notes[current_index-1]
			previous_root = previous[0].pitch
			while MelodyRule.getKey(self.root_key,self.octave,self.scale,rnd) == previous_root:
				rnd = random.randint(0, 6)
			for i in range(rnd, rnd + 6, 2):
				self.my_notes.append(Cell(MelodyRule.getKey(self.root_key,self.octave,self.scale,i)))
			return self.my_notes
