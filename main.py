from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.Qt6 import *

import sys

class Canvas(QWidget):
    pass

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
        self.barLayout.addWidget(QPushButton("Play ▶"))
        self.barLayout.addWidget(QPushButton("Stop ■"))
        self.barLayout.addWidget(QCheckBox("Loop"))

        print("Creating canvas...")
        self.canvas = Canvas()
        self.layout.addWidget(self.canvas)



app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
