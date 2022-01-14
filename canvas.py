import random

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QSizePolicy
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.Qt6 import *

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.highlightedColumn = -1
        self.board = None
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def highlightColumn(self, col):
        self.highlightedColumn = col

    def setBoard(self, board):
        self.board = board

    def verticalCells(self):
        return abs(self.board.highestKey - self.board.lowestKey + 1)

    def horizontalCells(self):
        return len(self.board.notes)

    def getLeftBorder(self):
        return 60

    def getCellWidth(self):
        width = self.size().width() - self.getLeftBorder()
        return width // self.horizontalCells()

    def getCellHeight(self):
        return self.size().height() // self.verticalCells()

    def getCellPosition(self, x, y):
        dx = self.getLeftBorder() + x * self.getCellWidth()
        dy = (self.verticalCells() - y - 1) * self.getCellHeight()
        return dx, dy

    def getCellWindowPosition(self, dx, dy):
        x = (-self.getLeftBorder() + dx) // self.getCellWidth()
        y = (self.verticalCells() - 1 - dy) // self.getCellHeight()
        return x, y

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(168, 34, 3))
        qp.drawRect(QRect(0, 0, self.size().width() - 1, self.size().height() - 1))

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))
        qp.setFont(QFont('Decorative', max(2, self.getCellHeight() - 2)))

        for y in range(0, self.verticalCells()):
            for x in range(0, self.horizontalCells()):
                keyNumber = self.board.lowestKey+y
                filled = False
                if self.board:
                    if self.board.getNote(x, keyNumber):
                        filled = True

                if self.highlightedColumn == x:
                    if filled:
                        qp.setBrush(QColor(40, 120, 60))
                    else:
                        qp.setBrush(QColor(220, 200, 250))
                else:
                    if filled:
                        qp.setBrush(QColor(0, 0, 0))
                    else:
                        qp.setBrush(QColor(255, 255, 255))
                

                dx, dy = self.getCellPosition(x, y)
                qp.drawRect(QRect(dx, dy, self.getCellWidth(), self.getCellHeight()))
            qp.drawText(QRect(0, dy, 
                              self.getLeftBorder(), self.getCellHeight()), 
                              0x0082, str(keyNumber))

        qp.end()
