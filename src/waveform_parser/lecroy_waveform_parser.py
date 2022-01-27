#!/usr/bin/python3

import argparse
import struct

from src.waveform_parser.lecroy_waveform import LecroyWaveform, LecroyWaveformDescriptor


class LecroyWaveformDescriptorParser:

    def defineDescriptorOffsets(self):
        """         Descriptor Member Offsets           """
        self.DESCRIPTOR_NAME_OFFSET = 0
        self.TEMPLATE_NAME_OFFSET = 16
        self.COMM_TYPE_OFFSET = 32
        self.COMM_ORDER_OFFSET = 34
        self.WAVEDESCRIPTOR_BLOCKLENGTH_OFFSET = 36
        self.USERTEXT_BLOCKLENGTH_OFFSET = 40
        self.RES_DESC1_BLOCKLENGTH_OFFSET = 44
        self.TRIGTIME_ARRAYLENGTH_OFFSET = 48
        self.RIS_TIME_ARRAYLENGTH_OFFSET = 52
        self.RES_ARRAY1_ARRAYLENGTH_OFFSET = 56
        self.WAVE_ARRAY1_ARRAYLENGTH_OFFSET = 60
        self.WAVE_ARRAY2_ARRAYLENGTH_OFFSET = 64
        self.RES_ARRAY2_ARRAYLENGTH_OFFSET = 68
        self.RES_ARRAY3_ARRAYLENGTH_OFFSET = 72
        self.INSTRUMENT_NAME_OFFSET = 76
        self.INSTRUMENT_NUMBER_OFFSET = 92
        self.TRACE_LABEL_OFFSET = 96
        self.RESERVED1_ENTRY_OFFSET = 112
        self.RESERVED2_ENTRY_OFFSET = 114
        self.WAVE_ARRAY_COUNT_OFFSET = 116
        self.POINTS_PER_SCREEN_OFFSET = 120
        self.FIRST_VALID_POINT_OFFSET = 124
        self.LAST_VALID_POINT_OFFSET = 128
        self.FIRST_POINT_OFFSET = 132
        self.SPARSING_FACTOR_OFFSET = 136
        self.SEGMENT_INDEX_OFFSET = 140
        self.SUARRAY_COUNT_OFFSET = 144
        self.SWEEPS_PER_ACQ_OFFSET = 148
        self.POINTS_PER_PAIR_OFFSET = 152
        self.PAIR_OFFSET_OFFSET = 154
        self.VERTICAL_GAIN_OFFSET = 156
        self.VERTICAL_OFFSET_OFFSET = 160
        self.MAX_VALUE_OFFSET = 164
        self.MIN_VALUE_OFFSET = 168
        self.NOMINAL_ITS_OFFSET = 172
        self.NOMINAL_SUARRAY_COUNT_OFFSET = 174
        self.HORIZONTAL_INTERVAL_OFFSET = 176
        self.HORIZONTAL_OFFSET_OFFSET = 180
        self.PIXEL_OFFSET_OFFSET = 188
        self.VERTICAL_UNIT_OFFSET = 196
        self.HORIZONTAL_UNIT_OFFSET = 244
        self.HORIZONTAL_UNCERTAINTY_OFFSET = 292
        self.TRIGGER_TIME_OFFSET = 296
        self.ACQUISITION_DURATION_OFFSET = 312
        self.RECORD_TYPE_OFFSET = 316
        self.PROCESSING_DONE_OFFSET = 318
        self.RESERVED5_ENTRY_OFFSET = 320
        self.RIS_SWEEPS_OFFSET = 322
        self.TIMEBASE_OFFSET = 324
        self.VERTICAL_COUPLING_OFFSET = 326
        self.PROBE_ATTENUATION_OFFSET = 328
        self.FIXED_VERTICAL_GAIN_OFFSET = 332
        self.BANDWIDTH_LIMIT_OFFSET = 334
        self.VERTICAL_VERNIER_OFFSET = 336
        self.ACQUISITION_VERTICAL_OFFSET_OFFSET = 340
        self.WAVE_SOURCE_OFFSET = 344

    def defineDescriptorLengths(self):
        """             Descriptor Member Lengths           """
        self.DESCRIPTOR_NAME_LENGTH = 16
        self.TEMPLATE_NAME_LENGTH = 16
        self.COMM_TYPE_LENGTH = 2
        self.COMM_ORDER_LENGTH = 2
        self.WAVEDESCRIPTOR_BLOCKLENGTH_LENGTH = 4
        self.USERTEXT_BLOCKLENGTH_LENGTH = 4
        self.RES_DESC1_BLOCKLENGTH_LENGTH = 4
        self.TRIGTIME_ARRAYLENGTH_LENGTH = 4
        self.RIS_TIME_ARRAYLENGTH_LENGTH = 4
        self.RES_ARRAY1_ARRAYLENGTH_LENGTH = 4
        self.WAVE_ARRAY1_ARRAYLENGTH_LENGTH = 4
        self.WAVE_ARRAY2_ARRAYLENGTH_LENGTH = 4
        self.RES_ARRAY2_ARRAYLENGTH_LENGTH = 4
        self.RES_ARRAY3_ARRAYLENGTH_LENGTH = 4
        self.INSTRUMENT_NAME_LENGTH = 16
        self.INSTRUMENT_NUMBER_LENGTH = 4
        self.TRACE_LABEL_LENGTH = 4
        self.RESERVED1_ENTRY_LENGTH = 2
        self.RESERVED2_ENTRY_LENGTH = 2
        self.WAVE_ARRAY_COUNT_LENGTH = 4
        self.POINTS_PER_SCREEN_LENGTH = 4
        self.FIRST_VALID_POINT_LENGTH = 4
        self.LAST_VALID_POINT_LENGTH = 4
        self.FIRST_POINT_LENGTH = 4
        self.SPARSING_FACTOR_LENGTH = 4
        self.SEGMENT_INDEX_LENGTH = 4
        self.SUARRAY_COUNT_LENGTH = 4
        self.SWEEPS_PER_ACQ_LENGTH = 4
        self.POINTS_PER_PAIR_LENGTH = 2
        self.PAIR_OFFSET_LENGTH = 2
        self.VERTICAL_GAIN_LENGTH = 4
        self.VERTICAL_OFFSET_LENGTH = 4
        self.MAX_VALUE_LENGTH = 4
        self.MIN_VALUE_LENGTH = 4
        self.NOMINAL_ITS_LENGTH = 2
        self.NOMINAL_SUARRAY_COUNT_LENGTH = 2
        self.HORIZONTAL_INTERVAL_LENGTH = 4
        self.HORIZONTAL_OFFSET_LENGTH = 8
        self.PIXEL_OFFSET_LENGTH = 8
        self.VERTICAL_UNIT_LENGTH = 48
        self.HORIZONTAL_UNIT_LENGTH = 48
        self.HORIZONTAL_UNCERTAINTY_LENGTH = 4
        self.TRIGGER_TIME_LENGTH = 16
        self.ACQUISITION_DURATION_LENGTH = 4
        self.RECORD_TYPE_LENGTH = 2
        self.PROCESSING_DONE_LENGTH = 2
        self.RESERVED5_ENTRY_LENGTH = 2
        self.RIS_SWEEPS_LENGTH = 2
        self.TIMEBASE_LENGTH = 2
        self.VERTICAL_COUPLING_LENGTH = 2
        self.PROBE_ATTENUATION_LENGTH = 4
        self.FIXED_VERTICAL_GAIN_LENGTH = 2
        self.BANDWIDTH_LIMIT_LENGTH = 2
        self.VERTICAL_VERNIER_LENGTH = 4
        self.ACQUISITION_VERTICAL_OFFSET_LENGTH = 4
        self.WAVE_SOURCE_LENGTH = 2

    def __init__(self, unprocessedDescriptor, waveformDescriptor):
        self.unprocessedDescriptor = unprocessedDescriptor
        self.waveformDescriptor = waveformDescriptor

        self.defineDescriptorOffsets()
        self.defineDescriptorLengths()

        self.parseDescriptorName()
        self.parseTemplateName()

        self.parseCommType()
        self.parseCommOrder()

        self.parseWaveformDescriptorBlockLength()
        self.parseUserTextBlockLength()
        self.parseReservedDescriptor1BlockLength()

        self.parseTrigTimeArrayLength()
        self.parseRISTimeArrayLength()
        self.parseReservedArray1Length()
        self.parseWaveArray1Length()
        self.parseWaveArray2Length()
        self.parseReservedArray2Length()
        self.parseReservedArray3Length()

        self.parseInstrumentName()
        self.parseInstrumentNumber()
        self.parseTraceLabel()
        self.parseReservedEntry1()
        self.parseReservedEntry2()

        self.parseWaveArrayCount()
        self.parsePointsPerScreen()
        self.parseFirstValidPoint()
        self.parseLastValidPoint()
        self.parseFirstPoint()
        self.parseSparsingFactor()
        self.parseSegmentIndex()
        self.parseSUArrayCount()
        self.parseSweepsPerAcquisition()
        self.parsePointsPerPair()
        self.parsePairOffset()
        self.parseVerticalGain()
        self.parseVerticalOffset()
        self.parseMaximumValue()
        self.parseMinimumValue()
        self.parseNominalITS()
        self.parseNominalSUArrayCount()
        self.parseHorizontalInterval()
        self.parseHorizontalOffset()
        self.parsePixelOffset()
        self.parseVerticalUnit()
        self.parseHorizontalUnit()
        self.parseHorizontalUncertainty()

        self.parseTriggerTime()
        self.parseAcquisitionDuration()
        self.parseRecordType()
        self.parseProcessingDone()
        self.parseReserved5Entry()
        self.parseRISSweeps()
        self.parseTimebase()
        self.parseVerticalCoupling()
        self.parseProbeAttenuation()
        self.parseFixedVerticalGain()
        self.parseBandwidthLimit()
        self.parseVerticalVernier()
        self.parseAcquisitionVerticalOffset()
        self.parseWaveSource()

    def parseDescriptorName(self):
        descriptorName = self.unprocessedDescriptor[self.DESCRIPTOR_NAME_OFFSET:
                                                    self.DESCRIPTOR_NAME_OFFSET + self.DESCRIPTOR_NAME_LENGTH].decode("utf-8")
        self.waveformDescriptor.setDescriptorName(descriptorName)

    def parseTemplateName(self):
        templateName = self.unprocessedDescriptor[self.TEMPLATE_NAME_OFFSET:
                                                  self.TEMPLATE_NAME_OFFSET + self.TEMPLATE_NAME_LENGTH].decode("utf-8")
        self.waveformDescriptor.setTemplateName(templateName)

    def parseCommType(self):
        commType = int.from_bytes(
            self.unprocessedDescriptor[self.COMM_TYPE_OFFSET:self.COMM_TYPE_OFFSET + self.COMM_TYPE_LENGTH], "little")
        self.waveformDescriptor.setCommType(
            LecroyWaveformDescriptor.CommType(commType))

    def parseCommOrder(self):
        commOrder = int.from_bytes(
            self.unprocessedDescriptor[self.COMM_ORDER_OFFSET:self.COMM_ORDER_OFFSET + self.COMM_ORDER_LENGTH], "little")
        self.waveformDescriptor.setCommOrder(
            LecroyWaveformDescriptor.CommOrder(commOrder))

    def parseWaveformDescriptorBlockLength(self):
        blockLength = int.from_bytes(
            self.unprocessedDescriptor[self.WAVEDESCRIPTOR_BLOCKLENGTH_OFFSET:self.WAVEDESCRIPTOR_BLOCKLENGTH_OFFSET + self.WAVEDESCRIPTOR_BLOCKLENGTH_LENGTH], "little")
        self.waveformDescriptor.setWaveDescriptorBlockLength(blockLength)

    def parseUserTextBlockLength(self):
        blockLength = int.from_bytes(
            self.unprocessedDescriptor[self.USERTEXT_BLOCKLENGTH_OFFSET:self.USERTEXT_BLOCKLENGTH_OFFSET + self.USERTEXT_BLOCKLENGTH_LENGTH], "little")
        self.waveformDescriptor.setUserTextBlockLength(blockLength)

    def parseReservedDescriptor1BlockLength(self):
        blockLength = int.from_bytes(
            self.unprocessedDescriptor[self.RES_DESC1_BLOCKLENGTH_OFFSET:self.RES_DESC1_BLOCKLENGTH_OFFSET + self.RES_DESC1_BLOCKLENGTH_LENGTH], "little")
        self.waveformDescriptor.setReservedDescriptor1BlockLength(blockLength)

    def parseTrigTimeArrayLength(self):
        arrayLength = int.from_bytes(
            self.unprocessedDescriptor[self.TRIGTIME_ARRAYLENGTH_OFFSET:self.TRIGTIME_ARRAYLENGTH_OFFSET + self.TRIGTIME_ARRAYLENGTH_LENGTH], "little")
        self.waveformDescriptor.setTrigTimeArrayLength(arrayLength)

    def parseRISTimeArrayLength(self):
        arrayLength = int.from_bytes(
            self.unprocessedDescriptor[self.RIS_TIME_ARRAYLENGTH_OFFSET:self.RIS_TIME_ARRAYLENGTH_OFFSET + self.RIS_TIME_ARRAYLENGTH_LENGTH], "little")
        self.waveformDescriptor.setRISTimeArrayLength(arrayLength)

    def parseReservedArray1Length(self):
        arrayLength = int.from_bytes(
            self.unprocessedDescriptor[self.RES_ARRAY1_ARRAYLENGTH_OFFSET:self.RES_ARRAY1_ARRAYLENGTH_OFFSET + self.RES_ARRAY1_ARRAYLENGTH_LENGTH], "little")
        self.waveformDescriptor.setReservedArray1Length(arrayLength)

    def parseWaveArray1Length(self):
        arrayLength = int.from_bytes(
            self.unprocessedDescriptor[self.WAVE_ARRAY1_ARRAYLENGTH_OFFSET:self.WAVE_ARRAY1_ARRAYLENGTH_OFFSET + self.WAVE_ARRAY1_ARRAYLENGTH_LENGTH], "little")
        self.waveformDescriptor.setWaveArray1Length(arrayLength)

    def parseWaveArray2Length(self):
        arrayLength = int.from_bytes(
            self.unprocessedDescriptor[self.WAVE_ARRAY2_ARRAYLENGTH_OFFSET:self.WAVE_ARRAY2_ARRAYLENGTH_OFFSET + self.WAVE_ARRAY2_ARRAYLENGTH_LENGTH], "little")
        self.waveformDescriptor.setWaveArray2Length(arrayLength)

    def parseReservedArray2Length(self):
        arrayLength = int.from_bytes(
            self.unprocessedDescriptor[self.RES_ARRAY2_ARRAYLENGTH_OFFSET:self.RES_ARRAY2_ARRAYLENGTH_OFFSET + self.RES_ARRAY2_ARRAYLENGTH_LENGTH], "little")
        self.waveformDescriptor.setReservedArray2Length(arrayLength)

    def parseReservedArray3Length(self):
        arrayLength = int.from_bytes(
            self.unprocessedDescriptor[self.RES_ARRAY3_ARRAYLENGTH_OFFSET:self.RES_ARRAY3_ARRAYLENGTH_OFFSET + self.RES_ARRAY3_ARRAYLENGTH_LENGTH], "little")
        self.waveformDescriptor.setReservedArray3Length(arrayLength)

    def parseInstrumentName(self):
        instrumentName = self.unprocessedDescriptor[self.INSTRUMENT_NAME_OFFSET:
                                                    self.INSTRUMENT_NAME_OFFSET + self.INSTRUMENT_NAME_LENGTH].decode("utf-8")
        self.waveformDescriptor.setInstrumentName(instrumentName)

    def parseInstrumentNumber(self):
        instrumentNumber = int.from_bytes(
            self.unprocessedDescriptor[self.INSTRUMENT_NUMBER_OFFSET:self.INSTRUMENT_NUMBER_OFFSET + self.INSTRUMENT_NUMBER_LENGTH], "little")
        self.waveformDescriptor.setInstrumentNumber(instrumentNumber)

    def parseTraceLabel(self):
        traceLabel = self.unprocessedDescriptor[self.TRACE_LABEL_OFFSET:
                                                self.TRACE_LABEL_OFFSET + self.TRACE_LABEL_LENGTH].decode("utf-8")
        self.waveformDescriptor.setTraceLabel(traceLabel)

    def parseReservedEntry1(self):
        reservedEntry = int.from_bytes(
            self.unprocessedDescriptor[self.RESERVED1_ENTRY_OFFSET:self.RESERVED1_ENTRY_OFFSET + self.RESERVED1_ENTRY_LENGTH], "little")
        self.waveformDescriptor.setReservedEntry1(reservedEntry)

    def parseReservedEntry2(self):
        reservedEntry = int.from_bytes(
            self.unprocessedDescriptor[self.RESERVED2_ENTRY_OFFSET:self.RESERVED2_ENTRY_OFFSET + self.RESERVED2_ENTRY_LENGTH], "little")
        self.waveformDescriptor.setReservedEntry2(reservedEntry)

    def parseWaveArrayCount(self):
        arrayCount = int.from_bytes(
            self.unprocessedDescriptor[self.WAVE_ARRAY_COUNT_OFFSET:self.WAVE_ARRAY_COUNT_OFFSET + self.WAVE_ARRAY_COUNT_LENGTH], "little")
        self.waveformDescriptor.setWaveArrayCount(arrayCount)

    def parsePointsPerScreen(self):
        pntsPerScreen = int.from_bytes(
            self.unprocessedDescriptor[self.POINTS_PER_SCREEN_OFFSET:self.POINTS_PER_SCREEN_OFFSET + self.POINTS_PER_SCREEN_LENGTH], "little")
        self.waveformDescriptor.setPointsPerScreen(pntsPerScreen)

    def parseFirstValidPoint(self):
        validPoint = int.from_bytes(
            self.unprocessedDescriptor[self.FIRST_VALID_POINT_OFFSET:self.FIRST_VALID_POINT_OFFSET + self.FIRST_VALID_POINT_LENGTH], "little")
        self.waveformDescriptor.setFirstValidPoint(validPoint)

    def parseLastValidPoint(self):
        validPoint = int.from_bytes(
            self.unprocessedDescriptor[self.LAST_VALID_POINT_OFFSET:self.LAST_VALID_POINT_OFFSET + self.LAST_VALID_POINT_LENGTH], "little")
        self.waveformDescriptor.setLastValidPoint(validPoint)

    def parseFirstPoint(self):
        point = int.from_bytes(
            self.unprocessedDescriptor[self.FIRST_POINT_OFFSET:self.FIRST_POINT_OFFSET + self.FIRST_POINT_LENGTH], "little")
        self.waveformDescriptor.setFirstPoint(point)

    def parseSparsingFactor(self):
        sparsingFactor = int.from_bytes(
            self.unprocessedDescriptor[self.SPARSING_FACTOR_OFFSET:self.SPARSING_FACTOR_OFFSET + self.SPARSING_FACTOR_LENGTH], "little")
        self.waveformDescriptor.setSparsingFactor(sparsingFactor)

    def parseSegmentIndex(self):
        segmentIndex = int.from_bytes(
            self.unprocessedDescriptor[self.SEGMENT_INDEX_OFFSET:self.SEGMENT_INDEX_OFFSET + self.SEGMENT_INDEX_LENGTH], "little")
        self.waveformDescriptor.setSegmentIndex(segmentIndex)

    def parseSUArrayCount(self):
        count = int.from_bytes(
            self.unprocessedDescriptor[self.SUARRAY_COUNT_OFFSET:self.SUARRAY_COUNT_OFFSET + self.SUARRAY_COUNT_LENGTH], "little")
        self.waveformDescriptor.setSUArrayCount(count)

    def parseSweepsPerAcquisition(self):
        sweeps = int.from_bytes(
            self.unprocessedDescriptor[self.SWEEPS_PER_ACQ_OFFSET:self.SWEEPS_PER_ACQ_OFFSET + self.SWEEPS_PER_ACQ_LENGTH], "little")
        self.waveformDescriptor.setSweepsPerAcquisition(sweeps)

    def parsePointsPerPair(self):
        points = int.from_bytes(
            self.unprocessedDescriptor[self.POINTS_PER_PAIR_OFFSET:self.POINTS_PER_PAIR_OFFSET + self.POINTS_PER_PAIR_LENGTH], "little")
        self.waveformDescriptor.setPointsPerPair(points)

    def parsePairOffset(self):
        offset = int.from_bytes(
            self.unprocessedDescriptor[self.PAIR_OFFSET_OFFSET:self.PAIR_OFFSET_OFFSET + self.PAIR_OFFSET_LENGTH], "little")
        self.waveformDescriptor.setPairOffset(offset)

    def parseVerticalGain(self):
        gain = struct.unpack(
            '<f', self.unprocessedDescriptor[self.VERTICAL_GAIN_OFFSET:self.VERTICAL_GAIN_OFFSET + self.VERTICAL_GAIN_LENGTH])[0]
        self.waveformDescriptor.setVerticalGain(gain)

    def parseVerticalOffset(self):
        offset = struct.unpack(
            '<f', self.unprocessedDescriptor[self.VERTICAL_OFFSET_OFFSET:self.VERTICAL_OFFSET_OFFSET + self.VERTICAL_OFFSET_LENGTH])[0]
        self.waveformDescriptor.setVerticalOffset(offset)

    def parseMaximumValue(self):
        maximum = struct.unpack(
            '<f', self.unprocessedDescriptor[self.MAX_VALUE_OFFSET:self.MAX_VALUE_OFFSET + self.MAX_VALUE_LENGTH])[0]
        self.waveformDescriptor.setMaximumValue(maximum)

    def parseMinimumValue(self):
        minimum = struct.unpack(
            '<f', self.unprocessedDescriptor[self.MIN_VALUE_OFFSET:self.MIN_VALUE_OFFSET + self.MIN_VALUE_LENGTH])[0]
        self.waveformDescriptor.setMinimumValue(minimum)

    def parseNominalITS(self):
        nominalITS = int.from_bytes(
            self.unprocessedDescriptor[self.NOMINAL_ITS_OFFSET:self.NOMINAL_ITS_OFFSET + self.NOMINAL_ITS_LENGTH], "little")
        self.waveformDescriptor.setNominalITS(nominalITS)

    def parseNominalSUArrayCount(self):
        nominalCount = int.from_bytes(
            self.unprocessedDescriptor[self.NOMINAL_SUARRAY_COUNT_OFFSET:self.NOMINAL_SUARRAY_COUNT_OFFSET + self.NOMINAL_SUARRAY_COUNT_LENGTH], "little")
        self.waveformDescriptor.setNominalSUArrayCount(nominalCount)

    def parseHorizontalInterval(self):
        interval = struct.unpack(
            '<f', self.unprocessedDescriptor[self.HORIZONTAL_INTERVAL_OFFSET:self.HORIZONTAL_INTERVAL_OFFSET + self.HORIZONTAL_INTERVAL_LENGTH])[0]
        self.waveformDescriptor.setHorizontalInterval(interval)

    def parseHorizontalOffset(self):
        offset = struct.unpack(
            '<d', self.unprocessedDescriptor[self.HORIZONTAL_OFFSET_OFFSET:self.HORIZONTAL_OFFSET_OFFSET + self.HORIZONTAL_OFFSET_LENGTH])[0]
        self.waveformDescriptor.setHorizontalOffset(offset)

    def parsePixelOffset(self):
        offset = struct.unpack(
            '<d', self.unprocessedDescriptor[self.PIXEL_OFFSET_OFFSET:self.PIXEL_OFFSET_OFFSET + self.PIXEL_OFFSET_LENGTH])[0]
        self.waveformDescriptor.setPixelOffset(offset)

    def parseVerticalUnit(self):
        verticalUnit = self.unprocessedDescriptor[self.VERTICAL_UNIT_OFFSET:
                                                  self.VERTICAL_UNIT_OFFSET + self.VERTICAL_UNIT_LENGTH].decode("utf-8")
        self.waveformDescriptor.setVerticalUnit(verticalUnit)

    def parseHorizontalUnit(self):
        horizontalUnit = self.unprocessedDescriptor[self.HORIZONTAL_UNIT_OFFSET:
                                                    self.HORIZONTAL_UNIT_OFFSET + self.HORIZONTAL_UNIT_LENGTH].decode("utf-8")
        self.waveformDescriptor.setHorizontalUnit(horizontalUnit)

    def parseHorizontalUncertainty(self):
        uncertainty = struct.unpack(
            '<f', self.unprocessedDescriptor[self.HORIZONTAL_UNCERTAINTY_OFFSET:self.HORIZONTAL_UNCERTAINTY_OFFSET + self.HORIZONTAL_UNCERTAINTY_LENGTH])[0]
        self.waveformDescriptor.setHorizontalUncertainty(uncertainty)

    def parseTriggerTime(self):
        TRIGGER_TIME_SECONDS_OFFSET = 0
        TRIGGER_TIME_SECONDS_LENGTH = 8
        TRIGGER_TIME_MINUTES_OFFSET = 8
        TRIGGER_TIME_MINUTES_LENGTH = 1
        TRIGGER_TIME_HOURS_OFFSET = 9
        TRIGGER_TIME_HOURS_LENGTH = 1
        TRIGGER_TIME_DAYS_OFFSET = 10
        TRIGGER_TIME_DAYS_LENGTH = 1
        TRIGGER_TIME_MONTHS_OFFSET = 11
        TRIGGER_TIME_MONTHS_LENGTH = 1
        TRIGGER_TIME_YEARS_OFFSET = 12
        TRIGGER_TIME_YEARS_LENGTH = 2
        TRIGGER_TIME_UNUSED_OFFSET = 14
        TRIGGER_TIME_UNUSED_LENGTH = 2

        triggerTime = self.unprocessedDescriptor[self.TRIGGER_TIME_OFFSET:
                                                 self.TRIGGER_TIME_OFFSET + self.TRIGGER_TIME_LENGTH]
        seconds = struct.unpack(
            '<d', triggerTime[TRIGGER_TIME_SECONDS_OFFSET:TRIGGER_TIME_SECONDS_OFFSET + TRIGGER_TIME_SECONDS_LENGTH])[0]
        minutes = int.from_bytes(
            triggerTime[TRIGGER_TIME_MINUTES_OFFSET:TRIGGER_TIME_MINUTES_OFFSET + TRIGGER_TIME_MINUTES_LENGTH], "little")
        hours = int.from_bytes(
            triggerTime[TRIGGER_TIME_HOURS_OFFSET:TRIGGER_TIME_HOURS_OFFSET + TRIGGER_TIME_HOURS_LENGTH], "little")
        days = int.from_bytes(
            triggerTime[TRIGGER_TIME_DAYS_OFFSET:TRIGGER_TIME_DAYS_OFFSET + TRIGGER_TIME_DAYS_LENGTH], "little")
        months = int.from_bytes(
            triggerTime[TRIGGER_TIME_MONTHS_OFFSET:TRIGGER_TIME_MONTHS_OFFSET + TRIGGER_TIME_MONTHS_LENGTH], "little")
        years = int.from_bytes(
            triggerTime[TRIGGER_TIME_YEARS_OFFSET:TRIGGER_TIME_YEARS_OFFSET + TRIGGER_TIME_YEARS_LENGTH], "little")
        unused = int.from_bytes(
            triggerTime[TRIGGER_TIME_UNUSED_OFFSET:TRIGGER_TIME_UNUSED_OFFSET + TRIGGER_TIME_UNUSED_LENGTH], "little")

        self.waveformDescriptor.setTriggerTimeSeconds(seconds)
        self.waveformDescriptor.setTriggerTimeMinutes(minutes)
        self.waveformDescriptor.setTriggerTimeHours(hours)
        self.waveformDescriptor.setTriggerTimeDays(days)
        self.waveformDescriptor.setTriggerTimeMonths(months)
        self.waveformDescriptor.setTriggerTimeYears(years)
        self.waveformDescriptor.setTriggerTimeUnused(unused)

    def parseAcquisitionDuration(self):
        duration = struct.unpack(
            '<f', self.unprocessedDescriptor[self.ACQUISITION_DURATION_OFFSET:self.ACQUISITION_DURATION_OFFSET + self.ACQUISITION_DURATION_LENGTH])[0]
        self.waveformDescriptor.setAcquisitionDuration(duration)

    def parseRecordType(self):
        recordType = int.from_bytes(
            self.unprocessedDescriptor[self.RECORD_TYPE_OFFSET:self.RECORD_TYPE_OFFSET + self.RECORD_TYPE_LENGTH], "little")
        self.waveformDescriptor.setRecordType(
            LecroyWaveformDescriptor.RecordType(recordType))

    def parseProcessingDone(self):
        processingDone = int.from_bytes(
            self.unprocessedDescriptor[self.PROCESSING_DONE_OFFSET:self.PROCESSING_DONE_OFFSET + self.PROCESSING_DONE_LENGTH], "little")
        self.waveformDescriptor.setProcessingDone(
            LecroyWaveformDescriptor.ProcessingDone(processingDone))

    def parseReserved5Entry(self):
        entry = int.from_bytes(
            self.unprocessedDescriptor[self.RESERVED5_ENTRY_OFFSET:self.RESERVED5_ENTRY_OFFSET + self.RESERVED5_ENTRY_LENGTH], "little")
        self.waveformDescriptor.setReserved5Entry(entry)

    def parseRISSweeps(self):
        sweeps = int.from_bytes(
            self.unprocessedDescriptor[self.RIS_SWEEPS_OFFSET:self.RIS_SWEEPS_OFFSET + self.RIS_SWEEPS_LENGTH], "little")
        self.waveformDescriptor.setRISSweeps(sweeps)

    def parseTimebase(self):
        timebase = int.from_bytes(
            self.unprocessedDescriptor[self.TIMEBASE_OFFSET:self.TIMEBASE_OFFSET + self.TIMEBASE_LENGTH], "little")
        self.waveformDescriptor.setTimebase(
            LecroyWaveformDescriptor.Timebase(timebase))

    def parseVerticalCoupling(self):
        coupling = int.from_bytes(
            self.unprocessedDescriptor[self.VERTICAL_COUPLING_OFFSET:self.VERTICAL_COUPLING_OFFSET + self.VERTICAL_COUPLING_LENGTH], "little")
        self.waveformDescriptor.setVerticalCoupling(
            LecroyWaveformDescriptor.VerticalCoupling(coupling))

    def parseProbeAttenuation(self):
        attenuation = struct.unpack(
            '<f', self.unprocessedDescriptor[self.PROBE_ATTENUATION_OFFSET:self.PROBE_ATTENUATION_OFFSET + self.PROBE_ATTENUATION_LENGTH])[0]
        self.waveformDescriptor.setProbeAttenuation(attenuation)

    def parseFixedVerticalGain(self):
        gain = int.from_bytes(
            self.unprocessedDescriptor[self.FIXED_VERTICAL_GAIN_OFFSET:self.FIXED_VERTICAL_GAIN_OFFSET + self.FIXED_VERTICAL_GAIN_LENGTH], "little")
        self.waveformDescriptor.setFixedVerticalGain(
            LecroyWaveformDescriptor.FixedVerticalGain(gain))

    def parseBandwidthLimit(self):
        bandwidthLimit = int.from_bytes(
            self.unprocessedDescriptor[self.BANDWIDTH_LIMIT_OFFSET:self.BANDWIDTH_LIMIT_OFFSET + self.BANDWIDTH_LIMIT_LENGTH], "little")
        self.waveformDescriptor.setBandwidthLimit(
            LecroyWaveformDescriptor.BandwidthLimit(bandwidthLimit))

    def parseVerticalVernier(self):
        vernier = struct.unpack(
            '<f', self.unprocessedDescriptor[self.VERTICAL_VERNIER_OFFSET:self.VERTICAL_VERNIER_OFFSET + self.VERTICAL_VERNIER_LENGTH])[0]
        self.waveformDescriptor.setVerticalVernier(vernier)

    def parseAcquisitionVerticalOffset(self):
        offset = struct.unpack(
            '<f', self.unprocessedDescriptor[self.ACQUISITION_VERTICAL_OFFSET_OFFSET:self.ACQUISITION_VERTICAL_OFFSET_OFFSET + self.ACQUISITION_VERTICAL_OFFSET_LENGTH])[0]
        self.waveformDescriptor.setAcquisitionVerticalOffset(offset)

    def parseWaveSource(self):
        source = int.from_bytes(
            self.unprocessedDescriptor[self.WAVE_SOURCE_OFFSET:self.WAVE_SOURCE_OFFSET + self.WAVE_SOURCE_LENGTH], "little")
        self.waveformDescriptor.setWaveSource(
            LecroyWaveformDescriptor.WaveSource(source))


class LecroyWaveformParser:

    def __init__(self, unprocessedData, waveform):
        self.WAVEDESCRIPTOR_OFFSET = 21
        self.WAVEDESCRIPTOR_LENGTH = 346

        self.unprocessedData = unprocessedData
        self.waveform = waveform

    def parse(self):
        self.parseWaveformDescriptor()
        self.parseWaveform()

    def parseWaveformDescriptor(self):
        LecroyWaveformDescriptorParser(
            self.unprocessedData[self.WAVEDESCRIPTOR_OFFSET:self.WAVEDESCRIPTOR_OFFSET + self.WAVEDESCRIPTOR_LENGTH], self.waveform.getWaveformDescriptor())

    def parseWaveform(self):
        waveformArrayOffset = self.WAVEDESCRIPTOR_OFFSET
        waveformArrayLength = self.waveform.getWaveformDescriptor().getWaveArray1Length()
        waveformArrayOffset += self.waveform.getWaveformDescriptor().getWaveDescriptorBlockLength()
        waveformArrayOffset += self.waveform.getWaveformDescriptor().getUserTextBlockLength()
        waveformArrayOffset += self.waveform.getWaveformDescriptor().getReservedDescriptor1BlockLength()
        waveformArrayOffset += self.waveform.getWaveformDescriptor().getTrigTimeArrayLength()
        waveformArrayOffset += self.waveform.getWaveformDescriptor().getRISTimeArrayLength()
        waveformArrayOffset += self.waveform.getWaveformDescriptor().getReservedArray1Length()

        unprocessedWaveformBytes = self.unprocessedData[
            waveformArrayOffset:waveformArrayOffset + waveformArrayLength]
        for byteIndex in range(0, waveformArrayLength, 2):
            rawData = int.from_bytes(
                unprocessedWaveformBytes[byteIndex:byteIndex + 2], "little", signed=True)
            data = self.waveform.getWaveformDescriptor().getVerticalGain(
            ) * (rawData - self.waveform.getWaveformDescriptor().getVerticalOffset())
            self.waveform.pushBackValue(data)
        self.waveform.setHorizontalUnit(
            self.waveform.getWaveformDescriptor().getHorizontalUnit())
        self.waveform.setVerticalUnit(
            self.waveform.getWaveformDescriptor().getVerticalUnit())
        self.waveform.setTimePerSample(
            self.waveform.getWaveformDescriptor().getHorizontalInterval())
        self.waveform.setTimeAtFrameStart(
            self.waveform.getWaveformDescriptor().getHorizontalOffset())


class LecroyWaveformBinaryParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.timebase = None
        self.data = None
        self.parse_bin(file_path)

    def parse_bin(self, file_path):
        self.fileHandle = open(file_path, "rb")
        bytesArray = list()
        try:
            bytesArray = self.fileHandle.read()
        except Exception:
            print("Non handled Exception!")
            raise
        waveform = LecroyWaveform()
        waveformParser = LecroyWaveformParser(bytesArray, waveform)
        waveformParser.parse()
        # waveform.getWaveformDescriptor().dump()
        self.timebase, self.data = waveform.getDataValues()

    def close_file(self):
        self.fileHandle.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="Test application to parse a PowerTracer binary file")
    parser.add_argument(
        "-b", "--binary_file",
        type=str,
        help="Path to the binary file",)
    arguments = parser.parse_args()
    if arguments.binary_file is not None:
        fileHandle = open(arguments.binary_file, "rb")
        bytesArray = list()
        try:
            bytesArray = fileHandle.read()
        except Exception:
            print("Non handled Exception!")
            raise
        waveform = LecroyWaveform()
        waveformParser = LecroyWaveformParser(bytesArray, waveform)
        waveformParser.parse()
        waveform.getWaveformDescriptor().dump()
        timebase, values = waveform.getDataValues()

        # print( timebase ) # timebase list...timestamp for every data sample
        # print( values ) # acquired data samples
    else:
        print("No Binary File input. Exit application!")
