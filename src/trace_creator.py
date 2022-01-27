#!/usr/bin/python3

import numpy as np
from scipy import signal
from scipy.io import loadmat

import holoviews as hv
from bokeh.plotting import  show
from bokeh.io import output_notebook, reset_output

from src.waveform_parser.lecroy_waveform_parser import LecroyWaveformBinaryParser

from src.trace_container import TraceContainer
import configparser


class TraceImporter:
    def __init__(self, testcase="langer_probes_short", averaged_measurements=10, number_of_aes=None, print_info=False, do_plots=False, index=0, use_lowpass=False):
        self.trace_container = TraceContainer()
        base_path_traces = "traces/"
        #base_path_traces = ""
        if testcase == "mbed_tls_secure_boot_resampled":
            basepath = base_path_traces + "arm-m4-48MHz/"
            filepath = "secure_boot_trace.npy"

            self.config = configparser.ConfigParser()
            self.config.read(basepath+"properties.ini",
                             encoding='unicode_escape')
            #read meaningful values!
            self.trace_container.import_from_config(self.config, filepath)
            self.trace_container.trace = np.load(basepath+filepath)
            self.trace_container.trace_raw = np.load(basepath+filepath)

        if testcase == "beaglebone_openssl_aes128":
            basepath = base_path_traces + "bbb_openssl/"
            filepath = "full_32.bin"

            my_parse = LecroyWaveformBinaryParser(basepath+filepath)
            print(len(my_parse.data))
            #curve = hv.Curve((range(0,len(data)),np.array(data)),label="concat_trace")
            data = np.array(my_parse.data)

            self.config = configparser.ConfigParser()
            self.config.read(basepath+"properties.ini",
                             encoding='unicode_escape')
            #read meaningful values!
            self.trace_container.import_from_config(self.config, filepath)
            self.trace_container.trace = data[int(len(data)/2):]
            self.trace_container.trace_raw = data[int(len(data)/2):]

        if testcase == "stm32f4_tinyaes":
            basepath = base_path_traces + "stm32f4/"
            tracenr = index
            lowpass = use_lowpass
            filepath = None
            trigger_trace_path = None
            if not lowpass:
                filepath = "STM32F4_TinyAes_125MSPS_50M_NoLowPass_new.npy"
                trigger_trace_path = "STM32F4_TinyAes_125MSPS_50M_NoLowPass_new_trig.npy"
            else:
                filepath = "STM32F4_TinyAes_125MSPS_50M_LowPass_new.npy"
                trigger_trace_path = "STM32F4_TinyAes_125MSPS_50M_LowPass_new_trig.npy"
            self.config = configparser.ConfigParser()
            self.config.read(basepath+"properties.ini",
                             encoding='unicode_escape')
            #read meaningful values!
            self.trace_container.import_from_config(self.config, filepath)
            self.trace_container.trace = np.load(basepath+filepath)
            self.trace_container.trace_raw = np.load(basepath+filepath)
            self.trace_container.trigger_trace = np.load(
                basepath+trigger_trace_path)
            self.trace_container.trigger_trace_raw = np.load(
                basepath+trigger_trace_path)
            #Resampling due to floating point reasons:
            f_s_new = 120000000
            self.trace_container.resample(f_s_new=f_s_new)
        if testcase == "stm32f4_HWAES":
            basepath = base_path_traces + "stm32f4/"
            tracenr = index
            lowpass = use_lowpass
            filepath = None
            trigger_trace_path = None
            if not lowpass:
                filepath = "STM32F4_HWAES_500MSPS_50M_NoLowPass.npy"
                trigger_trace_path = "STM32F4_HWAES_500MSPS_50M_NoLowPass_trig.npy"
            else:
                filepath = "STM32F4_HWAES_500MSPS_50M_LowPass.npy"
                trigger_trace_path = "STM32F4_HWAES_500MSPS_50M_LowPass_trig.npy"
            self.config = configparser.ConfigParser()
            self.config.read(basepath+"properties.ini",
                             encoding='unicode_escape')
            #read meaningful values!
            self.trace_container.import_from_config(self.config, filepath)
            self.trace_container.trace = np.load(basepath+filepath)
            self.trace_container.trace_raw = np.load(basepath+filepath)
            self.trace_container.trigger_trace = np.load(
                basepath+trigger_trace_path)
            self.trace_container.trigger_trace_raw = np.load(
                basepath+trigger_trace_path)
            #Resampling due to floating point reasons:
            f_s_new = 480000000
            self.trace_container.resample(f_s_new=f_s_new)

        if testcase == "arm-m4" or testcase == "mbed_tls_AES":
            basepath = base_path_traces + "arm-m4-48MHz/"
            filepath = "np_power.npy"
            trigger_trace_path = "np_trigger.npy"

            self.config = configparser.ConfigParser()
            self.config.read(basepath+"properties.ini",
                             encoding='unicode_escape')
            #read meaningful values!
            self.trace_container.import_from_config(self.config, filepath)
            self.trace_container.trace = np.load(basepath+filepath)
            self.trace_container.trace_raw = np.load(basepath+filepath)
            self.trace_container.trigger_trace = np.load(
                basepath+trigger_trace_path)
            self.trace_container.trigger_trace_raw = np.load(
                basepath+trigger_trace_path)
            #Resampling due to floating point reasons:
            f_s_new = 1200000000
            self.trace_container.resample(f_s_new=f_s_new)

        if testcase == "sha256_internal_clock":
            basepath = base_path_traces + "sha/"
            filepath = "sha256_power.npy"
            trigger_trace_path = "sha256_trigger.npy"

            self.config = configparser.ConfigParser()
            self.config.read(basepath+"properties.ini",
                             encoding='unicode_escape')
            #read meaningful values!
            self.trace_container.import_from_config(self.config, filepath)
            self.trace_container.trace = np.load(basepath+filepath)
            self.trace_container.trace_raw = np.load(basepath+filepath)
            self.trace_container.trigger_trace = np.load(
                basepath+trigger_trace_path)
            self.trace_container.trigger_trace_raw = np.load(
                basepath+trigger_trace_path)
            #Resampling due to floating point reasons:
            f_s_new = 1200000000
            self.trace_container.resample(f_s_new=f_s_new)

        if testcase == "sha256_48":
            basepath = base_path_traces + "sha/"
            filepath = "sha256_48_power.npy"
            trigger_trace_path = "sha256_48_trigger.npy"

            self.config = configparser.ConfigParser()
            self.config.read(basepath+"properties.ini",
                             encoding='unicode_escape')
            #read meaningful values!
            self.trace_container.import_from_config(self.config, filepath)
            self.trace_container.trace = np.load(basepath+filepath)
            self.trace_container.trace_raw = np.load(basepath+filepath)
            self.trace_container.trigger_trace = np.load(
                basepath+trigger_trace_path)
            self.trace_container.trigger_trace_raw = np.load(
                basepath+trigger_trace_path)
            #Resampling due to floating point reasons:
            f_s_new = 1200000000
            self.trace_container.resample(f_s_new=f_s_new)

        if testcase == "sha256_external_clock":
            basepath = base_path_traces + "sha/"
            filepath = "sha256_stable_1G25.mat"

            self.config = configparser.ConfigParser()
            self.config.read(basepath+"properties.ini",
                             encoding='unicode_escape')
            #read meaningful values!
            self.trace_container.import_from_config(self.config, filepath)
            loaded_mat = loadmat(basepath+filepath)

            self.trace_container.trace = np.array(loaded_mat.get("power")[0])
            self.trace_container.trace_raw = np.array(
                loaded_mat.get("power")[0])
            self.trace_container.trigger_trace = np.array(
                loaded_mat.get("trigger")[0])
            self.trace_container.trigger_trace_raw = np.array(
                loaded_mat.get("trigger")[0])
            #Resampling due to floating point reasons:
            f_s_new = 1080000000
            self.trace_container.resample(f_s_new=f_s_new)

    def decimate_trace(self, decimation_factor, do_plots=False):
        self.decimation_factor = decimation_factor
        #decimate data:
        decimated_trace = signal.decimate(
            np.array(self.trace_container.trace_raw), decimation_factor)
        decimated_test_trace = signal.decimate(
            np.array(self.trace_container.trace_raw), decimation_factor)
        if do_plots:
            hv.extension('bokeh')
            reset_output()
            output_notebook()
            #curve = hv.Curve((range(0,len(data)),np.array(data)),label="concat_trace")
            curve = hv.Curve((range(0, len(decimated_trace)), np.array(
                decimated_trace)), label="concat_trace_decimated")
            curve = curve.options(xlabel='Sample', ylabel='Power')
            curve.opts(width=900, height=600)
            hv.extension('bokeh')
            #hv.save(curve,'test.svg',fmt='',backend='bokeh')
            p = hv.render(curve, backend='bokeh')
            show(p)
        self.trace_container.sampling_frequency = self.trace_container.get_fs(
            raw=True)/decimation_factor
        self.trace = decimated_trace
        self.test_trace = decimated_test_trace
        #print(self.trace_container.get_trace())
        print("Decimating signal. This can take a while.")
        if self.trace_container != None:
            self.trace_container.trace = signal.decimate(
                np.array(self.trace_container.trace_raw), decimation_factor)
            self.trace_container.sampling_frequency = self.trace_container.sampling_frequency_raw/decimation_factor
            if self.trace_container.known_start_idx_aes != None:
                self.trace_container.known_start_idx_aes = [
                    int(idx/decimation_factor) for idx in self.trace_container.known_start_idx_aes]
            self.trace_container.decimation_factor = decimation_factor
            if not(self.trace_container.trigger_trace_raw is None):
                self.trace_container.trigger_trace = signal.decimate(
                    np.array(self.trace_container.trigger_trace_raw), decimation_factor)
        print("Finished decimating.")

        #print(self.trace_container.get_trace())
