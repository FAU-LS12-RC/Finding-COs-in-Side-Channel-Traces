
#!/usr/bin/python3

import json

from bokeh.models import Span
import holoviews as hv
#from holoviews.operation import decimate
#from holoviews.operation.datashader import datashade
from bokeh.plotting import figure, show
from bokeh.io import output_notebook, reset_output, save, export_svgs, output_file
import numpy as np
from bokeh.io import curdoc
from scipy.interpolate import interp1d
from scipy import signal

class TraceContainer:
    def __init__(self):
        self.nr_hidden_cos = None 
        self.averaged_measurements = None 
        self.no_similar_rounds = None
        self.rounds_in_co_template = None
        self.trace_raw = None 
        self.trace = None 
        self.trigger_trace_raw = None
        self.trigger_trace = None
        self.decimation_factor = 1 
        self.testcase = None 
        self.sampling_frequency = None
        self.sampling_frequency_raw = None
        
        self.calculated_start_idx_aes = None
        self.calculated_device_frequency = None
        self.calculated_width = None

        self.known_start_idx_aes = None
        self.known_device_frequency = None
        self.known_width_clk_cycles = None
        self.known_width = None

        self.snr = None

        self.quality_plot = None
        self.correlation_plot = None
        
    def import_by_name(self, nr_hidden_cos, averaged_measurements, no_similar_rounds, trace_raw, trace, decimation_factor, sampling_frequency, testcase, known_start_idx_aes = None, config=None, filename=None,rounds_in_co_template = None):
        self.nr_hidden_cos = nr_hidden_cos 
        self.averaged_measurements = averaged_measurements 
        self.no_similar_rounds = no_similar_rounds
        self.trace_raw = trace_raw 
        self.trace = trace 
        self.decimation_factor = decimation_factor 
        self.testcase = testcase 
        self.sampling_frequency = sampling_frequency
        self.sampling_frequency_raw = sampling_frequency
        if known_start_idx_aes != None:
            self.known_start_idx_aes = known_start_idx_aes
        self.rounds_in_co_template = rounds_in_co_template

    def import_from_config(self, config, section, print_info = False):
        print("creating trace container from file " + str(section)+". \nImported Information:")

        self.sampling_frequency = self._check_and_get_int(config,section,'fs')
        self.sampling_frequency_raw = self.sampling_frequency
        self.known_device_frequency = self._check_and_get_int(config,section,'fd')
        self.no_similar_rounds = self._check_and_get_int(config,section,'similar_rounds')
        self.rounds_in_co_template = self._check_and_get_int(config,section,'rounds_in_co_template')
        self.nr_hidden_cos = self._check_and_get_int(config,section,'nr_hidden_cos')
        self.known_width_clk_cycles = self._check_and_get_int(config,section,'approx_width_cycles')
        self.voltage_scaling = self._check_and_get_int(config,section,'voltage_scaling')
        self.voltage_offset = self._check_and_get_int(config,section,'voltage_offset')
        self.N = self._check_and_get_int(config,section,'N')

        if config.has_option(section,"known_start_idx"):
            self.known_start_idx_aes = json.loads(config.get(section,"known_start_idx")) #TODO: TEST THIS!
        else:
            self.known_start_idx_aes=None
            print("WARNING: no start indices in properties.ini!!!!")


    def _check_and_get_int(self,config, section, item, print_info = False):
        if config.has_option(section,item):
            thing = int(config.get(section,item))
            print("\t "+ item + ": "+ str(thing))
            return thing
        else:
            if print_info:
                print(item+ " not found in config under section: "+section)
            return -1
    def print_trace_information(self):
        print("TraceContainer information:")
        print("Trace length:         " + str(len(self.get_trace())))
        print("Sampling Frequency:   " + str(self.get_fs()))
        print("Device Frequency:     " + str(self.known_device_frequency))
        print("No of similar rounds: " + str(self.no_similar_rounds))
        print("Hidden COs:        " + str(self.nr_hidden_cos))


    def get_trace(self, raw=False):
        if raw:
            return self.trace_raw
        return self.trace

    def get_trigger_trace(self, raw=False):
        if raw:
            return self.trigger_trace_raw
        return self.trigger_trace

    def get_fs(self, raw=False):
        if raw:
            return self.sampling_frequency_raw
        return self.sampling_frequency
    
    def get_no_similar_rounds(self):
        return self.no_similar_rounds

    def get_start_known_start_idx_aes(self):
        if self.known_start_idx_aes != None:
            print("WARNING: Ground truth not set yet!")
        return self.known_start_idx_aes
    def get_known_width(self, in_clk_cycles = False):
        if in_clk_cycles:
            return self.known_width_clk_cycles
        if self.known_device_frequency != None and self.known_width_clk_cycles != None:
            self.known_width = self.get_fs()/self.known_device_frequency*self.known_width_clk_cycles
            return (int)(self.known_width)
        else:
            print("ERROR: width not known but requested!")
            return -1
    def get_samples_per_clk(self, use_calculated = False):
        if use_calculated:
            self.samples_per_clk = (int)(self.get_fs()/self.calculated_device_frequency)
        else:
            self.samples_per_clk = (int)(self.get_fs()/self.known_device_frequency)
        return self.samples_per_clk

    def set_after_calc(self, calculated_start_idx_aes, calculated_width, calculated_device_frequency):
        self.calculated_device_frequency = calculated_device_frequency
        self.calculated_start_idx_aes = calculated_start_idx_aes
        self.calculated_width = calculated_width
    
    def resample(self,f_s_new,f_s_old=0):
        if f_s_old==0:
            f_s_old=self.get_fs(raw=True)
        print("Resampling trace from "+str(f_s_old)+"S/s to "+str(f_s_new)+"S/s that is an integer multiple of the device frequency ("+str(self.known_device_frequency)+"Hz) . This can take a while...")

        old_len = len(self.get_trace(raw=True))
        new_len = int(f_s_new/f_s_old*old_len)
        f_interp = interp1d(range(old_len),self.get_trace(raw=True),kind='linear',fill_value=0)
        new_sample_points = [x*(f_s_old/f_s_new) for x in range(new_len-1)]
        new_sample_points.append(self.get_trace(raw=True)[len(self.get_trace(raw=True))-1])
        new_trace = np.array(f_interp(new_sample_points))

        self.trace = new_trace
        self.trace_raw = new_trace            
        self.sampling_frequency = f_s_new
        self.sampling_frequency_raw = f_s_new
        #resampling trigger_trace:
        if self.get_trigger_trace() is not None:
            f_interp = interp1d(range(old_len),self.get_trigger_trace(),kind='linear',fill_value=0)
            new_sample_points = [x*(f_s_old/f_s_new) for x in range(new_len-1)]
            new_sample_points.append(self.get_trace()[len(self.get_trace())-1])
            new_trigger_trace = np.array(f_interp(new_sample_points))
            self.trigger_trace = new_trigger_trace
            self.trigger_trace_raw = new_trigger_trace
        
    def decimate_trace(self,decimation_factor,do_plots=False):
        self.decimation_factor = decimation_factor
        #decimate data:
        decimated_trace = signal.decimate(np.array(self.trace_raw), decimation_factor)
        decimated_test_trace = signal.decimate(np.array(self.trace_raw), decimation_factor)
        if do_plots:
            hv.extension('bokeh')
            reset_output()
            output_notebook()
            #curve = hv.Curve((range(0,len(data)),np.array(data)),label="concat_trace")
            curve = hv.Curve((range(0,len(decimated_trace)),np.array(decimated_trace)),label="concat_trace_decimated")
            curve = curve.options(xlabel='Sample', ylabel='Power')   
            curve.opts(width=900, height=600)
            hv.extension('bokeh')
            #hv.save(curve,'test.svg',fmt='',backend='bokeh')
            p =  hv.render(curve, backend='bokeh')
            show(p)
        self.sampling_frequency = self.get_fs(raw=True)/decimation_factor
        self.trace = decimated_trace
        self.test_trace = decimated_test_trace
        print("Decimating signal by a factor of " + str(decimation_factor) +". This can take a while.")
        
        self.trace = signal.decimate(np.array(self.trace_raw), decimation_factor)
        self.sampling_frequency = self.sampling_frequency_raw/decimation_factor
        if self.known_start_idx_aes !=None:
            self.known_start_idx_aes = [int(idx/decimation_factor) for idx in self.known_start_idx_aes]
        self.decimation_factor = decimation_factor
        if not(self.trigger_trace_raw is None):
            self.trigger_trace = signal.decimate(np.array(self.trigger_trace_raw), decimation_factor)
        print("Finished decimating.")     



    def plot_trace(self, show_idx = True, show_known_idx = True, decimate_for_plot_factor = 10, save_filename = None, plot_range_min = 0, plot_range_max = None,show_trigger_trace = True, max_found_idx_to_show = None,export_csv=False, title = None, x_axis_in_time=False):
        hv.extension('bokeh')
        output_notebook()
        p = figure(x_axis_label = 'Sample', y_axis_label='Amplitude',plot_width=600, plot_height=300, title=None)
        #curve = hv.Curve((range(0,len(data)),np.array(data)),label="concat_trace")
        if plot_range_max==None:
            plot_range_max = len(self.get_trace())
        
        trace_to_plot = np.array(self.get_trace())[plot_range_min:plot_range_max]
        if decimate_for_plot_factor == 1: 
            if not x_axis_in_time:
                x_data = range(0,len(trace_to_plot))
            else:
                x_data = np.arange(0,len(trace_to_plot)/self.get_fs(),step=1/self.get_fs(),dtype=float)
                p.xaxis.axis_label = "Time [s]"
            p.line(x=x_data, y=trace_to_plot, line_width=0.5)#, legend_label="Power Trace")
            if show_trigger_trace==True and self.trigger_trace is not None:
                trigger_trace_to_plot = np.array(self.get_trigger_trace())[plot_range_min:plot_range_max]
                p.line(x=x_data, y=trigger_trace_to_plot, line_width=0.5, line_color='green', legend_label="Triggertrace")
            if show_idx==True and self.calculated_start_idx_aes is not None:
                for idx in self.calculated_start_idx_aes[:max_found_idx_to_show]:
                    vline = Span(location=idx-plot_range_min, dimension='height', line_color='red',line_dash='dotted', line_width=0.5)
                    p.add_layout(vline)
            if show_known_idx==True and self.known_start_idx_aes is not None:
                for idx in self.known_start_idx_aes[:max_found_idx_to_show]:
                    vline = Span(location=idx-plot_range_min, dimension='height', line_color='green',line_dash='dotted', line_width=0.5)
                    p.add_layout(vline)
            #hv.save(curve,'test.svg',fmt='',backend='bokeh')
        else:
            decimated_trace = signal.decimate(trace_to_plot, decimate_for_plot_factor)
            if not x_axis_in_time:
                x_data = range(0,len(decimated_trace))
            else:
                x_data = np.arange(0,len(decimated_trace)/self.get_fs(),step=1/self.get_fs(),dtype=float)
                p.xaxis.axis_label = "Time [s]"
            p.line(x=x_data, y=np.array(decimated_trace), line_width=0.5)#, legend_label="Power Trace")
            if show_trigger_trace==True and self.trigger_trace is not None:
                trigger_trace_to_plot = np.array(self.get_trigger_trace())[plot_range_min:plot_range_max]
                decimated_trigger_trace = signal.decimate(trigger_trace_to_plot, decimate_for_plot_factor)
                p.line(x=x_data, y=np.array(decimated_trigger_trace), line_width=0.5, line_color='green', legend_label="Triggertrace")
            if show_idx==True and self.calculated_start_idx_aes is not None:
                decimated_idx_aes = [idx/decimate_for_plot_factor for idx in self.calculated_start_idx_aes[:max_found_idx_to_show]]
                for idx in decimated_idx_aes:
                    vline = Span(location=idx-int(plot_range_min/decimate_for_plot_factor), dimension='height', line_color='red', line_dash='dotted', line_width=0.5)
                    p.add_layout(vline)
            if show_known_idx==True and self.known_start_idx_aes is not None:
                decimated_idx_aes = [idx/decimate_for_plot_factor for idx in self.known_start_idx_aes[:max_found_idx_to_show]]
                for idx in decimated_idx_aes:
                    vline = Span(location=idx-int(plot_range_min/decimate_for_plot_factor), dimension='height', line_color='green', line_dash='dotted', line_width=0.5)
                    p.add_layout(vline)

        curdoc().add_root(p)

        show(p)
        if save_filename!= None:
            output_file(save_filename, mode='inline')
            save(p)

    def get_idx_from_trigger_trace(self,threshold=20,trigger_raise_delay=50,raw=False):
        if raw:
            trigger_trace = self.trigger_trace_raw
        else:
            trigger_trace = self.trigger_trace
        known_start_idx = []

        for i in range(len(trigger_trace)-1):
            if trigger_trace[i+1]-trigger_trace[i]>threshold:
                #trigger on!
                for x in range(i+1,i+trigger_raise_delay):
                    trigger_trace[x]=trigger_trace[i+trigger_raise_delay]
                known_start_idx.append(i)
        
        print("Found " + str(len(known_start_idx)) + " start idx: \n" + str(known_start_idx))
        self.known_start_idx_aes = known_start_idx
        return known_start_idx



    def eval_calc_vs_known(self):
        
        print("Known indices -----------------------------------------------------------")
        sorted_old = np.sort(self.known_start_idx_aes)
        print(sorted_old)
        no_off = sorted_old-sorted_old[0]
        distance_old = np.array([((sorted_old[i+1]-sorted_old[i])/self.get_known_width()) for i in range(len(sorted_old)-1)])
        print(distance_old)


        print("CALCULATED INDICES -----------------------------------------------------------")
        sorted_new = np.sort(self.calculated_start_idx_aes)
        print(sorted_new)
        no_off = sorted_new-sorted_new[0]
        distance = np.array([((sorted_new[i+1]-sorted_new[i])/self.get_known_width()) for i in range(len(sorted_new)-1)])
        print(distance)

        self.difference_calc_vs_known = int(distance_old-distance)
        print("COMPARED DISTANCES: -----------------------------------------------------------")
        print(self.difference_calc_vs_known)

    def eval_calc_vs_refined(self,refined, do_plots=False):
        self.eval_calc_vs_known()
        print("Known indices -----------------------------------------------------------")
        sorted_old = np.sort(self.known_start_idx_aes)
        print(sorted_old)
        no_off = sorted_old-sorted_old[0]
        distance_old = np.array([int((sorted_old[i+1]-sorted_old[i])/self.get_known_width()) for i in range(len(sorted_old)-1)])
        print(distance_old)


        print("REFINED INDICES -----------------------------------------------------------")
        sorted_new = np.sort(refined)
        print(sorted_new)
        no_off = sorted_new-sorted_new[0]
        distance = np.array([int((sorted_new[i+1]-sorted_new[i])/self.get_known_width()) for i in range(len(sorted_new)-1)])
        print(distance)
        self.difference_refined_vs_known =  int(distance_old-distance)
        
        print("Distance Calculated vs Known: -----------------------------------------------------------")
        print(self.difference_refined_vs_known)

        


