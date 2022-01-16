from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.Qt6 import *

import sys, time, random
from functools import partial

from player import *

RULES = [
    'Full Melody',
    'Repetitive Chords', 
    'Chord Melody',
    'Top Melody',
    'Arpeggio',
    'Increase', 
    'Elementary',
    'AB',
]

DRUM_RULES = [
    'Every Nth',
    'Random Rythm',
    'Combine'
]

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        print("Creating window...")
        self.setWindowTitle("Cellular Music")
        self.setFixedSize(960, 720)
        self.setBaseSize(QSize(640, 480))
        self.setGeometry(10, 10, 640, 480)

        print("Creating layout...")
        self.layout = QVBoxLayout(self)
        self.barLayout = QHBoxLayout()
        self.layout.addLayout(self.barLayout)
        self.optionsLayout = QHBoxLayout()
        self.layout.addLayout(self.optionsLayout)
        self.combineRuleLayout = QHBoxLayout()
        self.layout.addLayout(self.combineRuleLayout)
        self.combineRuleRulesLayout = QHBoxLayout()
        self.drumsOptionsLayout = QHBoxLayout()
        self.repetitiveRuleLayout = QHBoxLayout()

        # Bar & Buttons 
        print("Creating buttons...")
        play_button = QPushButton("Play ▶")
        play_button.clicked.connect(self.playClicked)
        self.barLayout.addWidget(play_button)
        stop_button = QPushButton("Stop ■")
        stop_button.clicked.connect(self.stopClicked)
        self.barLayout.addWidget(stop_button)
        self.loopCheckbox = QCheckBox("Loop")
        self.barLayout.addWidget(self.loopCheckbox)
        self.loopCheckbox.setChecked(True)
        self.loopCheckbox.setEnabled(False)

        self.speedSlider = QSlider(Qt.Orientation.Horizontal)
        self.speedSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speedSlider.setPageStep(100)
        self.speedSlider.setSingleStep(100)
        self.speedSlider.setMinimum(300)
        self.speedSlider.setMaximum(1200)
        self.speedSlider.setTickInterval(10)
        self.speedSlider.setMaximumWidth(100)
        self.barLayout.addWidget(self.speedSlider)
        self.speedLabel = QLabel("bpm")
        self.barLayout.addWidget(self.speedLabel)
        self.speedSlider.valueChanged.connect(self.speedSliderChanged)

        # Options
        print("Creating options...")
        self.optionsRootKeyCombo = QComboBox()
        for key in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']:
            self.optionsRootKeyCombo.addItem(key)
        self.optionsLayout.addWidget(self.optionsRootKeyCombo)
        self.optionsLayout.addWidget(QLabel("Root key"))

        self.optionsScaleCombo = QComboBox()
        for scale in ['Major', 'minor', 'Phrygian', 'Dorian', 'Harmonic']:
            self.optionsScaleCombo.addItem(scale)
        self.optionsLayout.addWidget(self.optionsScaleCombo)
        self.optionsLayout.addWidget(QLabel("Scale"))

        self.optionsOctaveCombo = QComboBox()
        self.optionsOctaveCombo.addItems(['-5', '-4', '-3', '-2' ,'-1', '0', '1', '2', '3', '4', '5'])
        self.optionsOctaveCombo.setCurrentText('0')
        self.optionsLayout.addWidget(self.optionsOctaveCombo)
        self.optionsLayout.addWidget(QLabel("Octave"))
        

        self.optionsInstrumentCombo = QComboBox()
        self.optionsInstrumentCombo.addItems(Player.INSTRUMENTS.keys())
        self.optionsLayout.addWidget(self.optionsInstrumentCombo)
        self.optionsLayout.addWidget(QLabel("Instrument"))
        self.holdNotesCheckbox = QCheckBox("Hold notes")
        self.holdNotesCheckbox.setChecked(True)
        self.optionsLayout.addWidget(self.holdNotesCheckbox)

        # Drums options
        self.drumsCombo = QComboBox()
        self.drumsCombo.addItems(["Snare", "Kick", "Hi-Hat", "Tom", "Crash"])
        self.drumsOptionsLayout.addWidget(QLabel("Percussion:"))
        self.drumsOptionsLayout.addWidget(self.drumsCombo)
        self.optionsInstrumentCombo.currentTextChanged.connect(self.instrumentComboChanged)

        self.drumsStepSlider = QSlider(Qt.Orientation.Horizontal)
        self.drumsStepSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.drumsStepSlider.setPageStep(1)
        self.drumsStepSlider.setSingleStep(1)
        self.drumsStepSlider.setMinimum(1)
        self.drumsStepSlider.setMaximum(16)
        self.drumsStepSlider.setTickInterval(1)
        self.drumsOptionsLayout.addWidget(self.drumsStepSlider)
        self.drumStepLabel = QLabel(f"Step {self.drumsStepSlider.value()}")
        self.drumsOptionsLayout.addWidget(self.drumStepLabel)
        self.drumsStepSlider.valueChanged.connect(
                lambda v :
                    # if self.optionsRuleCombo.currentText() == "Random Rythm":
                    #     self.drumStepLabel = QLabel(f"Spacing {self.drumsStepSlider.value()}")
                    # else: 
                    self.drumStepLabel.setText(f"Step ({self.drumsStepSlider.value()})")
        )

        self.drumsShiftSlider = QSlider(Qt.Orientation.Horizontal)
        self.drumsShiftSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.drumsShiftSlider.setPageStep(1)
        self.drumsShiftSlider.setSingleStep(1)
        self.drumsShiftSlider.setMinimum(0)
        self.drumsShiftSlider.setMaximum(16)
        self.drumsShiftSlider.setTickInterval(1)
        self.drumsOptionsLayout.addWidget(self.drumsShiftSlider)
        self.drumsShiftLabel = QLabel(f"Shift ({self.drumsShiftSlider.value()})")
        self.drumsOptionsLayout.addWidget(self.drumsShiftLabel)
        self.drumsShiftSlider.valueChanged.connect(
                lambda v : 
                    self.drumsShiftLabel.setText(f"Shift ({self.drumsShiftSlider.value()})")
        )

        self.layout.addLayout(self.drumsOptionsLayout)
        self.layoutSetChildrenVisible(self.drumsOptionsLayout, False)
        
        self.optionsRuleCombo = QComboBox()
        self.optionsRuleCombo.addItems(RULES)
        self.optionsRuleCombo.currentTextChanged.connect(self.ruleComboChanged)
        self.optionsLayout.addWidget(self.optionsRuleCombo)
        self.optionsLayout.addWidget(QLabel("Rule"))


        # Combine Rule Layout & Combine Rule Rules Layout
        self.combineRuleLayout.addWidget(QLabel("Rules to combine:"))
        self.combineRuleLayout.addLayout(self.combineRuleRulesLayout)
        self.combineRuleLayout.addStretch()
        
        # add the same rules to Combine Rule Options
        combineRuleRemoveRule = QPushButton("-")
        combineRuleRemoveRule.setMaximumSize(QSize(24, 24))
        combineRuleRemoveRule.clicked.connect(self.removeLastItem)

        self.combineRuleLayout.addWidget(combineRuleRemoveRule)
        combineRuleAddRule = QPushButton("+")
        combineRuleAddRule.setMaximumSize(QSize(24, 24))
        combineRuleAddRule.clicked.connect(self.saveCombineOptions)

        self.combineRuleLayout.addWidget(combineRuleAddRule)
        self.combineRuleRulesCombo = self.copyCombo(self.optionsRuleCombo)
        self.combineRuleRulesCombo.clear()
        self.combineRuleRulesCombo.addItems(DRUM_RULES[0:-1])
        self.combineRuleRulesLayout.addWidget(self.combineRuleRulesCombo)

        # if default (current) option is not "Combine"
        if self.optionsRuleCombo.currentText != "Combine":
            self.layoutSetChildrenVisible(self.combineRuleRulesLayout, False)
            self.layoutSetChildrenVisible(self.combineRuleLayout, False)

        # Repetitive rule options
        self.repetitiveRuleLayout.addWidget(QLabel("Repetitive rule options:"))
        self.repetitiveChordsNumberSlider = QSlider(Qt.Orientation.Horizontal)
        self.repetitiveChordsNumberSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.repetitiveChordsNumberSlider.setPageStep(1)
        self.repetitiveChordsNumberSlider.setSingleStep(1)
        self.repetitiveChordsNumberSlider.setMinimum(1)
        self.repetitiveChordsNumberSlider.setMaximum(16)
        self.repetitiveChordsNumberSlider.setTickInterval(1)
        self.repetitiveRuleLayout.addWidget(self.repetitiveChordsNumberSlider)
        self.repetitiveChordsNumberLabel = QLabel(f"Number ({self.repetitiveChordsNumberSlider.value()})")
        self.repetitiveRuleLayout.addWidget(self.repetitiveChordsNumberLabel)
        self.repetitiveChordsNumberSlider.valueChanged.connect(
                lambda v:
                self.repetitiveChordsNumberLabel.setText(f"Number ({self.repetitiveChordsNumberSlider.value()})")
        )

        self.repetitiveChordsLengthSlider = QSlider(Qt.Orientation.Horizontal)
        self.repetitiveChordsLengthSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.repetitiveChordsLengthSlider.setPageStep(1)
        self.repetitiveChordsLengthSlider.setSingleStep(1)
        self.repetitiveChordsLengthSlider.setMinimum(1)
        self.repetitiveChordsLengthSlider.setMaximum(16)
        self.repetitiveChordsLengthSlider.setTickInterval(1)
        self.repetitiveRuleLayout.addWidget(self.repetitiveChordsLengthSlider)
        self.repetitiveChordsLengthLabel = QLabel(f"Length ({self.repetitiveChordsLengthSlider.value()})")
        self.repetitiveRuleLayout.addWidget(self.repetitiveChordsLengthLabel)
        self.repetitiveChordsLengthSlider.valueChanged.connect(
                lambda v:
                self.repetitiveChordsLengthLabel.setText(f"Length ({self.repetitiveChordsLengthSlider.value()})")
        )

        if self.optionsRuleCombo.currentText() != "Repetitive Chords":
            self.layoutSetChildrenVisible(self.repetitiveRuleLayout, False)
        self.layout.addLayout(self.repetitiveRuleLayout)

        # Audio players
        self.combine_options = []
        self.players = []
        addButton = QPushButton("Add")
        addButton.clicked.connect(self.createPlayer)
        self.optionsLayout.addWidget(addButton)

        self.layout.addStretch()

        self.timer = QTimer()
        self.setTimer(1000)
        self.timer.stop()
        self.speedSliderChanged()

    def createPlayer(self):            
        options = {}
        options['rootKey'] = self.optionsRootKeyCombo.currentText()
        options['scale'] = self.optionsScaleCombo.currentText()
        options['octave'] = self.optionsOctaveCombo.currentText()
        options['instrument'] = self.optionsInstrumentCombo.currentText()
        options['rule'] = self.optionsRuleCombo.currentText()
        options['percussion'] = self.drumsCombo.currentText()
        options['percussion_step'] = self.drumsStepSlider.value()
        options['percussion_shift'] = self.drumsShiftSlider.value()

        options['repetitive_number'] = self.repetitiveChordsNumberSlider.value()
        options['repetitive_length'] = self.repetitiveChordsLengthSlider.value()
        options['hold_notes'] = self.holdNotesCheckbox.isChecked()

        print(options)
        player = Player(options, self.combine_options)
        self.combine_options = []
        self.players.append(player)
        removeButton = QPushButton("Remove")

        def removePlayer(self, player, button):
            print(f"Deleting {player} {button} for {self}")
            self.players.remove(player)
            self.layout.removeWidget(button)
            self.layout.removeWidget(player)
            player.deleteLater()
            button.deleteLater()

        myRemove = partial(removePlayer, self, player, removeButton)

        removeButton.clicked.connect(myRemove)
        self.layout.addWidget(removeButton)
        self.layout.addWidget(player)

    def saveCombineOptions(self):
        options = {}
        # options['rootKey'] = self.optionsRootKeyCombo.currentText()
        # options['scale'] = self.optionsScaleCombo.currentText()
        # options['octave'] = self.optionsOctaveCombo.currentText()
        options['instrument'] = self.optionsInstrumentCombo.currentText()
        options['rule'] = self.optionsRuleCombo.currentText()
        options['combine_rule'] = self.combineRuleRulesCombo.currentText() 
        options['percussion'] = self.drumsCombo.currentText()
        options['percussion_step'] = self.drumsStepSlider.value()
        options['percussion_shift'] = self.drumsShiftSlider.value()

        # options['repetitive_number'] = self.repetitiveChordsNumberSlider.value()
        # options['repetitive_length'] = self.repetitiveChordsLengthSlider.value()
        options['hold_notes'] = self.holdNotesCheckbox.isChecked()

        print(options)
        self.combine_options.append(options)

    def setTimer(self, ms):
        if not self.timer:
            self.timer = QTimer()
        try:
            self.timer.timeout.disconnect()
        except TypeError:
            pass
        self.timer.timeout.connect(self.step)
        self.timer.start(ms)

    def playClicked(self):
        self.speedSliderChanged()
        for player in self.players:
            player.reset()

    def stopClicked(self):
        self.timer.stop()
        for player in self.players:
            player.reset()

    def speedSliderChanged(self):
        val = self.speedSlider.value()
        if not val:
            return

        bpm = (1000 * 60) // val
        self.speedLabel.setText(f"{bpm:0.0f} bpm ({int(val):0.0f} ms)"),
        if bpm > 0:
            val = 1000 * 60 // bpm 
        self.setTimer(int(val) )

    def ruleComboChanged(self, rule):
        print(self.combineRuleLayout)
        if rule == "Combine":
            self.layoutSetChildrenVisible(self.combineRuleLayout, True)
            self.layoutSetChildrenVisible(self.combineRuleRulesLayout, True)
        else:
            self.layoutSetChildrenVisible(self.combineRuleLayout, False)
            self.layoutSetChildrenVisible(self.combineRuleRulesLayout, False)

        if rule == "Repetitive Chords":
            self.layoutSetChildrenVisible(self.repetitiveRuleLayout, True)
        else:
            self.layoutSetChildrenVisible(self.repetitiveRuleLayout, False)

    def instrumentComboChanged(self, instrument):
        print(instrument)
        if instrument == "Drums":
            self.layoutSetChildrenVisible(self.drumsOptionsLayout, True)
            self.optionsRuleCombo.clear()
            self.optionsRuleCombo.addItems(DRUM_RULES)
        else:
            self.layoutSetChildrenVisible(self.drumsOptionsLayout, False)
            self.optionsRuleCombo.clear()
            self.optionsRuleCombo.addItems(RULES)

    def step(self):
        for player in self.players:
            player.step()

    def copyCombo(self, combo):
        newCombo = QComboBox()
        for i in range(combo.count()):
            newCombo.addItem(combo.itemText(i))
        return newCombo

    def layoutSetChildrenVisible(self, layout, visible = True):
        for i in range(layout.count()):
            ch = layout.itemAt(i)
            if ch.widget():
                ch.widget().setVisible(visible)

    def removeLastItem(self):
        if self.combine_options:
            self.combine_options.pop()
        else:
            self.combine_options = []

    def layoutItems(self, layout):
        items = []
        for i in range(layout.count()):
            items.append(layout.itemAt(i))
        return items

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
