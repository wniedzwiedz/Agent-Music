from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.Qt6 import *

import sys, time, random

from external import fluidsynth
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
        self.loop_checkbox = QCheckBox("Loop")
        self.barLayout.addWidget(self.loop_checkbox)

        self.players = []
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.createPlayer)
        self.optionsLayout.addWidget(add_button)

        self.timer = QTimer()
        self.setTimer(1000)
        self.timer.stop()

    def createPlayer(self):
        player = Player()
        self.players.append(player)
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
        self.setTimer(60)
        for player in self.players:
            player.reset()

    def stopClicked(self):
        self.timer.stop()

    def step(self):
        for player in self.players:
            player.step()

app = QApplication(sys.argv)
window = MainWindow()
window.show()

testFluidsynth = False

if testFluidsynth:
    fs = fluidsynth.Synth()
    fs.start()

    sfid = fs.sfload("example.sf2")
    fs.program_select(0, sfid, 0, 0)

    fs.noteon(0, 60, 30)
    fs.noteon(0, 67, 30)
    fs.noteon(0, 76, 30)

    time.sleep(1.0)

    fs.noteoff(0, 60)
    fs.noteoff(0, 67)
    fs.noteoff(0, 76)

    time.sleep(1.0)

    fs.delete()

app.exec()
