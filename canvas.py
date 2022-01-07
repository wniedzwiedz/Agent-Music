import random

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.Qt6 import *

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.highlightedColumn = -1

    def highlightColumn(self, col):
        self.highlightedColumn = col

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), 0, "Notes")     
        qp.drawRect(QRect(0, 0, self.size().width() - 1, self.size().height() - 1))

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))

        cellsH = 10
        cellsV = 6
        cellWidth = self.size().width() // cellsH
        cellHeight = self.size().height() // cellsV

        for y in range(0, cellsV):
            for x in range(0, cellsH):
                if self.highlightedColumn == x:
                    qp.setBrush(QColor(100, 100, 100))
                else:
                    qp.setBrush(QColor(0, 0, 0))

                if random.random() < 0.4:
                    qp.drawRect(QRect(2 + x * cellWidth, 
                        2 + y * cellHeight, 
                        cellWidth - 2, 
                        cellHeight - 2))

        qp.end()
