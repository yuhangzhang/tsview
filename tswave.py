import numpy as np
import obspy.core.trace as trace

class TSWave():
    def __init__(self, trace):
        self.times = []
        self.data = []
        self.decirate = None
        self.sampled = False
        self.sampledTrace = None

        self.setWave(trace)

    def setWave(self, trace):
        self.trace = trace

    def expandWave(self, trace):
        self.trace = self.trace.__add__(trace)


    def getWave(self, starttime=None, endtime=None, decirate=None):


        if starttime is None:
            starttime = self.trace.meta['starttime']
        if endtime is None:
            endtime = self.trace.meta['endtime']




        if decirate != self.decirate:
            self.decirate = decirate
            self.sampled = False

        if self.sampled == True:
            pass
        else:
            if self.decirate is None:
                self.decirate = round((endtime-starttime)/1000)

            if self.decirate>16:
                # tmpTrace = self.trace.copy()
                # genor = tmpTrace.slide(0.1, self.decirate)
                # self.sampledTrace = self.trace.copy().trim(self.trace.meta['starttime'],self.trace.meta['starttime'])
                # for window in genor:
                #     self.sampledTrace = self.sampledTrace.__add__(window)
                self.decirate=16
                self.sampledTrace = self.trace.copy().decimate(self.decirate, True)
            else:
                self.sampledTrace = self.trace.copy().decimate(self.decirate, True)

        self.sampled = True

        return self.sampledTrace.trim(starttime, endtime)