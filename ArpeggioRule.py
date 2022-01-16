import random
from cell import *
from rule import *

class ArpeggioRule():
	def __init__(self, root_key, scale, octave, chords_num, length):
		self.keys_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
		self.octave = int(octave)
		self.root_key = ArpeggioRule.getRoot(root_key,self.octave,self.keys_list)
		self.scale = ArpeggioRule.getScale(scale)
		self.my_notes = []
		self.n = chords_num * length
		self.chord_length = length
		self.chord = []

	def getRoot(name, octave, keys_list):
		root = 60 + 12*octave + keys_list.index(name)
		return root

	def getScale(name):
		if name=='Major':
			scale_rule=[0,2,4,5,7,9,11]
		elif name=='minor':
			scale_rule=[0,2,3,5,7,8,10]
		elif name=='Dorian':
			scale_rule=[0,2,3,5,7,9,10]
		elif name=='Phrygian':
			scale_rule=[0,1,3,5,7,8,10]
		elif name=='Harmonic':
			scale_rule=[0,2,3,5,7,8,11]
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
			self.chord = [rnd, rnd + 2, rnd + 4]
			self.my_notes.append(Cell(ArpeggioRule.getKey(self.root_key,self.octave,self.scale,rnd)))
			return self.my_notes

		elif current_index >= self.n:
			self.my_notes = notes[current_index % self.n]
			return self.my_notes

		elif current_index % self.chord_length == 0:
			if ((current_index / self.chord_length) + 1) % 4 == 0:
				rnd = random.randint(0, 6)
				praprevious = notes[current_index - 2 * self.chord_length]
				praprevious_root = praprevious[0].key
				previous = notes[current_index - self.chord_length]
				previous_root = previous[0].key
				tmp_key = ArpeggioRule.getKey(self.root_key,self.octave,self.scale,rnd)
				while abs(tmp_key - previous_root) > 5 or abs(tmp_key - previous_root) == 0 or abs(tmp_key - praprevious_root) == 0:
					rnd = random.randint(0, 6)
					tmp_key = ArpeggioRule.getKey(self.root_key,self.octave,self.scale,rnd)
				self.chord = [rnd, rnd + 2, rnd + 4]
				self.my_notes.append(Cell(ArpeggioRule.getKey(self.root_key,self.octave,self.scale,rnd)))
				return self.my_notes
			else:
				rnd = random.randint(0, 6)
				previous = notes[current_index - self.chord_length]
				previous_root = previous[0].key
				tmp_key = ArpeggioRule.getKey(self.root_key,self.octave,self.scale,rnd)
				while abs(tmp_key - previous_root) > 2 or abs(tmp_key - previous_root) == 0:
					rnd = random.randint(0, 6)
					tmp_key = ArpeggioRule.getKey(self.root_key,self.octave,self.scale,rnd)
				self.chord = [rnd, rnd + 2, rnd + 4]
				self.my_notes.append(Cell(ArpeggioRule.getKey(self.root_key,self.octave,self.scale,rnd)))
				return self.my_notes

		else:
			self.my_notes.append(Cell(ArpeggioRule.getKey(self.root_key,self.octave,self.scale,self.chord[(current_index % self.chord_length) % len(self.chord)])))
			return self.my_notes
