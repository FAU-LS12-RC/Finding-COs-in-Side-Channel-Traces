#!/usr/bin/python3

# sure imports
import numpy as np
import holoviews as hv
from bokeh.plotting import figure, show
from bokeh.io import output_notebook, reset_output

from src.helper import _print, detrending_filter
from src.autocorrelation_accl import Autocorrelation_Accelerator


class SampleFinder:
    def __init__(self, trace_container, top_x=10, do_plots=False, print_info=True, error_margin=0.02, exact_clk_cycles=None, allowed_sub_peak_delta=2):
        if(print_info):
            print("initialized the sample finder with " + str(trace_container.nr_hidden_cos) +
                  " hidden aes cycles, sample rate of " + str(trace_container.get_fs()))

        self.trace_container = trace_container

        if exact_clk_cycles == None:
            self.min_clk_cycles = max(
                1, int(trace_container.known_width_clk_cycles*0.95))
            self.max_clk_cycles = max(
                self.min_clk_cycles+1, int(trace_container.known_width_clk_cycles*1.05))
        else:
            self.min_clk_cycles = exact_clk_cycles
            self.max_clk_cycles = exact_clk_cycles+1

        # is config of sample finder:
        self.store_for_latex = False
        self.top_x = top_x
        self.error_margin = error_margin
        self.print_info = print_info
        self.do_plots = do_plots
        self.dict_plots = None
        self.df_corr_for_each_width = None
        self.allowed_sub_peak_delta = allowed_sub_peak_delta

        self.correlation_dict = {}
        self.filtered_correlation_dict = {}
        self.mean_event_dicts = {}

    #
    def full_auto_find_COs(self, do_quality_plot=False, do_main_sub_peak_plot=False, sad_for_autocorr=False, sad_approach=True, avg_round_template=True, use_detrended=False):
        """
            full_auto_find_COs Finds all COs in the trace in self.trace_container.

            :param do_quality_plot: If this is set, the similarity of step 1 will be plotted (takes a lot of time)
            :param do_main_sub_peak_plot: If this is set, the similarity of step 3 will be plotted. This is where the main-peaks and sub-peaks are.
            :param sad_for_autocorr: Calculates the round-similarity with SAD instead of the Pearson correlation
            :param sad_approach: Calculates the similarity of the found template candidate (through step 1) with SAD instead of the Pearson correlation
            :param avg_round_template: Instead of using the entire CO as a template, average all rounds, then concatenate them together
            :param use_detrended: Use a rolling average filter to detrend the similarity of the similarity in step 1
            :return: returns a triple with the best_fitting_width found, a list of starting indices that we found and the CO-Template candidate that we chose.
        """
        f_device = self.trace_container.known_device_frequency
        self.trace_container.calculated_device_frequency = f_device
        samples_per_clock = self.trace_container.get_fs() / f_device
        print("samples per clock: " + str(samples_per_clock))
        possible_widths = np.arange(samples_per_clock*self.min_clk_cycles,
                                    samples_per_clock*self.max_clk_cycles, step=samples_per_clock, dtype=int)
        print("possible widths (samples): " + str(possible_widths))
        print("possible widths (cycles):  " +
              str(np.arange(self.min_clk_cycles, self.max_clk_cycles)))
        self.f_device = f_device

        # 2. Test all possible widths, find starting index that has best autocorreltaion
        from time import process_time
        t1_start = process_time()
        opencl_autocorr = Autocorrelation_Accelerator(self.trace_container.get_trace(
        ), self.trace_container.no_similar_rounds, self.top_x, do_plots=do_quality_plot, use_detrended=use_detrended, trace_container=self.trace_container)
        if sad_for_autocorr:
            best_widths, widths_correlation, correlation_for_each_width = opencl_autocorr.autosad_accelerated_updated(
                possible_widths)
        else:
            best_widths, widths_correlation, correlation_for_each_width = opencl_autocorr.autocorrelation_accelerated_updated(
                possible_widths)
        t1_stop = process_time()
        self.alg1_time_sec = t1_stop-t1_start
        if self.print_info:
            print("GPU: Finding best possible starting points used " +
                  str((t1_stop-t1_start)) + " seconds")
            print(best_widths)
            best_width = possible_widths[int(best_widths[0, 1])]
            starting_position = widths_correlation[int(
                best_widths[0, 1]), 0, 1]
            # print(best_widths)
            print("best_width = " + str(best_width) + " with correlation of: " +
                  str(best_widths[0, 0]) + " at starting position: " + str(starting_position))

        # 3. calculate best fitting width, utilizing the number of sub-peaks behind each main-peak.
        find_best_fitting_width_start = process_time()
        best_fitting_width, peak_idx_list, char_trace_template = self.get_best_fitting_width(
            best_widths, possible_widths, widths_correlation, f_device, sad_approach=sad_approach, avg_round_template=avg_round_template, allowed_sub_peak_delta=self.allowed_sub_peak_delta, do_plots=do_main_sub_peak_plot)
        find_best_fitting_width_end = process_time()
        self.alg2_time_sec = find_best_fitting_width_end-find_best_fitting_width_start
        if self.print_info:
            print("best fitting width is :   " + str(best_fitting_width))
            print("found on cpu using " + str((find_best_fitting_width_end -
                  find_best_fitting_width_start)) + " seconds")
        self.trace_container.calculated_start_idx_aes = peak_idx_list
        self.trace_container.calculated_width = best_fitting_width
        return (best_fitting_width, peak_idx_list, char_trace_template)

    def number_of_equidistant_peaks(self, x, distance, main_peak_idx=0, max_peaks=9, delta=1):
        number_of_peaks = 0
        max_idx = len(x)-1
        for sub_peak_idx in np.arange(distance, main_peak_idx+distance*max_peaks, step=distance):
            if(sub_peak_idx+2 * delta-1 > max_idx):
                return number_of_peaks
            #idx_is_peak = (x[sub_peak_idx]>x[sub_peak_idx+delta] and x[sub_peak_idx]>x[sub_peak_idx-delta] and (x[sub_peak_idx]<=x[main_peak_idx]))
            idx_is_peak = self.is_a_peak(x, sub_peak_idx, main_peak_idx, delta)
            if delta > 1:
                for idx in np.arange(sub_peak_idx-delta, sub_peak_idx+delta, step=1, dtype=int):
                    if self.is_a_peak(x, idx, main_peak_idx, delta):
                        idx_is_peak = self.is_a_peak(
                            x, idx, main_peak_idx, delta)
            if idx_is_peak:
                number_of_peaks += 1
            else:
                return number_of_peaks
        return number_of_peaks

    def is_a_peak(self, x, idx, main_peak_idx, delta=1):
        return (x[idx] > x[idx+delta] and x[idx] > x[idx-delta] and (x[idx] <= x[main_peak_idx]))

    def find_peaks(self, correlation, w_segment, w_event, correlation_step_size, min_number_of_sub_peaks=8, no_rounds=64, max_num_peaks=5000, allowed_sub_peak_delta=2):
        if self.print_info:
            print("Finding main- and sub-peaks for width : " +
                  str(w_segment*correlation_step_size))
        correlation_orig = np.copy(correlation)
        correlation_removed_peaks = np.copy(correlation)
        peak_idx = []
        nr_of_peaks = 0

        for i in range(max_num_peaks):
            # find next main-peak at max_idx
            max_idx = np.argmax(correlation_removed_peaks)
            if(max_idx > len(correlation_orig)-w_event):  # add 0 if we need them!
                correlation = np.concatenate(
                    (correlation, np.zeros(w_event+1)))
                correlation_removed_peaks = np.concatenate(
                    (correlation_removed_peaks, np.zeros(w_event+1)))
                correlation_orig = np.concatenate(
                    (correlation_orig, np.zeros(w_event+1)))
            nr_of_peaks = self.number_of_equidistant_peaks(
                correlation_orig[max_idx:max_idx+w_event+2*allowed_sub_peak_delta], distance=w_segment, delta=allowed_sub_peak_delta, max_peaks=no_rounds)
            _print("nr_of_equidistant_peaks = " +
                   str(nr_of_peaks), print_info="debug")

            if True:  # if we want to check before peaks
                nr_of_peaks_before = self.number_of_equidistant_peaks(np.flip(correlation_orig[np.max(
                    (max_idx-w_event-2*allowed_sub_peak_delta, 0)):max_idx+1]), distance=w_segment, delta=allowed_sub_peak_delta, max_peaks=no_rounds)
                _print("nr_of_equidistant_peaks_before = " +
                       str(nr_of_peaks_before), print_info="debug")
                nr_of_peaks = (nr_of_peaks + nr_of_peaks_before)/2

            if nr_of_peaks < min_number_of_sub_peaks:
                # not enough sub peaks, probably no more aes in here! (at leas no well detectable aes cycles!)
                if self.print_info:
                    print("We found " + str(i) + " peaks. Not enough sub-peaks for next main-peak at position: " +
                          str(max_idx*correlation_step_size))
                break

            peak_idx.append(max_idx*correlation_step_size)
            for i in range(max(0, max_idx-int(w_event*0.7)), min(len(correlation_removed_peaks), max_idx + int(w_event*0.7))):
                correlation_removed_peaks[i] = 0
        return peak_idx, nr_of_peaks

    # Evaluate certain best width:
    def get_peaks_for_width(self, f_device, width, starting_position, min_number_of_sub_peaks=8, do_plots=False, print_info=False, max_num_peaks=5000, new_chosen_mean_event=None, sad_approach=False, avg_round_template=True, allowed_sub_peak_delta=1):
        samples_per_clock = self.trace_container.get_fs()/f_device
        w = int(width)
        i = int(starting_position)
        # IDEA: starting position could be "in the middle of a clock cycle" => calculate offset! from 0
        start_offset = i % samples_per_clock
        correlation_step_size = min(w/4, samples_per_clock)
        if not w in self.correlation_dict:
            # we create a new characteristic trace from scratch at starting point i and correlate/sad it with everything!
            idx_list = np.arange(start_offset, len(self.trace_container.get_trace(
            ))-(self.trace_container.no_similar_rounds*w), step=correlation_step_size, dtype=int)
            # check bounds:
            if (i+w*self.trace_container.no_similar_rounds) > len(self.trace_container.get_trace()):
                return (-1, -1, -1)
            if avg_round_template:
                chosen_mean_segment = np.average([self.trace_container.get_trace(
                )[i+w*j:i+w*(j+1)] for j in range(self.trace_container.no_similar_rounds)], axis=0)
                chosen_mean_event = np.array([chosen_mean_segment for j in range(
                    self.trace_container.no_similar_rounds)]).flatten()
            else:
                chosen_mean_event = self.trace_container.get_trace(
                )[i:i+w*self.trace_container.rounds_in_co_template]

            if not sad_approach:
                corrl_accl = Autocorrelation_Accelerator()
                all_correlation = corrl_accl.correlate(
                    self.trace_container.get_trace(), chosen_mean_event, idx_list, opencl=True)

                filtered_correlation = detrending_filter(
                    all_correlation, (w)/correlation_step_size)
                self.mean_event_dicts[w] = chosen_mean_event
                self.correlation_dict[w] = all_correlation
                self.filtered_correlation_dict[w] = filtered_correlation
            else:
                corrl_accl = Autocorrelation_Accelerator()
                self.mean_event_dicts[w] = chosen_mean_event
                sad_over_everything = np.array(corrl_accl.calc_sad(
                    self.mean_event_dicts[w], self.trace_container.get_trace(), idx_list=idx_list))
                all_correlation = -1*sad_over_everything
                filtered_correlation = detrending_filter(
                    all_correlation, (w)/correlation_step_size)
                self.correlation_dict[w] = all_correlation
                self.filtered_correlation_dict[w] = filtered_correlation
            if do_plots:
                reset_output()
                output_notebook()
                p = figure(width=900, height=600)
                x_range = range(0, len(self.trace_container.get_trace()))
                corr_plot_y = all_correlation * \
                    np.max(self.trace_container.get_trace())
                p.line(np.arange(0, len(self.trace_container.get_trace()), step=correlation_step_size)[
                       :len(corr_plot_y)], corr_plot_y, color='black')
                filtered_corr_plot_y = filtered_correlation * \
                    np.max(self.trace_container.get_trace()) - \
                    np.max(self.trace_container.get_trace())
                p.line(np.arange(0, len(self.trace_container.get_trace()), step=correlation_step_size)[
                       :len(filtered_corr_plot_y)], filtered_corr_plot_y, color='orange')
                show(p)
        else:
            filtered_correlation = self.filtered_correlation_dict[w]
            all_correlation = self.correlation_dict[w]
            chosen_mean_event = self.mean_event_dicts[w]

        peak_idx_list, least_peaks = self.find_peaks(filtered_correlation, int(w/correlation_step_size), int((self.trace_container.no_similar_rounds*w)/correlation_step_size),
                                                     correlation_step_size, min_number_of_sub_peaks, max_num_peaks=max_num_peaks, allowed_sub_peak_delta=allowed_sub_peak_delta, no_rounds=self.trace_container.no_similar_rounds)
        peak_idx_list = (np.array(peak_idx_list))

        # remove overlapping peaks if they dont fit
        if(len(peak_idx_list) > self.trace_container.nr_hidden_cos):
            # here we check if the peaks that where added at last fit into the by then collected peaks. if they do, its not our case!
            min_peak = int(
                peak_idx_list[self.trace_container.nr_hidden_cos-1]/correlation_step_size)
            max_peak = int(peak_idx_list[0]/correlation_step_size)
            min_threshold = filtered_correlation[min_peak] - (
                filtered_correlation[max_peak] - filtered_correlation[min_peak])
            min_threshold = filtered_correlation[min_peak] - (
                filtered_correlation[max_peak] - filtered_correlation[min_peak])*2/self.trace_container.nr_hidden_cos
            for overlap_peak_idx in range(self.trace_container.nr_hidden_cos, len(peak_idx_list)):
                overlap_peak = peak_idx_list[overlap_peak_idx] / \
                    correlation_step_size
                #if self.print_info: print("hidden cycles = "+ str(self.trace_container.nr_hidden_cos) +"removed, peaklistlennow:" + str(len(peak_idx_list)))
                if filtered_correlation[int(overlap_peak)] < min_threshold:
                    # remove this point and because it does not belong here
                    peak_idx_list = peak_idx_list[:overlap_peak_idx]
                    if self.print_info:
                        print("REMOVED last peaks because they are too low: hidden cycles = " + str(
                            self.trace_container.nr_hidden_cos) + " peaklistlennow:" + str(len(peak_idx_list)))
                    break
        return (peak_idx_list, least_peaks, chosen_mean_event)

    # Evaluate certain best width:
    def get_best_fitting_width(self, best_widths, w_list, widths_correlation, f_device, sad_approach=False, avg_round_template=True, allowed_sub_peak_delta=1, do_plots=False):
        best_fitting_width = 0
        least_peaks_array = np.zeros(
            len(best_widths[:, 1]))+self.trace_container.no_similar_rounds
        peak_idx_list = []
        return_peak_idx_list = []

        chosen_mean_events = [np.zeros(int(best_widths[i, 1]))
                              for i in range(len(best_widths[:, 1]))]
        for min_number_of_sub_peaks in np.arange(self.trace_container.no_similar_rounds-1, 1, step=-1, dtype=int):
            if self.print_info:
                print("Try with min number of " +
                      str(min_number_of_sub_peaks) + " sub peaks for each CO!")
            print("--------------------------------------------------------------------")
            least_peaks_array_idx = 0
            for width_idx, idx in zip(best_widths[:, 1], range(len(best_widths[:, 1]))):
                # skip the ones that won't get new peaks this round:
                if least_peaks_array[least_peaks_array_idx] < min_number_of_sub_peaks:
                    least_peaks_array_idx += 1
                    continue
                width = w_list[int(width_idx)]
                starting_position = widths_correlation[int(width_idx), 0, 1]
                # Find number of main-peaks for this width with at least min_number_of_subpeaks:
                peak_idx_list, least_peaks_array[least_peaks_array_idx], chosen_mean_events[idx] = self.get_peaks_for_width(f_device, width, starting_position, min_number_of_sub_peaks=min_number_of_sub_peaks, do_plots=do_plots, max_num_peaks=(
                    self.trace_container.nr_hidden_cos*2 + self.trace_container.nr_hidden_cos*allowed_sub_peak_delta), sad_approach=sad_approach, avg_round_template=avg_round_template, allowed_sub_peak_delta=allowed_sub_peak_delta)
                if least_peaks_array[least_peaks_array_idx] == -1:
                    continue
                if(len(peak_idx_list) >= int(self.trace_container.nr_hidden_cos) and len(peak_idx_list) <= self.trace_container.nr_hidden_cos + int(self.trace_container.nr_hidden_cos*self.error_margin)):  # Margin for error :)
                    peak_idx_list = peak_idx_list[:self.trace_container.nr_hidden_cos]
                    print("right number of COs for width of " + str(width))
                    if self.print_info:
                        print("peaks: ")
                    if self.print_info:
                        print(peak_idx_list)
                    best_fitting_width = width
                    return_peak_idx_list = peak_idx_list
                    first_index = int(starting_position)
                    char_round_template = np.average([self.trace_container.get_trace(
                    )[first_index+width*j:first_index+width*(j+1)] for j in range(self.trace_container.no_similar_rounds)], axis=0)
                    char_trace_template = np.array([char_round_template for j in range(
                        self.trace_container.no_similar_rounds)]).flatten()
                    self.min_number_of_sub_peaks_needed = min_number_of_sub_peaks
                    break
                if len(peak_idx_list) > self.trace_container.nr_hidden_cos + int(self.trace_container.nr_hidden_cos*self.error_margin):
                    continue
                least_peaks_array_idx += 1
            if(best_fitting_width != 0):
                return best_fitting_width, return_peak_idx_list, char_trace_template
        return -1, -1, -1  # no fitting width found!

    def find_COs_with_template(self, template, do_plots=False, print_info=True, use_sad=True, no_decimation=True):
        corrl_accl = Autocorrelation_Accelerator()
        samples_per_clock = self.trace_container.get_fs(
        )/self.trace_container.calculated_device_frequency
        w = int(self.trace_container.calculated_width)
        if self.trace_container.calculated_start_idx_aes[0] != None:
            i = int(self.trace_container.calculated_start_idx_aes[0])
            # IDEA: starting position could be "in the middle of a clock cycle" => calculate offset! from 0
            start_offset = i % samples_per_clock
            correlation_step_size = min(w/2, samples_per_clock)
        else:
            start_offset = 0
            correlation_step_size = min(w/2, samples_per_clock)
        if no_decimation:
            correlation_step_size = 1
        idx_list = np.arange(start_offset, len(self.trace_container.get_trace(
        ))-len(template), step=correlation_step_size, dtype=int)
        if use_sad:
            correlation = np.array(corrl_accl.calc_sad(
                template, self.trace_container.get_trace(), idx_list))*-1
        else:
            correlation = corrl_accl.correlate(
                self.trace_container.get_trace(), template, idx_list, opencl=True)
        filtered_correlation = detrending_filter(
            correlation, (int(self.trace_container.calculated_width))/correlation_step_size)
        if do_plots:
            curve = hv.Curve((range(0, len(filtered_correlation)), np.array(
                filtered_correlation)), label="filtered correlation")
            curve = curve.options(xlabel='Sample', ylabel='correlation')
            curve.opts(width=900, height=600)
            hv.extension('bokeh')
            # hv.save(curve,'test.svg',fmt='',backend='bokeh')
            p = hv.render(curve, backend='bokeh')
            show(p)
        peak_idx_list, peak_end_idx_list = self.get_peaks_above_threshold(
            filtered_correlation, correlation_step_size)

        return peak_idx_list

    def get_peaks_above_threshold(self, correlation, correlation_step_size, threshold=0):
        correlation_removed_peaks = np.copy(correlation)
        window_size = int(self.trace_container.calculated_width) * \
            self.trace_container.no_similar_rounds

        peak_idx = []
        peak_end_idx = []
        num_peaks = self.trace_container.nr_hidden_cos

        for i in range(num_peaks):
            max_idx = np.argmax(correlation_removed_peaks)
            if correlation[max_idx] < threshold:
                break
            peak_idx.append(max_idx*correlation_step_size)
            peak_end_idx.append(max_idx*correlation_step_size+window_size)
            for i in range(max(0, max_idx-int(window_size/correlation_step_size*0.7)), min(len(correlation_removed_peaks), max_idx + int(window_size/correlation_step_size*0.7))):
                correlation_removed_peaks[i] = 0

        return np.array(peak_idx), np.array(peak_end_idx)
