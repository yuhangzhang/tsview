
import pyasdf
import obspy.core.trace as trace
import numpy as np

class TSASDF():
    def __init__(self, filename):
        self.rawdata = pyasdf.ASDFDataSet(filename, mode="r")

        self.start=0
        self.end=100
        self.decirate = 1
        #self.times = trace.Trace(self.rawdata.waveforms[waveformname].raw_recording[0].times())
        #self.data = trace.Trace(self.rawdata.waveforms[waveformname].raw_recording[0].data)

        self.rawtimes = np.array(self.rawdata.waveforms['AU.VIC099'].raw_recording[0].times())#.copy()
        self.rawdata = np.array(self.rawdata.waveforms['AU.VIC099'].raw_recording[0].data)#.copy()

        self.currenttimes = self.rawtimes.copy()
        self.currentdata = self.rawdata.copy()

        self.currentwaveformname = ''



    def getwaveform(self, waveformname, start=None, end=None):
        if start is None:
            start = self.start
        else:
            self.start = start

        if end is None:
            end = self.end
        else:
            self.end = end

        if self.currentwaveformname != waveformname:
            self.times = np.array(self.currenttimes[start: end])
            self.data = np.array(self.currentdata[start: end])
            self.currentwaveformname = waveformname

        return [self.times,
                self.data]

    def getwaveformshift(self, shift):

        shift = (self.end-self.start+1)*shift

        if self.start==0 and shift<0:
            pass
        elif self.end == len(self.currentdata) and shift >0:
            pass
        else:
            if self.start+shift<0:
                shift = -self.start
            if self.end+shift>len(self.currentdata):
                shift = len(self.currentdata) -self.end

            self.start = int(self.start+shift)
            self.end = int(self.end+shift)

            self.times = np.array(self.currenttimes[self.start: self.end])
            self.data = np.array(self.currentdata[self.start: self.end])

        return [self.times,
                self.data]

    def getwaveformresample(self, shift):

        if self.decirate==1 and shift<0:
            pass
        elif self.decirate==16 and shift>0:
            pass
        elif shift==0:
            pass
        else:
            #print("shift=",shift)

            #self.end = float(self.decirate) / (self.decirate + shift)
            decirate = int(self.decirate + shift)

            if decirate < 1:
                decirate = 1
            if decirate > 16:
                decirate = 16




            self.currenttimes = trace.Trace(
                self.rawtimes).decimate(decirate,True).copy()


            self.currentdata = trace.Trace(
                self.rawdata).decimate(decirate,True).copy()



            gap = self.end-self.start
            self.start = int(float(self.start) * self.decirate / decirate)
            self.end = self.start+gap
            #self.end = int(float(self.end) * decirate / self.decirate)
            if self.end<1:
                self.end=1
            if self.end>len(self.currentdata):
                self.end=len(self.currentdata)


            self.decirate = decirate

            self.times = np.array(self.currenttimes[self.start: self.end])
            self.data = np.array(self.currentdata[self.start: self.end])

        #print('scale',self.start,self.end,self.decirate)

        return [self.times,
                self.data]

    def getwaveformnames(self):
        return self.rawdata.waveforms.list()

    def recommendaspect(self):
        self.aspect = float(self.times.max()-self.times.min())/(self.data.max()-self.data.min())/10

        return self.aspect
