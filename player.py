from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.Qt6 import *

from canvas import *

class Player(Canvas):
    def __init__(self):
        super().__init__()
        self.stepCounter = 0

    def reset(self):
        self.stepCounter = 0

    def step(self):
        self.highlightColumn(self.stepCounter)
        self.play(self.stepCounter)

        self.stepCounter += 1
        self.update()

    def play(self, col):
        pass
