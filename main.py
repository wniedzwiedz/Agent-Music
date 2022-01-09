from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.Qt6 import *

import sys, time, random
from functools import partial

from player import *

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
        for instrument in ['Piano', 'Drums']:
            self.optionsInstrumentCombo.addItem(instrument)
        self.optionsLayout.addWidget(self.optionsInstrumentCombo)
        self.optionsLayout.addWidget(QLabel("Instrument"))
        
        self.optionsRuleCombo = QComboBox()
        for rule in ['Increase', 'Elementary', 'Melody', 'AB']:
            self.optionsRuleCombo.addItem(rule)
        self.optionsLayout.addWidget(self.optionsRuleCombo)
        self.optionsLayout.addWidget(QLabel("Rule"))

        self.players = []
        addButton = QPushButton("Add")
        addButton.clicked.connect(self.createPlayer)
        self.optionsLayout.addWidget(addButton)

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


    def step(self):
        for player in self.players:
            player.step()

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
