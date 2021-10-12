#!/usr/bin/python3
import numpy as np
import scipy

import matplotlib.pyplot as plt
import tikzplotlib
import holoviews as hv
from bokeh.plotting import figure, show
from bokeh.io import output_notebook, reset_output, save, export_svgs
from bokeh.palettes import Dark2_5 as palette

import os
from numba import jit
from scipy import signal
import itertools

import pandas as pd


#printlvl="debug"
printlvl="less_info"


def _print(msg,print_info="debug"):
    if print_info==printlvl:
        print(msg)

    


def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    if total==0:
        total=1
        iteration=1
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def odd(number):
    if(number%2==0):
        return number-1
    else:
        return number

@jit(nopython=True)
def detrending_filter(y,windowsize):
    offset = int(windowsize/2)
    result_signal = np.array([y[i]-np.mean(y[max(0,i-offset):min(len(y)-1,i+offset)]) for i in range(len(y))])
    return result_signal

@jit(nopython=True)
def calc_sad_over_everything(template,trace):
    return [np.sum(np.array([np.abs(template[idx]-trace[i+idx]) for idx in range(len(template))],type=float)) for i in range(len(trace)-len(template)-1)]

@jit(nopython=True)
def calc_sad(a,b):
    return np.sum(np.array([np.abs(a[idx]-b[idx]) for idx in range(len(a))],type=float))

def autocorr_loop(len_all_rounds,w,data,no_similar_rounds):
    correlation_list = [np.mean([np.abs(np.corrcoef(mean_axis0(np.array([data[i+w*f:i+w*(f+1)] for f in range(no_similar_rounds)])),data[i+j*w:i+(j+1)*w])[0,1]) for j in range(no_similar_rounds)]) for i in range(len(data)-len_all_rounds)]

    return correlation_list

def mean_axis0(a):
    return np.array([np.mean(a[:,i]) for i in range(a.shape[1])])

def highpass_filter(y, fr, stop_freq=100000000,pass_freq=150000000):
  filter_stop_freq = stop_freq  # Hz
  filter_pass_freq = pass_freq  # Hz
  filter_order = min((101,odd(int(len(y)/4))))

  # High-pass filter
  nyquist_rate = fr / 2.
  desired = (0, 0, 1, 1)
  bands = (0, filter_stop_freq, filter_pass_freq, nyquist_rate)
  filter_coefs = scipy.signal.firls(filter_order, bands, desired, nyq=nyquist_rate)

  # Apply high-pass filter
  filtered_audio = scipy.signal.filtfilt(filter_coefs, [1], y)
  return filtered_audio


# Pick top N values out of list:
def top_x_array(a,N,scale = 1): 
    max_ind = np.argsort(a)[::-1][:N]
    return np.column_stack((a[max_ind],max_ind*scale))



def plot_found_segments(trace,starting_points,length):
    reset_output()
    output_notebook()
    p = figure(width=900, height=600,title="Different extracted CO-Segments")
    # create a color iterator
    colors = itertools.cycle(palette)  
    x_range = range(length)
    p.line(x_range, trace[starting_points[0]:starting_points[0]+length], color="black",legend_label=str(0))

    for i, color in zip(range(1,len(starting_points)), colors): #Adjust range(n) to plot certain traces
        p.line(x_range,np.array(trace[starting_points[i]:starting_points[i]+length]), color=color, legend_label=str(i))
    p.legend.click_policy="hide"

    show(p)

class Exporter:
    def __init__(self,root_folder="./"):
        self.root_folder = root_folder

    def export_data(self, data_y, filename="i_was_lazy",data_x = None, fs = 1):
        if data_x == None:
            if fs > 1:
                data_x = np.arange(0,len(data_y)/fs,step=1/fs,dtype=float)
            else:
                data_x = np.arange(0,len(data_y),step=1,dtype=int)
        data = np.transpose(np.concatenate(([data_y],[data_x])))
        np.savetxt(str(self.root_folder) + str(filename) + ".csv",X=data ,delimiter=',',header="y_values,x_values", comments='')

    def export_dict(self,dict_save,filename="i_was_lazy"):
        df = pd.DataFrame.from_dict(dict_save)
        df.to_csv(str(self.root_folder)+str(filename)+".csv",mode='w')
        print("EXPORTED TO: " + str(self.root_folder)+str(filename)+".csv")


    def export_df(self,df_save,filename="i_was_lazy"):
        df_save.to_csv(str(self.root_folder)+str(filename)+".csv",mode='w')
        print("EXPORTED TO: " + str(self.root_folder)+str(filename)+".csv")
        
        
    def export_tikz(self, data_y, filename="i_was_lazy",data_x = None):
        if data_x == None:
            data_x = np.arange(0,len(data_y),step=1,dtype=int)
        plt.style.use("ggplot")
        plt.plot(data_x,data_y,"-")
        plt.xlabel("Sample (1)")
        plt.ylabel("Power")
        plt.title("Testplot smthing")
        plt.grid(True)
        tikzplotlib.save(str(self.root_folder) + filename + ".tex")
        

class Plotter:
    def __init__(self,x,y,x_label,y_label,title,curve_label,additional_y_stuff = None,additional_x_stuff = None,additional_y_stuff_label = "something?",save_filename=None,decimation_factor = 1):
        self.x = x
        self.y = y
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.curve_label = curve_label
        self.additional_y_stuff = additional_y_stuff
        self.additional_x_stuff = additional_x_stuff
        self.save_filename = save_filename
        self.decimation_factor = decimation_factor
        self.show()

    def show(self):
        hv.extension('bokeh')
        reset_output()
        output_notebook()
        if self.decimation_factor>1:
            self.x = signal.decimate(self.x, self.decimation_factor)#itertools.islice(self.x, 0, None, self.decimation_factor)#signal.decimate(self.x, self.decimation_factor)
            self.y = signal.decimate(self.y, self.decimation_factor)
            if self.additional_y_stuff!=None:
                self.additional_y_stuff = signal.decimate(self.additional_y_stuff, self.decimation_factor)
            if self.additional_x_stuff!=None:
                self.additional_x_stuff = signal.decimate(self.additional_x_stuff, self.decimation_factor)
        curve = hv.Curve((self.x,np.array(self.y)),label=self.curve_label)
        if self.additional_y_stuff!=None:
            for y_stuff in self.additional_y_stuff:
                print(y_stuff)
                curve *= hv.Curve((self.x,np.array(y_stuff)),label=additional_y_stuff_label)
        if self.additional_x_stuff!=None:
            for x_stuff in self.additional_x_stuff:
                print(x_stuff)
                #print(self.y[np.where(self.x==x_stuff.astype(int))])
                points = hv.Points((np.array(x_stuff),np.array(self.y[np.array([np.where(self.x==some_x)[0] for some_x in x_stuff.astype(int)]).flatten()])),marker="+",label="hits?")
                points.opts(color='r', marker='+', size=10)
                curve *= points
        curve = curve.options(xlabel=self.x_label, ylabel=self.y_label)   
        curve.opts(width=900, height=600)
        hv.extension('bokeh')
        #hv.save(curve,'test.svg',fmt='',backend='bokeh')
        p =  hv.render(curve, backend='bokeh')
        show(p)
        if self.save_filename!= None:
            output_file(save_filename, mode='inline')
            save(p)

    def save(self,filename=None):
        if filename==None:
            filename = self.title
        print("save() : NOT IMPLEMENTED!")
        #go save routine :D whatever that may be!

    
            

