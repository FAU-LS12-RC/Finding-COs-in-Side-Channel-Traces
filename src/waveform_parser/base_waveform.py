#!/usr/bin/python3

class BaseWaveform:
	
    def __init__(self):
        self.dataValues = list()
        self.horizontalTimeAtFrameStart = 0
        self.horizontalTimePerSample = 0
        self.horizontalUnit = ""
        self.verticalUnit = ""
        self.byteArray = list()

    def getDataValues(self):
        timeValues = list()
        if self.horizontalTimePerSample != 0:
            for timestamp in range(0, len( self.dataValues ), 1):
                timeValues.append(self.horizontalTimeAtFrameStart + (self.horizontalTimePerSample * timestamp) )
        return timeValues, self.dataValues

    def pushBackValue(self, value):
        self.dataValues.append(value)

    def getTimeAtFrameStart(self):
        return self.horizontalTimeAtFrameStart

    def setTimeAtFrameStart(self, timestamp):
        self.horizontalTimeAtFrameStart = timestamp

    def getTimePerSample(self):
        return self.horizontalTimePerSample

    def setTimePerSample(self, timeInterval):
        self.horizontalTimePerSample = timeInterval

    def getHorizontalUnit(self):
        return self.horizontalUnit

    def setHorizontalUnit(self, unit):
        self.horizontalUnit = unit

    def getVerticalUnit(self):
        return self.verticalUnit

    def setVerticalUnit(self, unit):
        self.verticalUnit = unit

    def getBytesArray(self):
        return self.byteArray

    def setBytesArray(self, byteArray):
        self.byteArray = byteArray