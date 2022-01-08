import random

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.Qt6 import *

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.highlightedColumn = -1
        self.board = None

    def highlightColumn(self, col):
        self.highlightedColumn = col

    def setBoard(self, board):
        self.board = board

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), 0, "Notes")     
        qp.drawRect(QRect(0, 0, self.size().width() - 1, self.size().height() - 1))

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))

        cellsH = len(self.board.notes)
        cellsV = 40
        cellWidth = self.size().width() // cellsH
        cellHeight = self.size().height() // cellsV

        MARGIN = 1

        for y in range(0, cellsV):
            for x in range(0, cellsH):
                filled = False
                if self.board:
                    if self.board.getNote(x, 80+y):
                        filled = True

                if self.highlightedColumn == x:
                    if filled:
                        qp.setBrush(QColor(40, 90, 60))
                    else:
                        qp.setBrush(QColor(220, 200, 230))
                else:
                    if filled:
                        qp.setBrush(QColor(0, 0, 0))
                    else:
                        qp.setBrush(QColor(255, 255, 255))

                qp.drawRect(QRect(MARGIN + x * cellWidth, MARGIN + y * cellHeight, 
                                  cellWidth - MARGIN, cellHeight - MARGIN))

        qp.end()
