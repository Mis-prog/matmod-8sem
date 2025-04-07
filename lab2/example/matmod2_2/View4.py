from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget,
                             )
import time
import sys
import math
import random
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from copy import copy, deepcopy
pmax=10
r=1
dp=5
p1=35
de=2
L=15
dr=3
A=0.3
T=3
class View4(QWidget):
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
        self.p = [[pmax] * self.N for i in range(self.N)]
        self.e= [[0] * self.N for i in range(self.N)]
        self.life = [[0] * self.N for i in range(self.N)]
        # self.cells_state[15][14]=1
        # self.cells_state[15][15] = 1
        # self.cells_state[15][16] = 1
        # self.cells_state[17][14] = 1
        # self.cells_state[17][15] = 1
        # self.cells_state[17][16] = 1
        for i in range(int(A*N*N)):
            self.cells_state[random.randint(0, int((self.N - 1)/2))][random.randint(0, self.N - 1)] = 1


    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def action(self):
        new_cells_state = deepcopy(self.cells_state)

        for i in range(self.N):
            for j in range(self.N):
                if self.p[i][j]!=pmax:
                    self.p[i][j]+=r
                self.p[i][j]=min(pmax,self.p[i][j])
                if self.cells_state[i][j]==1:
                    if self.p[i][j] >=dp:
                        self.p[i][j]-=dp
                        self.e[i][j] += dp
                        self.e[i][j] =min(p1,self.e[i][j])
                    self.e[i][j] -= de
                    self.life[i][j]+=1

                    if self.life[i][j]>L or self.e[i][j]<=0:
                        self.cells_state[i][j]=0
                        self.e[i][j] =0
                        self.life[i][j] =0
        move = [[1] * self.N for i in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if self.cells_state[i][j]==1 and move[i][j]==1:
                    bk=i
                    bl=j
                    bp=self.p[i][j]
                    for k in range(i - 1, i + 2):
                        for l in range(j - 1, j + 2):
                            if k >= 0 and k < self.N and l >= 0 and l< self.N:
                                if self.cells_state[k][l]==0:
                                    if self.p[k][l]>bp:
                                        bk=k
                                        bl=l
                                        bp=self.p[k][l]
                    move[bk][bl] = 0
                    if bk!=i or bl!=j:
                        self.cells_state[i][j] = 0
                        self.cells_state[bk][bl] = 1
                        self.e[bk][bl] = self.e[i][j]
                        self.life[bk][bl] = self.life[i][j]
                        self.e[i][j] = 0
                        self.life[i][j] = 0
        done = [[1] * self.N for i in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if self.cells_state[i][j]==1 and done[i][j]==1:
                    if self.e[i][j]>=dr and self.life[i][j]>=T:
                        dest=1
                        for k in range(i - 1, i + 2):
                            for l in range(j - 1, j + 2):
                                if (dest==1 and l < self.N and l >= 0 and k < self.N and k >= 0 and (l != j or k != i)):
                                    self.cells_state[k][l]=1
                                    self.e[i][j]-=dr
                                    self.e[k][l]=self.e[i][j]
                                    done[k][l]=0
                                    self.life[k][l] = self.life[i][j]
                                    self.e[i][j] = 0
                                    self.life[i][j] = 0
                                    dest=0

    def showTime(self, count):
        print(count)
        self.action()
        self.update()
        # if count %10==0 and count>0:
        #     time.sleep(10)


    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        h = int(min(self.width, self.height) / self.N)
        for i in range(self.N):
            for j in range(self.N):
                if self.cells_state[i][j] == 0:
                    color = Qt.white
                if self.cells_state[i][j] == 1:
                    color = Qt.yellow
                painter.setBrush(QBrush(color, Qt.SolidPattern))
                painter.setPen(QPen(color, 1, Qt.SolidLine))
                painter.drawRect(j * h, i * h, h, h)
        # painter.drawRect(20, 20, 100, 100)
    def countAliveCells(self):
        count = 0
        for i in range(self.N):
            for j in range(self.N):
                if self.cells_state[i][j] == 1:
                    count += 1
        return count