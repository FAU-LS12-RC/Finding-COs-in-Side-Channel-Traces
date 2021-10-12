from src.helper import calc_sad
from src.trace_container import TraceContainer
from numba import jit
from time import process_time
import numpy as np
import itertools
import holoviews as hv
from bokeh.plotting import figure, show
from bokeh.palettes import Dark2_5 as palette
from bokeh.io import output_notebook, reset_output, save, export_svgs
from src.autocorrelation_accl import Autocorrelation_Accelerator
class Refiner:
    def __init__(self,trace_container):
        self.trace_container = trace_container


    def get_template_with_sad(self, plot_template_on_index=0, plot_finished_template=False,use_top_x_percent=0):
        #adjust offsets when cutting. idea:
        # 1st. try all offsets (-max_offset to +max_offset) with SAD and see what is best
        # 2nd. try offsets in this bracket (-width,+width) for minimum SAD!
        #ranking possible due to min SAD for each trace!
        accl = Autocorrelation_Accelerator()
        rounds_in_co_template = self.trace_container.rounds_in_co_template
        max_offset=rounds_in_co_template
        width = int(self.trace_container.calculated_width)
        trace = self.trace_container.get_trace()
        start_aes_list = np.array(self.trace_container.calculated_start_idx_aes)
        finished_cut_aes_traces = np.array([trace[int(start_aes_list[0]-(max_offset)*width):int(start_aes_list[0]+(rounds_in_co_template+max_offset)*width)]])

        if use_top_x_percent>0:
            import pandas as pd
            df_id_to_sad = pd.DataFrame({'list_idx':[],'sad_value':[]})
        #1st is best, as we have highest correlation to our very good template --> we orient on this!
        baseline_encryption = trace[int(start_aes_list[0]):int(start_aes_list[0]+(rounds_in_co_template)*width)]
        #for i, color in zip(range(show_offset,show_offset+nr_traces_to_show), colors): #Adjust range(n) to plot certain traces
        
        for aes_idx,list_idx in zip(start_aes_list[1:],range(len(start_aes_list[1:]))):
            sad_values = [calc_sad(baseline_encryption,trace[int(aes_idx-(offset)*width):int(aes_idx-(offset)*width)+len(baseline_encryption)]) for offset in range(-max_offset,max_offset+1)]
            best_offset = np.array(range(-max_offset,max_offset+1))[np.argmin(sad_values)]

            #sad_values = accl.calc_sad(baseline_encryption,trace[int(aes_idx-(max_offset*width)):int(aes_idx+(max_offset*width)+len(baseline_encryption))])
            #best_offset_new=np.array(range(int(-(max_offset*width)),int((max_offset*width)+len(baseline_encryption))))[np.argmin(sad_values)]      
            sad_values_offset_width = [calc_sad(baseline_encryption,trace[int(aes_idx-(best_offset*width + offset_width)):int(aes_idx-(best_offset*width + offset_width))+len(baseline_encryption)]) for offset_width in range(-width,width+1)]

            best_offset_width = np.array(range(-width,width+1))[np.argmin(sad_values_offset_width)]
            #print("best offset old: " + str(best_offset) + " best offset width: " +str(best_offset_width) +"   best offset new" + str(best_offset_new))
            if use_top_x_percent > 0:
                df_id_to_sad.append({'list_idx':aes_idx,'sad_value':np.amin(sad_values_offset_width)},ignore_index=True)
            #print(best_offset_width)
            finished_cut_aes_traces = np.append(finished_cut_aes_traces,[trace[int(aes_idx-((max_offset+best_offset)*width + best_offset_width)):int(aes_idx-((max_offset+best_offset)*width + best_offset_width))+len(finished_cut_aes_traces[0])]],axis=0)
        if plot_template_on_index>0:
            show_offset = 35
            nr_traces_to_show = plot_template_on_index
            reset_output()
            output_notebook()
            p = figure(width=900, height=600)
            # create a color iterator
            colors = itertools.cycle(palette)  
            x_range = range(0, len(finished_cut_aes_traces[0]))
            p.line(x_range, finished_cut_aes_traces[0], color="black",legend_label=str(0))

            for i, color in zip(range(show_offset,show_offset+nr_traces_to_show), colors): #Adjust range(n) to plot certain traces
                p.line(x_range, finished_cut_aes_traces[i], color=color,legend_label=str(i))
            print(str(nr_traces_to_show)+" of "+str(len(finished_cut_aes_traces)) +" imported traces below (unprocessed)!")
            p.legend.click_policy="hide"

            show(p)
        if use_top_x_percent>0:
            df_id_to_sad = df_id_to_sad.sort_values(by=['sad_value'])
            idx_list = np.concatenate((np.array([0]),np.array(df_id_to_sad['list_idx'],dtype=int)[:int(len(finished_cut_aes_traces)/100*use_top_x_percent)]))
        else:
            idx_list = np.arange(0,len(finished_cut_aes_traces),dtype=int)
        sad_adjusted_template = np.average([finished_cut_aes_traces[idx] for idx in idx_list],axis=0)[max_offset*width:len(finished_cut_aes_traces[0])-max_offset*width]
        if plot_finished_template:
            reset_output()
            output_notebook()
            p = figure(width=900, height=600)
            x_range = range(0, len(sad_adjusted_template))
            p.line(x_range, sad_adjusted_template, color="green",legend_label="refined_template")
            p.legend.click_policy="hide"
            show(p)
        return sad_adjusted_template

    def get_template_with_sad_old(self, plot_template_on_index=0, plot_finished_template=False):
        #adjust offsets when cutting. idea:
        # 1st. try all offsets (-max_offset to +max_offset) with SAD and see what is best
        # 2nd. try offsets in this bracket (-width,+width) for minimum SAD!
        #ranking possible due to min SAD for each trace!
        rounds_in_co_template = self.trace_container.rounds_in_co_template
        max_offset=rounds_in_co_template
        width = int(self.trace_container.calculated_width)
        trace = self.trace_container.get_trace()
        start_aes_list = np.array(self.trace_container.calculated_start_idx_aes)
        finished_cut_aes_traces = np.array([trace[int(start_aes_list[0]-(max_offset)*width):int(start_aes_list[0]+(rounds_in_co_template+max_offset)*width)]])

        #1st is best, as we have highest correlation to our very good template --> we orient on this!
        baseline_encryption = trace[int(start_aes_list[0]):int(start_aes_list[0]+(rounds_in_co_template)*width)]
        sad_values_for_each_idx = np.array([0])

        for aes_idx in start_aes_list[1:]:
            sad_values = [calc_sad(baseline_encryption,trace[int(aes_idx-(offset)*width):int(aes_idx-(offset)*width)+len(baseline_encryption)]) for offset in range(-max_offset,max_offset+1)]
            best_offset = np.array(range(-max_offset,max_offset+1))[np.argmin(sad_values)]
            sad_values_offset_width = [calc_sad(baseline_encryption,trace[int(aes_idx-(best_offset*width + offset_width)):int(aes_idx-(best_offset*width + offset_width))+len(baseline_encryption)]) for offset_width in range(-width,width+1)]

            best_offset_width = np.array(range(-width,width+1))[np.argmin(sad_values_offset_width)]
            sad_values_for_each_idx = np.append(sad_values_for_each_idx,np.min(sad_values_offset_width))
            #print(best_offset_width)
            finished_cut_aes_traces = np.append(finished_cut_aes_traces,[trace[int(aes_idx-((max_offset+best_offset)*width + best_offset_width)):int(aes_idx-((max_offset+best_offset)*width + best_offset_width))+len(finished_cut_aes_traces[0])]],axis=0)
        if plot_template_on_index>0:
            show_offset = 0
            nr_traces_to_show = plot_template_on_index
            reset_output()
            output_notebook()
            p = figure(width=900, height=600)
            # create a color iterator
            colors = itertools.cycle(palette)  
            x_range = range(0, len(finished_cut_aes_traces[0]))
            for i, color in zip(range(show_offset,show_offset+nr_traces_to_show), colors): #Adjust range(n) to plot certain traces
                p.line(x_range, finished_cut_aes_traces[i], color=color)
            print(str(nr_traces_to_show)+" of "+str(len(finished_cut_aes_traces)) +" imported traces below (unprocessed)!")
            show(p)
        sad_adjusted_template = np.average(finished_cut_aes_traces,axis=0)[max_offset*width:len(finished_cut_aes_traces[0])-max_offset*width]
        if plot_finished_template:
            reset_output()
            output_notebook()
            p = figure(width=900, height=600)
            x_range = range(0, len(sad_adjusted_template))
            p.line(x_range, sad_adjusted_template, color="green")
            show(p)
        return sad_adjusted_template

