from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.Qt6 import *

import sys, time, random
from functools import partial

from player import *

RULES = [
    'Repetitive Chords', 
    'Increase', 
    'Elementary', 
    'Chord Melody', 
    'AB',
    'Every Nth', 
    'Combine'
]

DRUM_RULES = [
    'Every Nth'
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
        for scale in ['Major', 'minor']:
            self.optionsScaleCombo.addItem(scale)
        self.optionsLayout.addWidget(self.optionsScaleCombo)
        self.optionsLayout.addWidget(QLabel("Scale"))

        self.optionsOctaveCombo = QComboBox()
        for octave in ['-5', '-4', '-3', '-2' ,'-1', '0', '1', '2', '3', '4', '5']:
            self.optionsOctaveCombo.addItem(octave)
        self.optionsLayout.addWidget(self.optionsOctaveCombo)
        self.optionsLayout.addWidget(QLabel("Octave"))
        

        self.optionsInstrumentCombo = QComboBox()
        self.optionsInstrumentCombo.addItems(Player.INSTRUMENTS.keys())
        self.optionsLayout.addWidget(self.optionsInstrumentCombo)
        self.optionsLayout.addWidget(QLabel("Instrument"))

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
        self.drumsStepSlider.setMinimum(0)
        self.drumsStepSlider.setMaximum(16)
        self.drumsStepSlider.setTickInterval(1)
        self.drumsOptionsLayout.addWidget(self.drumsStepSlider)
        self.drumsOptionsLayout.addWidget(QLabel("Step"))

        self.drumsShiftSlider = QSlider(Qt.Orientation.Horizontal)
        self.drumsShiftSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.drumsShiftSlider.setPageStep(1)
        self.drumsShiftSlider.setSingleStep(1)
        self.drumsShiftSlider.setMinimum(0)
        self.drumsShiftSlider.setMaximum(16)
        self.drumsShiftSlider.setTickInterval(1)
        self.drumsOptionsLayout.addWidget(self.drumsShiftSlider)
        self.drumsOptionsLayout.addWidget(QLabel("Shift"))

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
        combineRuleRemoveRule.clicked.connect(lambda :  
            self.removeLastItem(self.combineRuleRulesLayout)
        )
        self.combineRuleLayout.addWidget(combineRuleRemoveRule)
        combineRuleAddRule = QPushButton("+")
        combineRuleAddRule.setMaximumSize(QSize(24, 24))
        combineRuleAddRule.clicked.connect(lambda :  
            self.combineRuleRulesLayout.addWidget(self.copyCombo(self.optionsRuleCombo))
        )
        self.combineRuleLayout.addWidget(combineRuleAddRule)
        self.combineRuleRulesCombo = self.copyCombo(self.optionsRuleCombo)
        self.combineRuleRulesLayout.addWidget(self.combineRuleRulesCombo)

        # if default (current) option is not "Combine"
        if self.optionsRuleCombo.currentText != "Combine":
            self.layoutSetChildrenVisible(self.combineRuleRulesLayout, False)
            self.layoutSetChildrenVisible(self.combineRuleLayout, False)

        # Audio players
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
        options['rules'] = [ 
            item.widget().currentText() for item in self.layoutItems(self.combineRuleRulesLayout) 
        ]
        options['percussion'] = self.drumsCombo.currentText()
        options['percussion_step'] = self.drumsStepSlider.value()
        options['percussion_shift'] = self.drumsShiftSlider.value()

        print(options)
        player = Player(options)
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

    def removeLastItem(self, layout):
        if layout.count() <= 0:
            return

        item = layout.itemAt(layout.count() - 1)
        if item.widget():
            item.widget().deleteLater()
        layout.removeItem(item)

    def layoutItems(self, layout):
        items = []
        for i in range(layout.count()):
            items.append(layout.itemAt(i))
        return items

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
