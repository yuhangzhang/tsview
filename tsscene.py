
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

        self.wheelactive = False

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


    def timeshift(self, shift):
        shift = (self.endtime-self.starttime)*shift

        starttime = self.starttime + shift
        endtime = self.endtime + shift

        for wavename in self.visibleWave:
            if starttime<self.data.dict[wavename].starttime():
                starttime = self.starttime
            if endtime>self.data.dict[wavename].endtime():
                endtime = self.endtime

        if starttime!=self.starttime and endtime!=self.endtime:
            self.starttime = starttime
            self.endtime = endtime
            tmplist = self.visibleWave.copy()
            for wavename in tmplist:
                self.togglewave(wavename)
                self.togglewave(wavename, tmplist[wavename][2])


    def timescale(self, delta):
        shift = (self.endtime - self.starttime) * -delta*0.1

        starttime = self.starttime + shift
        endtime = self.endtime - shift

        for wavename in self.visibleWave:
            if starttime<self.data.dict[wavename].starttime():
                starttime = self.starttime
            if endtime>self.data.dict[wavename].endtime():
                endtime = self.endtime

        if endtime-starttime<60:
            pass
        elif starttime==self.starttime and endtime==self.endtime:
            pass
        else:
            self.starttime = starttime
            self.endtime = endtime
            tmplist = self.visibleWave.copy()
            for wavename in tmplist:
                self.togglewave(wavename)
                self.togglewave(wavename, tmplist[wavename][2])

        self.wheelactive = False

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
            shift = float(self.downx - self.upx) / self.graphwidth
            self.timeshift(shift)
            self.downx=self.upx

    def mouseReleaseEvent(self, event):
        super(TSScene, self).mousePressEvent(event)
        self.downx = None

    def wheelEvent(self, event):
        super(TSScene, self).wheelEvent(event)

        delta = -event.delta() / 8 / 15

        if self.wheelactive==False:
            self.wheelactive = True
            self.timescale(delta)





    def setdata(self, filename):
        self.data = TSData(filename)

    def getList(self):
        return self.data.getList()