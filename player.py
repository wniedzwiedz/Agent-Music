from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.Qt6 import *

from canvas import *
from board import *
from rule import *

from external import fluidsynth


class Player(Canvas):
    def __init__(self):
        super().__init__()
        self.stepCounter = 0
        rule = IncreaseRule(base_pitch=80)
        board = Board()
        board.generateCells(40, rule)
        self.setBoard(board)

        self.fs = fluidsynth.Synth()
        self.fs.start()
        sfid = self.fs.sfload("soundfonts/Grand Piano.sf2")
        self.fs.program_select(0, sfid, 0, 0)

        self.fs.cc(0, 7, 127)

    def __del__(self):
        self.fs.delete()


    def reset(self):
        self.stepCounter = 0
        self.highlightColumn(-1)


    def step(self):
        self.highlightColumn(self.stepCounter)
        self.play(self.stepCounter)

        self.stepCounter += 1
        self.update()

        if self.stepCounter >= len(self.board.notes):
            self.stepCounter = 0


    def play(self, col):
        note = self.board.notes[col]
        if note:
            self.fs.noteoff(0, note.pitch)
            self.fs.noteon(0, note.pitch, note.velocity)
