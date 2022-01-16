from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.Qt6 import *

from canvas import *
from board import *
from rule import *
from ChordMelodyRule import *
from RepetetiveChordRule import *
from PercussionRules import *
from TopMelodyRule import *
from ArpeggioRule import *
from FullMelodyRule import *

from external import fluidsynth


class Player(Canvas):

    INSTRUMENTS = {
            'Grand Piano': "soundfonts/Full Grand Piano.sf2",
            'Drama Piano': "soundfonts/Drama Piano.sf2",
            'FM Piano': "soundfonts/FM Piano.sf2",
            'Korg Triniton Piano': "soundfonts/Korg Triniton Piano.SF2",
            'Stereo Piano': "soundfonts/Stereo Piano.sf2",
            'Tight Piano': "soundfonts/Tight Piano.sf2",
            'Drums': "soundfonts/GoldDrums.sf2"
    }

    def __init__(self, options, combine_options):
        super().__init__()
        print(f"Creating Player with {options}..")
        self.options = options
        self.combine_options = combine_options
        self.stepCounter = 0
        if not "rule" in options:
            raise Exception("Rule not specified!")

        rule = self.getRule(self.options.get("rule"), self.options)

        if not rule:
            raise Exception("Specified rule not found!")

        board = Board()
        board.generateCells(96, rule)
        self.setBoard(board)

        self.fs = fluidsynth.Synth()
        self.fs.start()

        path = ""
        bank = -1

        if not "instrument" in options:
            raise Exception("Instrument not specified")

        if options.get("instrument", "") != "":
            path = Player.INSTRUMENTS[options.get("instrument")]
            bank = 0

        if path == "" or bank < 0:
            raise Exception("Instrument not found!")
            
        sfid = self.fs.sfload(path)
        self.fs.program_select(0, sfid, bank, 0)

        self.fs.cc(0, 7, 127)
        self.holdNotes = options.get("hold_notes", True)


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

                if not sameNote or not self.holdNotes or col == 0:
                    self.fs.noteoff(0, note.key)
                    self.fs.noteon(0, note.key, note.velocity)

    def getRule(self, name, options):
        if name == "Increase":
            return IncreaseRule(base_key=20)

        elif name == "Full Melody":
            return FullMelodyRule(root_key=options['rootKey'],
                            scale=options['scale'],
                            octave=options['octave'])

        elif name == "Chord Melody":
            return ChordMelodyRule(root_key=options['rootKey'],
                            scale=options['scale'],
                            octave=options['octave'])

        elif name == "Repetitive Chords":
            return RepetetiveChordRule(root_key=options['rootKey'],
                            scale=options['scale'],
                            octave=options['octave'],
                            chords_num=options['repetitive_number'],
                            length=options['repetitive_length'])

        elif name == "Arpeggio":
            return ArpeggioRule(root_key=options['rootKey'],
                            scale=options['scale'],
                            octave=options['octave'],
                            chords_num=8, #options['repetitive_number'],
                            length=6) #options['repetitive_length'])

        elif name == "Top Melody":
            return TopMelodyRule(root_key=options['rootKey'],
                            scale=options['scale'],
                            octave=options['octave'])

        elif name == "Elementary":
            return ElemCARule(base_key=35, width=7, rule=163)

        elif name == "AB":
            return ABRule(base_key=44)

        elif name == "Every Nth":
            return EveryNthRule(
                drum_name=options['percussion'], 
                step=options['percussion_step'], 
                shift=options['percussion_shift'])

        elif name == "Random Rythm":
            return RandomRythmRule(
                drum_name=options['percussion'],
                spacing=options['percussion_step'], 
                error=options['percussion_shift'])

        elif name == "Combine":
            if self.combine_options:
                rules = []
                for options_list in self.combine_options:
                    rules.append(self.getRule(options_list['combine_rule'], options_list))
                return CombineRule(rules)
            else:
                return None # Można by dodać jakiś warning, a nie wywalanie programu - to się dzieje, gdy już dodamy zkombajnowane instrumenty, a nie dodamy nic nowego do listy, więc jest pusta

        else:
            return None

    def mousePressEvent(self, event: QMouseEvent):
        cellX, cellY = self.getCellWindowPosition(event.position().x(), event.position().y())
        self.stepCounter = int(cellX)
        print(cellX, cellY)

