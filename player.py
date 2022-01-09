from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.Qt6 import *

from canvas import *
from board import *
from rule import *
from MelodyRule import *

from external import fluidsynth


class Player(Canvas):
    def __init__(self, options):
        super().__init__()
        print(f"Creating Player with {options}..")
        self.options = options
        self.stepCounter = 0
        rule = None

        if options.get("rule", "") == "Increase":
            rule = IncreaseRule(base_pitch=20)
        elif options.get("rule", "") == "Melody":
            rule = MelodyRule(root_key=self.options['rootKey'],
                            scale=self.options['scale'],
                            octave=self.options['octave'])
        if not rule:
            raise Exception("Rule not specified!")

        board = Board()
        board.generateCells(40, rule)
        self.setBoard(board)

        self.fs = fluidsynth.Synth()
        self.fs.start()

        path = ""
        bank = -1

        if options.get("instrument", "") == "Piano":
            path = "soundfonts/Full Grand Piano.sf2"
            bank = 0
        elif options.get("instrument", "") == "Drums":
            path = "soundfonts/GoldDrums.sf2"
            bank = 0

        if path == "" or bank < 0:
            raise Exception("Instrument not specified!")
            
        sfid = self.fs.sfload(path)
        self.fs.program_select(0, sfid, bank, 0)

        self.fs.cc(0, 7, 127)

    def __del__(self):
        self.fs.delete()


    def reset(self):
        self.stepCounter = 0
        self.highlightColumn(-1)
        self.update()

    def step(self):
        self.highlightColumn(self.stepCounter)
        self.play(self.stepCounter)

        self.stepCounter += 1
        self.update()

        if self.stepCounter >= len(self.board.notes):
            self.stepCounter = 0


    def play(self, col):
        notes = self.board.notes[col]
        if len(notes) > 0:
            for note in notes:
                self.fs.noteoff(0, note.pitch)
                self.fs.noteon(0, note.pitch, note.velocity)
