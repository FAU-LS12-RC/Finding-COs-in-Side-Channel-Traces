#!/usr/bin/python3

from enum import IntEnum

from src.waveform_parser.base_waveform import BaseWaveform


class LecroyWaveformDescriptor:

    class CommType(IntEnum):
        BYTE_FORMAT = 0
        WORD_FORMAT = 1

    class CommOrder(IntEnum):
        HIGH_BYTE_FIRST = 0
        LOW_BYTE_FIRST = 1

    class RecordType(IntEnum):
        SINGLE_SWEEP = 0
        INTERLEAVED = 1
        HISTOGRAM = 2
        GRAPH = 3
        FILTER_COEFFICIENT = 4
        COMPLEX = 5
        EXTREMA = 6
        SEQUENCE_OBSOLETE = 7
        CENTERED_RIS = 8
        PEAK_DETECT = 9

    class ProcessingDone(IntEnum):
        NO_PROCESSING = 0
        FIR_FILTER = 1
        INTERPOLATED = 2
        SPARSED = 3
        AUTOSCALED = 4
        NO_RESULT = 5
        ROLLING = 6
        CUMULATIVE = 7

    class Timebase(IntEnum):
        TIMEBASE_1_PS_PER_DIV = 0
        TIMEBASE_2_PS_PER_DIV = 1
        TIMEBASE_5_PS_PER_DIV = 2
        TIMEBASE_10_PS_PER_DIV = 3
        TIMEBASE_20_PS_PER_DIV = 4
        TIMEBASE_50_PS_PER_DIV = 5
        TIMEBASE_100_PS_PER_DIV = 6
        TIMEBASE_200_PS_PER_DIV = 7
        TIMEBASE_500_PS_PER_DIV = 8
        TIMEBASE_1_NS_PER_DIV = 9
        TIMEBASE_2_NS_PER_DIV = 10
        TIMEBASE_5_NS_PER_DIV = 11
        TIMEBASE_10_NS_PER_DIV = 12
        TIMEBASE_20_NS_PER_DIV = 13
        TIMEBASE_50_NS_PER_DIV = 14
        TIMEBASE_100_NS_PER_DIV = 15
        TIMEBASE_200_NS_PER_DIV = 16
        TIMEBASE_500_NS_PER_DIV = 17
        TIMEBASE_1_US_PER_DIV = 18
        TIMEBASE_2_US_PER_DIV = 19
        TIMEBASE_5_US_PER_DIV = 20
        TIMEBASE_10_US_PER_DIV = 21
        TIMEBASE_20_US_PER_DIV = 22
        TIMEBASE_50_US_PER_DIV = 23
        TIMEBASE_100_US_PER_DIV = 24
        TIMEBASE_200_US_PER_DIV = 25
        TIMEBASE_500_US_PER_DIV = 26
        TIMEBASE_1_MS_PER_DIV = 27
        TIMEBASE_2_MS_PER_DIV = 28
        TIMEBASE_5_MS_PER_DIV = 29
        TIMEBASE_10_MS_PER_DIV = 30
        TIMEBASE_20_MS_PER_DIV = 31
        TIMEBASE_50_MS_PER_DIV = 32
        TIMEBASE_100_MS_PER_DIV = 33
        TIMEBASE_200_MS_PER_DIV = 34
        TIMEBASE_500_MS_PER_DIV = 35
        TIMEBASE_1_S_PER_DIV = 36
        TIMEBASE_2_S_PER_DIV = 37
        TIMEBASE_5_S_PER_DIV = 38
        TIMEBASE_10_S_PER_DIV = 39
        TIMEBASE_20_S_PER_DIV = 40
        TIMEBASE_50_S_PER_DIV = 41
        TIMEBASE_100_S_PER_DIV = 42
        TIMEBASE_200_S_PER_DIV = 43
        TIMEBASE_500_S_PER_DIV = 44
        TIMEBASE_1_KS_PER_DIV = 45
        TIMEBASE_2_KS_PER_DIV = 46
        TIMEBASE_5_KS_PER_DIV = 47
        EXTERNAL = 100

    class VerticalCoupling(IntEnum):
        DC_50_OHMS = 0
        DC_GROUND = 1
        DC_1_MOHM = 2
        AC_GROUND = 3
        AC_1_MOHM = 4

    class FixedVerticalGain(IntEnum):
        GAIN_1uV_PER_DIV = 0
        GAIN_2uV_PER_DIV = 1
        GAIN_5uV_PER_DIV = 2
        GAIN_10uV_PER_DIV = 3
        GAIN_20uV_PER_DIV = 4
        GAIN_50uV_PER_DIV = 5
        GAIN_100uV_PER_DIV = 6
        GAIN_200uV_PER_DIV = 7
        GAIN_500uV_PER_DIV = 8
        GAIN_1mV_PER_DIV = 9
        GAIN_2mV_PER_DIV = 10
        GAIN_5mV_PER_DIV = 11
        GAIN_10mV_PER_DIV = 12
        GAIN_20mV_PER_DIV = 13
        GAIN_50mV_PER_DIV = 14
        GAIN_100mV_PER_DIV = 15
        GAIN_200mV_PER_DIV = 16
        GAIN_500mV_PER_DIV = 17
        GAIN_1V_PER_DIV = 18
        GAIN_2V_PER_DIV = 19
        GAIN_5V_PER_DIV = 20
        GAIN_10V_PER_DIV = 21
        GAIN_20V_PER_DIV = 22
        GAIN_50V_PER_DIV = 23
        GAIN_100V_PER_DIV = 24
        GAIN_200V_PER_DIV = 25
        GAIN_500V_PER_DIV = 26
        GAIN_1kV_PER_DIV = 27

    class BandwidthLimit(IntEnum):
        BANDWIDTH_LIMIT_OFF = 0
        BANDWIDTH_LIMIT_ON = 1

    class WaveSource(IntEnum):
        CHANNEL_1 = 0
        CHANNEL_2 = 1
        CHANNEL_3 = 2
        CHANNEL_4 = 3
        UNKNOWN_CHANNEL = 9

    def __init__(self):
        self.descriptorName = "Default"
        self.templateName = "Default"
        self.commType = self.CommType.BYTE_FORMAT
        self.commOrder = self.CommOrder.HIGH_BYTE_FIRST
        self.waveDescriptorLength = 0
        self.userTextLength = 0
        self.reservedDescriptor1Length = 0
        self.trigTimeArrayLength = 0
        self.risTimeArrayLength = 0
        self.reservedArray1Length = 0
        self.waveArray1Length = 0
        self.waveArray2Length = 0
        self.reservedArray2Length = 0
        self.reservedArray3Length = 0
        self.instrumentName = "Lecroy HDO6054A"
        self.instrumentNumber = 0
        self.traceLabel = "Default"
        self.reservedEntry1 = 0
        self.reservedEntry2 = 0
        self.waveArrayCount = 0
        self.pointsPerScreen = 0
        self.firstValidPoint = 0
        self.lastValidPoint = 0
        self.firstPoint = 0
        self.sparsingFactor = 0
        self.segmentIndex = 0
        self.suArrayCount = 0
        self.sweepsPerAcquisition = 0
        self.pointsPerPair = 0
        self.pairOffset = 0
        self.verticalGain = 0.0
        self.verticalOffset = 0.0
        self.maximumValue = 0.0
        self.minimumValue = 0.0
        self.nominalITS = 0
        self.nominalSUArrayCount = 0
        self.horizontalInterval = 1.0
        self.horizontalOffset = 0.0
        self.pixelOffset = 0.0
        self.verticalUnit = "V"
        self.horizontalUnit = "s"
        self.horizontalUncertainty = 0
        self.triggerTimeSeconds = 0.00
        self.triggerTimeMinutes = 0
        self.triggerTimeHours = 12
        self.triggerTimeDays = 20
        self.triggerTimeMonths = 2
        self.triggerTimeYears = 2020
        self.triggerTimeUnused = 0.0
        self.acquisitionDuration = 0.0
        self.recordType = self.RecordType.SINGLE_SWEEP
        self.processingDone = self.ProcessingDone.NO_PROCESSING
        self.reserved5Entry = 0
        self.risSweeps = 0
        self.timebase = self.Timebase.TIMEBASE_1_S_PER_DIV
        self.verticalCoupling = self.VerticalCoupling.DC_1_MOHM
        self.probeAttenuation = 10.0
        self.fixedVerticalGain = self.FixedVerticalGain.GAIN_1V_PER_DIV
        self.bandwidthLimit = self.BandwidthLimit.BANDWIDTH_LIMIT_OFF
        self.verticalVernier = 0.0
        self.acquisitionVerticalOffset = 0.0
        self.waveSource = self.WaveSource.UNKNOWN_CHANNEL

    def dump(self):
        print("[WAVEFORM DESCRIPTOR]")
        print("\t *Descriptor Name: " + self.getDescriptorName())
        print("\t *Template Name: " + self.getTemplateName())
        print("\t *CommType: " + str(self.getCommType()))
        print("\t *CommOrder: " + str(self.getCommOrder()))

        print("\t *WaveDescriptorBlockLength: " +
              str(self.getWaveDescriptorBlockLength()))
        print("\t *UserTextBlockLength: " + str(self.getUserTextBlockLength()))
        print("\t *ReservedDescriptor1BlockLength: " +
              str(self.getReservedDescriptor1BlockLength()))

        print("\t *TrigTimeArrayLength: " + str(self.getTrigTimeArrayLength()))
        print("\t *RISTimeArrayLength: " + str(self.getRISTimeArrayLength()))
        print("\t *WaveArray1Length: " + str(self.getWaveArray1Length()))
        print("\t *WaveArray2Length: " + str(self.getWaveArray2Length()))
        print("\t *ReservedArray1Length: " +
              str(self.getReservedArray1Length()))
        print("\t *ReservedArray2Length: " +
              str(self.getReservedArray2Length()))
        print("\t *ReservedArray3Length: " +
              str(self.getReservedArray3Length()))

        print("\t *InstrumentName: " + self.getInstrumentName())
        print("\t *InstrumentNumber: " + str(self.getInstrumentNumber()))
        print("\t *TraceLabel: " + self.getTraceLabel())
        print("\t *ReservedEntry1: " + str(self.getReservedEntry1()))
        print("\t *ReservedEntry2: " + str(self.getReservedEntry2()))

        print("\t *WaveArrayCount: " + str(self.getWaveArrayCount()))
        print("\t *PointsPerScreen: " + str(self.getPointsPerScreen()))
        print("\t *FirstValidPointIndex: " + str(self.getFirstValidPoint()))
        print("\t *LastValidPointIndex: " + str(self.getLastValidPoint()))

        print("\t *FirstPoint: " + str(self.getFirstPoint()))
        print("\t *SparsingFactor: " + str(self.getSparsingFactor()))
        print("\t *SegmentIndex: " + str(self.getSegmentIndex()))
        print("\t *SUArrayCount: " + str(self.getSUArrayCount()))
        print("\t *SweepsPerAcquisition: " +
              str(self.getSweepsPerAcquisition()))
        print("\t *PointsPerPair: " + str(self.getPointsPerPair()))
        print("\t *PairOffset: " + str(self.getPairOffset()))
        print("\t *VerticalGain: " + str(self.getVerticalGain()))
        print("\t *VerticalOffset: " + str(self.getVerticalOffset()))
        print("\t *MaximumValue: " + str(self.getMaximumValue()))
        print("\t *MinimumValue: " + str(self.getMinimumValue()))
        print("\t *NominalITS: " + str(self.getNominalITS()))
        print("\t *NominalSUArrayCount: " + str(self.getNominalSUArrayCount()))
        print("\t *HorizontalInterval: " + str(self.getHorizontalInterval()))
        print("\t *HorizontalOffset: " + str(self.getHorizontalOffset()))
        print("\t *PixelOffset: " + str(self.getPixelOffset()))
        print("\t *VerticalUnit: " + self.getVerticalUnit())
        print("\t *HorizontalUnit: " + self.getHorizontalUnit())
        print("\t *HorizontalUncertainty: " +
              str(self.getHorizontalUncertainty()))

        print("\t *TriggerTimeSeconds: " + str(self.getTriggerTimeSeconds()))
        print("\t *TriggerTimeMinutes: " + str(self.getTriggerTimeMinutes()))
        print("\t *TriggerTimeHours: " + str(self.getTriggerTimeHours()))
        print("\t *TriggerTimeDays: " + str(self.getTriggerTimeDays()))
        print("\t *TriggerTimeMonths: " + str(self.getTriggerTimeMonths()))
        print("\t *TriggerTimeYears: " + str(self.getTriggerTimeYears()))
        print("\t *TriggerTimeUnused: " + str(self.getTriggerTimeUnused()))

        print("\t *AcquisitionDuration: " + str(self.getAcquisitionDuration()))
        print("\t *RecordType: " + str(self.getRecordType()))
        print("\t *ProcessingDone: " + str(self.getProcessingDone()))
        print("\t *Reserved5Entry: " + str(self.getReserved5Entry()))
        print("\t *RIS Sweeps: " + str(self.getRISSweeps()))
        print("\t *Timebase: " + str(self.getTimebase()))
        print("\t *Vertical Coupling: " + str(self.getVerticalCoupling()))
        print("\t *Probe Attenuation: " + str(self.getProbeAttenuation()))
        print("\t *Fixed Vertical Gain: " + str(self.getFixedVerticalGain()))
        print("\t *Bandwidth Limit: " + str(self.getBandwidthLimit()))
        print("\t *Vertical Vernier: " + str(self.getVerticalVernier()))
        print("\t *Acuisition Vertical Offset: " +
              str(self.getAcquisitionVerticalOffset()))
        print("\t *Wave Source: " + str(self.getWaveSource()))

        print("[END WAVEFORM DESCRIPTOR]")

    def getDescriptorName(self):
        return self.descriptorName

    def setDescriptorName(self, name):
        self.descriptorName = name

    def getTemplateName(self):
        return self.templateName

    def setTemplateName(self, name):
        self.templateName = name

    def getCommType(self):
        return self.commType

    def setCommType(self, commType):
        self.commType = commType

    def getCommOrder(self):
        return self.commOrder

    def setCommOrder(self, order):
        self.commOrder = order

    def getWaveDescriptorBlockLength(self):
        return self.waveDescriptorLength

    def setWaveDescriptorBlockLength(self, length):
        self.waveDescriptorLength = length

    def getUserTextBlockLength(self):
        return self.userTextLength

    def setUserTextBlockLength(self, length):
        self.userTextLength = length

    def getReservedDescriptor1BlockLength(self):
        return self.reservedDescriptor1Length

    def setReservedDescriptor1BlockLength(self, length):
        self.reservedDescriptor1Length = length

    def getTrigTimeArrayLength(self):
        return self.trigTimeArrayLength

    def setTrigTimeArrayLength(self, length):
        self.trigTimeArrayLength = length

    def getRISTimeArrayLength(self):
        return self.risTimeArrayLength

    def setRISTimeArrayLength(self, length):
        self.risTimeArrayLength = length

    def getReservedArray1Length(self):
        return self.reservedArray1Length

    def setReservedArray1Length(self, length):
        self.reservedArray1Length = length

    def getWaveArray1Length(self):
        return self.waveArray1Length

    def setWaveArray1Length(self, length):
        self.waveArray1Length = length

    def getWaveArray2Length(self):
        return self.waveArray2Length

    def setWaveArray2Length(self, length):
        self.waveArray2Length = length

    def getReservedArray2Length(self):
        return self.reservedArray2Length

    def setReservedArray2Length(self, length):
        self.reservedArray2Length = length

    def getReservedArray3Length(self):
        return self.reservedArray3Length

    def setReservedArray3Length(self, length):
        self.reservedArray3Length = length

    def getInstrumentName(self):
        return self.instrumentName

    def setInstrumentName(self, name):
        self.instrumentName = name

    def getInstrumentNumber(self):
        return self.instrumentNumber

    def setInstrumentNumber(self, number):
        self.instrumentNumber = number

    def getTraceLabel(self):
        return self.traceLabel

    def setTraceLabel(self, label):
        self.traceLabel

    def getReservedEntry1(self):
        return self.reservedEntry1

    def setReservedEntry1(self, entry):
        self.reservedEntry1 = entry

    def getReservedEntry2(self):
        return self.reservedEntry2

    def setReservedEntry2(self, entry):
        self.reservedEntry2 = entry

    def getWaveArrayCount(self):
        return self.waveArrayCount

    def setWaveArrayCount(self, count):
        self.waveArrayCount = count

    def getPointsPerScreen(self):
        return self.pointsPerScreen

    def setPointsPerScreen(self, points):
        self.pointsPerScreen = points

    def getFirstValidPoint(self):
        return self.firstValidPoint

    def setFirstValidPoint(self, point):
        self.firstValidPoint = point

    def getLastValidPoint(self):
        return self.lastValidPoint

    def setLastValidPoint(self, point):
        self.lastValidPoint = point

    def getFirstPoint(self):
        return self.firstPoint

    def setFirstPoint(self, point):
        self.firstPoint = point

    def getSparsingFactor(self):
        return self.sparsingFactor

    def setSparsingFactor(self, factor):
        self.sparsingFactor = factor

    def getSegmentIndex(self):
        return self.segmentIndex

    def setSegmentIndex(self, index):
        self.segmentIndex = index

    def getSUArrayCount(self):
        return self.suArrayCount

    def setSUArrayCount(self, count):
        self.suArrayCount = count

    def getSweepsPerAcquisition(self):
        return self.sweepsPerAcquisition

    def setSweepsPerAcquisition(self, sweeps):
        self.sweepsPerAcquisition = sweeps

    def getPointsPerPair(self):
        return self.pointsPerPair

    def setPointsPerPair(self, points):
        self.pointsPerPair = points

    def getPairOffset(self):
        return self.pairOffset

    def setPairOffset(self, offset):
        self.pairOffset = offset

    def getVerticalGain(self):
        return self.verticalGain

    def setVerticalGain(self, gain):
        self.verticalGain = gain

    def getVerticalOffset(self):
        return self.verticalOffset

    def setVerticalOffset(self, offset):
        self.verticalOffset = offset

    def getMaximumValue(self):
        return self.maximumValue

    def setMaximumValue(self, value):
        self.maximumValue = value

    def getMinimumValue(self):
        return self.minimumValue

    def setMinimumValue(self, value):
        self.minimumValue = value

    def getNominalITS(self):
        return self.nominalITS

    def setNominalITS(self, nominalITS):
        self.nominalITS = nominalITS

    def getNominalSUArrayCount(self):
        return self.nominalSUArrayCount

    def setNominalSUArrayCount(self, nominalCount):
        self.nominalSUArrayCount = nominalCount

    def getHorizontalInterval(self):
        return self.horizontalInterval

    def setHorizontalInterval(self, interval):
        self.horizontalInterval = interval

    def getHorizontalOffset(self):
        return self.horizontalOffset

    def setHorizontalOffset(self, offset):
        self.horizontalOffset = offset

    def getPixelOffset(self):
        return self.pixelOffset

    def setPixelOffset(self, offset):
        self.pixelOffset = offset

    def getVerticalUnit(self):
        return self.verticalUnit

    def setVerticalUnit(self, unit):
        self.verticalUnit = unit

    def getHorizontalUnit(self):
        return self.horizontalUnit

    def setHorizontalUnit(self, unit):
        self.horizontalUnit = unit

    def getHorizontalUncertainty(self):
        return self.horizontalUncertainty

    def setHorizontalUncertainty(self, uncertainty):
        self.horizontalUncertainty = uncertainty

    def getTriggerTimeSeconds(self):
        return self.triggerTimeSeconds

    def setTriggerTimeSeconds(self, seconds):
        self.triggerTimeSeconds = seconds

    def getTriggerTimeMinutes(self):
        return self.triggerTimeMinutes

    def setTriggerTimeMinutes(self, minutes):
        self.triggerTimeMinutes = minutes

    def getTriggerTimeHours(self):
        return self.triggerTimeHours

    def setTriggerTimeHours(self, hours):
        self.triggerTimeHours = hours

    def getTriggerTimeDays(self):
        return self.triggerTimeDays

    def setTriggerTimeDays(self, days):
        self.triggerTimeDays = days

    def getTriggerTimeMonths(self):
        return self.triggerTimeMonths

    def setTriggerTimeMonths(self, months):
        self.triggerTimeMonths = months

    def getTriggerTimeYears(self):
        return self.triggerTimeYears

    def setTriggerTimeYears(self, years):
        self.triggerTimeYears = years

    def getTriggerTimeUnused(self):
        return self.triggerTimeUnused

    def setTriggerTimeUnused(self, unused):
        self.triggerTimeUnused = unused

    def getAcquisitionDuration(self):
        return self.acquisitionDuration

    def setAcquisitionDuration(self, duration):
        self.acquisitionDuration = duration

    def getRecordType(self):
        return self.recordType

    def setRecordType(self, recordType):
        self.recordType = recordType

    def getProcessingDone(self):
        return self.processingDone

    def setProcessingDone(self, processing):
        self.processingDone = processing

    def getReserved5Entry(self):
        return self.reserved5Entry

    def setReserved5Entry(self, entry):
        self.reserved5Entry = entry

    def getRISSweeps(self):
        return self.risSweeps

    def setRISSweeps(self, sweeps):
        self.risSweeps = sweeps

    def getTimebase(self):
        return self.timebase

    def setTimebase(self, timebase):
        self.timebase = timebase

    def getVerticalCoupling(self):
        return self.verticalCoupling

    def setVerticalCoupling(self, coupling):
        self.VerticalCoupling = coupling

    def getProbeAttenuation(self):
        return self.probeAttenuation

    def setProbeAttenuation(self, attenuation):
        self.probeAttenuation = attenuation

    def getFixedVerticalGain(self):
        return self.fixedVerticalGain

    def setFixedVerticalGain(self, gain):
        self.fixedVerticalGain = gain

    def getBandwidthLimit(self):
        return self.bandwidthLimit

    def setBandwidthLimit(self, limit):
        self.bandwidthLimit = limit

    def getVerticalVernier(self):
        return self.verticalVernier

    def setVerticalVernier(self, vernier):
        self.verticalVernier = vernier

    def getAcquisitionVerticalOffset(self):
        return self.acquisitionVerticalOffset

    def setAcquisitionVerticalOffset(self, offset):
        self.acquisitionVerticalOffset = offset

    def getWaveSource(self):
        return self.waveSource

    def setWaveSource(self, source):
        self.waveSource = source


class LecroyWaveform(BaseWaveform):
    def __init__(self):
        super().__init__()
        self.waveformDescriptor = LecroyWaveformDescriptor()

    def getWaveformDescriptor(self):
        return self.waveformDescriptor


if __name__ == "__main__":
    waveform = LecroyWaveform()
    waveform.getWaveformDescriptor().dump()
