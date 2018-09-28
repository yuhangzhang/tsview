
from PyQt5.QtWidgets import QGraphicsScene

from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.pyplot as plt

from tsdata import TSData


class TSScene(QGraphicsScene):
    def __init__(self, width=14, height=4):
        super(TSScene, self).__init__()



        self.pixmap = QPixmap()

        self.figure = Figure()
        self.figure.set_size_inches(width, height)
        self.axes = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.canvas = FigureCanvas(self.figure)
        self.plothandle=self.addWidget(self.canvas)

        self.graphwidth = self.figure.dpi * width


        self.line = None

        self.downx = None
        self.data = None

        self.axes = self.figure.add_subplot(111)

        self.visibleWave = {}

        self.starttime = None
        self.endtime = None

    def togglewave(self, wavename, colorcode=0):
        if wavename in self.visibleWave:
            handle = (self.visibleWave[wavename])[1]
            self.removewave(handle)
            self.visibleWave.pop(wavename, None)
        else:
            waveform = self.data.getwaveform(wavename, self.starttime, self.endtime)
            handle = self.displaywave(wavename, waveform, colorcode)
            self.visibleWave[wavename] = (waveform, handle, colorcode)

    def displaywave(self, wavename, waveform, colorcode):

        #self.axes.remove()
        colorcode = 'C'+str(colorcode%10)

        times = [waveform.meta['starttime']+t for t in waveform.times()]
        handle = self.axes.plot(times, waveform.data,linestyle="-", label=wavename, color=colorcode)
        self.axes.legend()
        self.downx = None

        self.canvas.draw()

        self.starttime = waveform.meta['starttime']
        self.endtime = waveform.meta['endtime']

        return handle


    def displaywaveshift(self, shift):
        gap = self.endtime-self.starttime
        self.starttime = self.starttime + gap * shift
        self.endtime = self.endtime + gap * shift

        tmplist = self.visibleWave.copy()
        for wavename in tmplist:
            self.togglewave(wavename)
            self.togglewave(wavename, tmplist[wavename][2])


    def removewave(self, handle):
        handle.pop(0).remove()
        self.axes.relim()
        self.axes.autoscale_view(True, True, True)
        if len(self.visibleWave)>0:
            self.axes.legend()
        self.canvas.draw()


    def mousePressEvent(self, event):
        super(TSScene, self).mousePressEvent(event)
        self.downx = event.scenePos().x()


    def mouseMoveEvent(self, event):
        if self.downx is not None:
            self.upx = event.scenePos().x()
            #print(self.downx, self.upx)
            shift = float(self.downx - self.upx) / self.graphwidth
            self.displaywaveshift(shift)
            self.downx=self.upx

    def mouseReleaseEvent(self, event):
        super(TSScene, self).mousePressEvent(event)
        self.downx = None

    def wheelEvent(self, event):
        super(TSScene, self).wheelEvent(event)

        delta = -event.delta() / 8 / 15

        self.displaywave(self.data.getwaveformresample(delta))



    def setdata(self, filename):
        self.data = TSData(filename)
        #self.displaywave(wave)
        #self.displaywave(self.data.getwaveform('AU.VIC099'))

    def getList(self):
        return self.data.getList()