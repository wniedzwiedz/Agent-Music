from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.Qt6 import *

from canvas import *
from board import *
from rule import *
from ChordMelodyRule import *

from external import fluidsynth


class Player(Canvas):
    def __init__(self, options):
        super().__init__()
        print(f"Creating Player with {options}..")
        self.options = options
        self.stepCounter = 0
        rule = None

        if options.get("rule", "") == "Increase":
            rule = IncreaseRule(base_key=20)
            
        elif options.get("rule", "") == "Chord Melody":
            rule = ChordMelodyRule(root_key=self.options['rootKey'],
                            scale=self.options['scale'],
                            octave=self.options['octave'])

        elif options.get("rule", "") == "Elementary":
            rule = ElemCARule(base_key=35, width=7, rule=163)
            
        elif options.get("rule", "") == "AB":
            rule = ABRule(base_key=44)


        if not rule:
            raise Exception("Rule not specified!")

        board = Board()
        board.generateCells(100, rule)
        self.setBoard(board)

        self.fs = fluidsynth.Synth()
        self.fs.start()

        path = ""
        bank = -1

        if options.get("instrument", "") == "Grand Piano":
            path = "soundfonts/Full Grand Piano.sf2"
            bank = 0
        elif options.get("instrument", "") == "Drums":
            path = "soundfonts/GoldDrums.sf2"
            bank = 0
        elif options.get("instrument", "") == "Drama Piano":
            path = "soundfonts/Drama Piano.sf2"
            bank = 0
        elif options.get("instrument", "") == "FM Piano":
            path = "soundfonts/FM Piano.sf2"
            bank = 0
        elif options.get("instrument", "") == "Korg Piano":
            path = "soundfonts/Korg Triniton Piano.sf2"
            bank = 0
        elif options.get("instrument", "") == "Piano Bass":
            path = "soundfonts/Piano Bass.sf2"
            bank = 0
        elif options.get("instrument", "") == "Stereo Piano":
            path = "soundfonts/Stereo Piano.sf2"
            bank = 0
        elif options.get("instrument", "") == "Tight Piano":
            path = "soundfonts/Tight Piano.sf2"
            bank = 0

        if path == "" or bank < 0:
            raise Exception("Instrument not specified!")
            
        sfid = self.fs.sfload(path)
        self.fs.program_select(0, sfid, bank, 0)

        self.fs.cc(0, 7, 127)
        self.holdNotes = True

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
        previousNotes = self.board.notes[col-1]
        notes = self.board.notes[col]
        if len(notes) > 0:
            for note in notes:
                sameNote = False
                for prevNote in previousNotes:
                    if prevNote.key == note.key:
                        sameNote = True
                        break

                if not sameNote or not self.holdNotes:
                    self.fs.noteoff(0, note.key)
                    self.fs.noteon(0, note.key, note.velocity)
