from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget,
                             )
import sys
import math
import random
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from copy import copy, deepcopy

T=5
B=8
P=3
A=0.3
class View2(QWidget):
    def __init__(self, width, height, N=256):
        super().__init__()
        self.title = "PyQt5 Drawing Tutorial"
        self.top = 150
        self.left = 150
        self.width = width
        self.height = height
        self.InitWindow()
        self.N = N
        self.source=0
        self.colors = [Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.black, Qt.gray]
        self.cells_state = [[0] * self.N for i in range(self.N)]
        self.takt = [[0] * self.N for i in range(self.N)]
        self.act = [[0] * self.N for i in range(self.N)]
        # self.cells_state[15][14]=1
        # self.cells_state[15][15] = 1
        # self.cells_state[15][16] = 1
        # self.cells_state[17][14] = 1
        # self.cells_state[17][15] = 1
        # self.cells_state[17][16] = 1
        for i in range(self.N):
            self.cells_state[50][i]=1
            #self.cells_state[-1][i]=1
            self.takt[50][i] = T
            #self.takt[-1][i] = T
            self.act[50][i] = 1
            #self.act[-1][i]=1
        i = int(self.N / 2)
        j = int(self.N / 2)
        for k in range(i - 1, i + 2):
            for l in range(j - 1, j + 2):
                self.cells_state[k][l] = 1
                self.takt[k][l] = T

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def action(self):
        new_cells_state = deepcopy(self.cells_state)

        for i in range(self.N):
            for j in range(self.N):
                count = 0
                if self.cells_state[i][j]==0:
                    for k in range(i - 1, i + 2):
                        for l in range(j - 1, j + 2):
                            if (l < self.N and l >= 0 and k < self.N and k >= 0):
                                count += self.act[k][l]
                    if count>=P:
                        new_cells_state[i][j]=1
                        self.takt[i][j]=T+1
        for i in range(self.N):
            for j in range(self.N):
                if self.takt[i][j]>0:
                    self.takt[i][j]-=1
                if self.takt[i][j]==0:
                    if new_cells_state[i][j]==2:
                        new_cells_state[i][j]=0
                    if new_cells_state[i][j]==1:
                        new_cells_state[i][j]=2
                        self.takt[i][j] = B

                self.act[i][j]*=(1-A)
                if new_cells_state[i][j]==1:
                    self.act[i][j] =1
        if self.source==0:
            i = int(self.N / 2)
            j = int(self.N / 2)
            for k in range(i - 1, i + 2):
                for l in range(j - 1, j + 2):
                    new_cells_state[k][l] = 1
                    self.takt[k][l] = T
        self.source+=1
        self.source%=15

        self.cells_state = new_cells_state

    def showTime(self,count):
        print(count)
        self.action()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        h = int(min(self.width, self.height) / self.N)
        for i in range(self.N):
            for j in range(self.N):
                if self.cells_state[i][j] == 0:
                    color = Qt.black
                if self.cells_state[i][j] == 1:
                    color = Qt.red
                if self.cells_state[i][j] == 2:
                    color = Qt.yellow
                painter.setBrush(QBrush(color, Qt.SolidPattern))
                painter.setPen(QPen(color, 1, Qt.SolidLine))
                painter.drawRect(j * h, i * h, h, h)
        # painter.drawRect(20, 20, 100, 100)