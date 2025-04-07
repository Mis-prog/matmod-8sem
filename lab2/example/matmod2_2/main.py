from importlib import import_module

from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget,
                             )
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from View import View
from View2 import View2
from View3 import View3
from View4 import View4

import matplotlib.pyplot as plt

# print(self.prior)
# Press the green button in the gutter to run the script.

ACTIVE, TAKT = [], []


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "MyProject"
        self.top = 150
        self.left = 150
        self.width = 800
        self.height = 800
        self.InitWindow()
        self.view = View3(self.width, self.height) #3 задание
        # self.view=View4(self.width,self.height)  # 4 задание
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(100)
        self.count = 0
        # self.setLayout(layout)
        self.setCentralWidget(self.view)

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def showTime(self):
        print("Живых клеток: ", self.view.countAliveCells())
        self.view.showTime(self.count)
        self.count += 1
        TAKT.append(self.count)
        ACTIVE.append(self.view.countAliveCells())
        self.update()

        if self.count >= 50:
            self.timer.stop()
            self.plot_graph()

    def plot_graph(self):
        plt.plot(TAKT, ACTIVE)
        plt.xlabel('Время (шаги)')
        plt.ylabel('Количество живых клеток')
        plt.title('Динамика живых клеток')
        plt.show()


App = QApplication(sys.argv)
window = Window()
# window.show()

sys.exit(App.exec())

