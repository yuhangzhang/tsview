
from PyQt5.QtWidgets import QGraphicsScene

from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.pyplot as plt

from tsasdf import TSASDF


class TSScene(QGraphicsScene):
    def __init__(self, width=16, height=4):
        super(TSScene, self).__init__()



        self.pixmap = QPixmap()

        self.figure = Figure(edgecolor='r', linewidth=2)
        self.figure.set_size_inches(width, height)
        self.axes = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.canvas = FigureCanvas(self.figure)
        self.plothandle=self.addWidget(self.canvas)

        self.unitperpixel = 1.5 / self.figure.dpi / width

        self.line = None

        self.downx = None

    def displaywave(self, waveform):


        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        self.axes.plot(waveform[0], waveform[1])

        self.downx = None

        self.canvas.draw()




    def mousePressEvent(self, event):
        super(TSScene, self).mousePressEvent(event)
        self.downx = event.scenePos().x()


    def mouseMoveEvent(self, event):
        if self.downx is not None:
            self.upx = event.scenePos().x()
            #print(self.downx, self.upx)
            shift = (self.downx - self.upx) * self.unitperpixel
            self.displaywave(self.data.getwaveformshift(shift))
            self.downx=self.upx

    def mouseReleaseEvent(self, event):
        super(TSScene, self).mousePressEvent(event)
        self.downx = None

    def wheelEvent(self, event):
        super(TSScene, self).wheelEvent(event)

        delta = -event.delta() / 8 / 15

        self.displaywave(self.data.getwaveformresample(delta))



    def setdata(self,filename):
        self.data = TSASDF(filename)
        self.displaywave(self.data.getwaveform('AU.VIC099'))