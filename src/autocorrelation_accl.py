#!/usr/bin/python3
from __future__ import absolute_import
from __future__ import print_function
# sure imports
import numpy as np
import scipy
import pyopencl as cl

from src.helper import printProgressBar, top_x_array, Plotter, detrending_filter, autocorr_loop
# open-cl stuff:


class Autocorrelation_Accelerator:
    def __init__(self, data=None, no_similar_rounds=None, top_x=10, do_plots=False, use_detrended=False, hidden_aes_operations=33, trace_container=None):
        self.data = data
        self.no_similar_rounds = no_similar_rounds
        self.top_x = top_x
        self.do_plots = do_plots
        self.use_detrended = use_detrended
        self.hidden_aes_operations = hidden_aes_operations
        self.trace_container = trace_container

    def calc_sad(self, template_candidate, trace, idx_list=[]):
        # insert code here :)
        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)
        mf = cl.mem_flags

        # setup memory:
        trace_host = trace.astype(np.float32)
        trace_dev = cl.Buffer(ctx, mf.READ_ONLY |
                              mf.COPY_HOST_PTR, hostbuf=trace_host)
        template_candidate_host = template_candidate.astype(np.float32)
        template_candidate_dev = cl.Buffer(
            ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=template_candidate_host)
        correlation_dev = cl.Buffer(ctx, mf.WRITE_ONLY, trace_host.nbytes)
        template_length_dev = cl.Buffer(
            ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.int32(len(template_candidate)))

        programstring = """
        #if __OPENCL_VERSION__ < 120
            #if cl_khr_fp64
                #pragma OPENCL EXTENSION cl_khr_fp64 : enable
            #elif cl_amd_fp64
                #pragma OPENCL EXTENSION cl_amd_fp64 : enable
            #else
                #error Missing double precision extension
            #endif
        #endif
        float sad_calculation(__global const float* X, __global const float* avg_segment_adj, int n){ 
            float sad = 0;
            for (int i = 0; i < n; ++i){ 
                sad += fabs((float)(avg_segment_adj[i]-X[i]));
            }
            return sad; 
        } 

        __kernel void correlate(__global const float *data, __global float *correlation,  __global float *template_candidate, __global int *template_length){
            int i = get_global_id(0);
            int idx_max = get_global_size(0);
            int i_template_length = *template_length;

            // Abort if we would otherwise run out of valid idx
            if(i+i_template_length >= idx_max){
                correlation[i] = -1;
                return;
            }
            correlation[i] = sad_calculation(&data[i], template_candidate, i_template_length);
        }
        """
        prg = cl.Program(ctx, programstring).build()

        prg.correlate(queue, trace_host.shape, None, trace_dev,
                      correlation_dev, template_candidate_dev, template_length_dev)

        correlation_host = np.empty_like(trace_host)
        cl.enqueue_copy(queue, correlation_host, correlation_dev)

        #Plotter(range(len(correlation_host)),correlation_host,"Sample","Correlation","Correlation of right width (autocorr)","correlation_host")
        #Plotter(range(len(correlation_host_detrended)),correlation_host_detrended,"Sample","Correlation detrended","Correlation detrended of right width (autocorr)","correlation_host")

        # print(correlation_host)
        # print(len(correlation_host))
        #print("max = " + str(max(correlation_host)))
        if len(idx_list) == 0:
            idx_list = np.array(range(len(trace)))
        else:
            idx_list = np.array(idx_list)
        return correlation_host[idx_list[np.where(idx_list < len(correlation_host)-len(template_candidate))]]

    def correlate(self, trace, template_candidate, idx_list, opencl=True, print_times=True):
        from time import process_time

        t1_start = process_time()
        if not opencl:
            correlation = np.array([np.abs(scipy.stats.pearsonr(
                template_candidate, trace[idx:idx+len(template_candidate)])[0]) for idx in idx_list])
        else:
            # insert code here :)
            ctx = cl.create_some_context()
            queue = cl.CommandQueue(ctx)
            mf = cl.mem_flags

            # setup memory:
            trace_host = trace.astype(np.float32)
            trace_dev = cl.Buffer(ctx, mf.READ_ONLY |
                                  mf.COPY_HOST_PTR, hostbuf=trace_host)
            template_candidate_host = template_candidate.astype(np.float32)
            template_candidate_dev = cl.Buffer(
                ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=template_candidate_host)
            correlation_dev = cl.Buffer(ctx, mf.WRITE_ONLY, trace_host.nbytes)
            template_length_dev = cl.Buffer(
                ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.int32(len(template_candidate)))

            programstring = """
            #if __OPENCL_VERSION__ < 120
                #if cl_khr_fp64
                    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
                #elif cl_amd_fp64
                    #pragma OPENCL EXTENSION cl_amd_fp64 : enable
                #else
                    #error Missing double precision extension
                #endif
            #endif
            float correlationCoefficient(__global const float* X, __global const float* avg_segment_adj, int n){ 
                float sum_X = 0, sum_Y = 0, sum_XY = 0; 
                float squareSum_X = 0, squareSum_Y = 0; 
            
                for (int i = 0; i < n; ++i){ 
                    sum_X = sum_X + X[i]; 
                    sum_Y = sum_Y + avg_segment_adj[i]; 
                    sum_XY = sum_XY + X[i] * avg_segment_adj[i];
                    squareSum_X = squareSum_X + X[i] * X[i]; 
                    squareSum_Y = squareSum_Y + avg_segment_adj[i] * avg_segment_adj[i]; 
                }  
                float corr = (float)(n * sum_XY - sum_X * sum_Y)  / sqrt((float)((n * squareSum_X - sum_X * sum_X) * (n * squareSum_Y - sum_Y * sum_Y))); 
                return corr; 
            } 

            __kernel void correlate(__global const float *data, __global float *correlation,  __global float *template_candidate, __global int *template_length){
                int i = get_global_id(0);
                int idx_max = get_global_size(0);
                int i_template_length = *template_length;

                // Abort if we would otherwise run out of valid idx
                if(i+i_template_length >= idx_max){
                    correlation[i] = 0;
                    return;
                }
                correlation[i] = correlationCoefficient(&data[i], template_candidate, i_template_length);
            }
            """
            prg = cl.Program(ctx, programstring).build()

            prg.correlate(queue, trace_host.shape, None, trace_dev,
                          correlation_dev, template_candidate_dev, template_length_dev)

            correlation_host = np.empty_like(trace_host)
            cl.enqueue_copy(queue, correlation_host, correlation_dev)

            #Plotter(range(len(correlation_host)),correlation_host,"Sample","Correlation","Correlation of right width (autocorr)","correlation_host")
            #Plotter(range(len(correlation_host_detrended)),correlation_host_detrended,"Sample","Correlation detrended","Correlation detrended of right width (autocorr)","correlation_host")

            # print(correlation_host)
            # print(len(correlation_host))
            #print("max = " + str(max(correlation_host)))
            correlation = np.abs(correlation_host)[idx_list]
        t1_stop = process_time()
        if print_times:
            if opencl:
                print("GPU: correlate used " +
                      str((t1_stop-t1_start)) + " seconds")
            else:
                print("CPU: correlate used " +
                      str((t1_stop-t1_start)) + " seconds")
        return correlation

    def autocorrelation_accelerated_updated(self, w_list):
        # go through all possible widhts to determine the best one! (w = perfect segment width)
        correlation_for_each_width = []

        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)
        mf = cl.mem_flags

        #data_dev = cl_array.to_device(queue, self.data)
        data_host = self.data.astype(np.float32)
        correlation_dev = cl.Buffer(ctx, mf.WRITE_ONLY, data_host.nbytes)
        data_dev = cl.Buffer(ctx, mf.READ_ONLY |
                             mf.COPY_HOST_PTR, hostbuf=data_host)

        no_similar_rounds_dev = cl.Buffer(
            ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.int32(self.no_similar_rounds))

        widths_correlation = []
        for w in w_list:
            programstring = "#define WIDTH "+str(w)+"""
            #if __OPENCL_VERSION__ < 120
                #if cl_khr_fp64
                    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
                #elif cl_amd_fp64
                    #pragma OPENCL EXTENSION cl_amd_fp64 : enable
                #else
                    #error Missing double precision extension
                #endif
            #endif

            float correlationCoefficient_stable(__global const float* X, __private const float* avg_segment_adj, int n){ 
                float sum_X = 0, sum_Y = 0, sum_XY = 0; 
                float squareSum_X = 0, squareSum_Y = 0; 
            
                for (int i = 0; i < n; ++i){ 
                    sum_X = sum_X + X[i]; 
                    sum_Y = sum_Y + avg_segment_adj[i]; 
                    sum_XY = sum_XY + X[i] * avg_segment_adj[i];
                    squareSum_X = squareSum_X + X[i] * X[i]; 
                    squareSum_Y = squareSum_Y + avg_segment_adj[i] * avg_segment_adj[i]; 
                }  
                float corr = (float)(n * sum_XY - sum_X * sum_Y)  / sqrt((float)((n * squareSum_X - sum_X * sum_X) * (n * squareSum_Y - sum_Y * sum_Y))+0.00001); 
                return corr; 
            } 

            __kernel void correlate(__global const float *data, __global float *correlation, __global int *no_similar_rounds){
                int i = get_global_id(0);
                int idx_max = get_global_size(0);
                float avg_segment[WIDTH]= { 0 };

                int w = WIDTH;
                int max_rounds = *no_similar_rounds;
                // Abort if we would otherwise run out of valid idx
                if(i+max_rounds*w >= idx_max){
                    correlation[i] = 0;
                    return;
                }
                // Create mean segment:
                for(int round = 0; round < max_rounds; ++round){
                    for(int avg_idx=0; avg_idx<w; ++avg_idx){
                        avg_segment[avg_idx] += data[i+avg_idx+(round*w)]/max_rounds;
                    }
                }
                //find avg correlation:
                float avg_correlation = 0;
                for(int round = 0; round < max_rounds; ++round){
                    float round_correlation = correlationCoefficient_stable(&data[i+round*w],avg_segment,w);
                    avg_correlation += round_correlation/max_rounds;
                }
                correlation[i] = avg_correlation;
            }
            """
            prg = cl.Program(ctx, programstring).build()

            len_all_rounds = w*self.no_similar_rounds
            if(len_all_rounds > len(data_host)):
                break

            # all start positions need to be considered!
            prg.correlate(queue, data_host.shape, None, data_dev,
                          correlation_dev, no_similar_rounds_dev)

            correlation_host = np.empty_like(data_host)
            cl.enqueue_copy(queue, correlation_host, correlation_dev)
            if self.use_detrended:
                correlation_host_detrended = detrending_filter(
                    correlation_host, w*self.no_similar_rounds)
            if self.do_plots:
                if not self.use_detrended:
                    Plotter(range(len(correlation_host)), np.array(correlation_host, dtype=float), "Sample", "Similarity",
                            "Similarity of width" + str(w) + " (autocorr)", "Similarity (Step 1) for width: " + str(w), decimation_factor=30)
                else:
                    Plotter(range(len(correlation_host_detrended)), np.array(correlation_host_detrended, dtype=float), "Sample", "Similarity detrended",
                            "Correlation detrended of width " + str(w) + " (autocorr)", "correlation_host_detrended  " + str(w), decimation_factor=30)

            self.trace_container.quality_plot = correlation_host

            if self.use_detrended:
                add_len = len(correlation_host) - \
                    len(correlation_host_detrended)
                correlation_host = np.concatenate(
                    (correlation_host_detrended, np.zeros(add_len)))

            correlation_for_each_width.append(correlation_host)
            top_x_correlation = top_x_array(
                np.array(correlation_host), self.top_x, scale=1)
            widths_correlation.append(top_x_correlation)
            printProgressBar(len(widths_correlation), len(w_list))

        print("\n")
        print("-------AUTOCORR-------RESULTS-------------------------------")
        widths_correlation = np.array(widths_correlation)
        # np.save("widths_correlation_savepoint",widths_correlation)
        best_widths = top_x_array(widths_correlation[:, 0, 0], 100)
        filtered_best_widths = []
        for item in best_widths:
            if item[0] > 0.:
                filtered_best_widths.append(item)
        best_widths = np.array(filtered_best_widths)
        return best_widths, widths_correlation, correlation_for_each_width

    def autocorrelation_accelerated_knownWidth(self, w):
        # go through all possible widhts to determine the best one! (w = perfect segment width)
        w_list = np.array([w])
        best_widths, widths_correlation, correlation_for_each_width = self.autocorrelation_accelerated_updated(
            w_list)
        return widths_correlation[0], correlation_for_each_width[0]

    def autocorr_cpu(self, w_list):
        # go through all possible widhts to determine the best one! (w = perfect segment width)
        widths_correlation = []

        for w in w_list:
            printProgressBar(np.where(w_list == w)[0][0], len(w_list)-1)
            len_all_rounds = w*self.no_similar_rounds
            if(len_all_rounds > len(self.data)):
                break

            # all start positions need to be considered!
            correlation_list = autocorr_loop(
                len_all_rounds, w, self.data, self.no_similar_rounds)
            # found best correlation spot --> how many peaks do we get here?!
            print(len(correlation_list))
            top_x_correlation = top_x_array(
                np.array(correlation_list), self.top_x, scale=1)
            widths_correlation.append(top_x_correlation)

            #correlation_list_detrended = detrending_filter(correlation_list[:len(correlation_list)-w*self.trace_container.no_similar_rounds],w*self.trace_container.no_similar_rounds*2)

            #Plotter(range(len(correlation_list)),correlation_list,"Sample","Correlation","Correlation of right width (autocorr)","correlation_host")
            #Plotter(range(len(correlation_list_detrended)),correlation_list_detrended,"Sample","Correlation detrended","Correlation detrended of right width (autocorr)","correlation_host")

        print("\n")
        print("--------------RESULTS-------------------------------")
        widths_correlation = np.array(widths_correlation)
        best_widths = top_x_array(widths_correlation[:, 0, 0], 20)
        return best_widths, widths_correlation

    def autosad_accelerated_updated(self, w_list):
        # go through all possible widhts to determine the best one! (w = perfect segment width)
        correlation_for_each_width = []

        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)
        mf = cl.mem_flags

        #data_dev = cl_array.to_device(queue, self.data)
        data_host = self.data.astype(np.float32)
        correlation_dev = cl.Buffer(ctx, mf.WRITE_ONLY, data_host.nbytes)
        data_dev = cl.Buffer(ctx, mf.READ_ONLY |
                             mf.COPY_HOST_PTR, hostbuf=data_host)

        no_similar_rounds_dev = cl.Buffer(
            ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.int32(self.no_similar_rounds))

        widths_correlation = []
        for w in w_list:
            programstring = "#define WIDTH "+str(w)+"""
            #if __OPENCL_VERSION__ < 120
                #if cl_khr_fp64
                    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
                #elif cl_amd_fp64
                    #pragma OPENCL EXTENSION cl_amd_fp64 : enable
                #else
                    #error Missing double precision extension
                #endif
            #endif

            float negative_sad_calculation(__global const float* X, __private const float* avg_segment_adj, int n){ 
                float sad = 0;
                for (int i = 0; i < n; ++i){ 
                    sad -= fabs((float)(avg_segment_adj[i]-X[i]));
                }
                return sad; 
            } 

        
            __kernel void correlate(__global const float *data, __global float *correlation, __global int *no_similar_rounds){
                int i = get_global_id(0);
                int idx_max = get_global_size(0);
                float avg_segment[WIDTH]= { 0 };

                int w = WIDTH;
                int max_rounds = *no_similar_rounds;
                // Abort if we would otherwise run out of valid idx
                if(i+max_rounds*w >= idx_max){
                    correlation[i] = -FLT_MAX;
                    return;
                }
                // Create mean segment:
                for(int round = 0; round < max_rounds; ++round){
                    for(int avg_idx=0; avg_idx<w; ++avg_idx){
                        avg_segment[avg_idx] += data[i+avg_idx+(round*w)]/max_rounds;
                    }
                }
                //find avg correlation:
                float avg_correlation = 0;
                for(int round = 0; round < max_rounds; ++round){
                    float round_correlation = negative_sad_calculation(&data[i+round*w],avg_segment,w);
                    avg_correlation += round_correlation/max_rounds;
                }
                correlation[i] = avg_correlation;
            }
            """
            prg = cl.Program(ctx, programstring).build()

            len_all_rounds = w*self.no_similar_rounds
            if(len_all_rounds > len(data_host)):
                break

            # all start positions need to be considered!
            prg.correlate(queue, data_host.shape, None, data_dev,
                          correlation_dev, no_similar_rounds_dev)

            correlation_host = np.empty_like(data_host)
            cl.enqueue_copy(queue, correlation_host, correlation_dev)
            correlation_host_detrended = detrending_filter(
                correlation_host[:len(correlation_host)-w*self.no_similar_rounds], w)

            if self.do_plots:
                Plotter(range(len(correlation_host[:int(len(correlation_host)-w*self.no_similar_rounds)])), np.array(correlation_host[:int(len(correlation_host)-w *
                        self.no_similar_rounds)], dtype=float), "Sample", "Correlation", "Correlation of right width (autocorr)", "correlation_host", decimation_factor=10)
                Plotter(range(len(correlation_host_detrended)), np.array(correlation_host_detrended, dtype=float), "Sample",
                        "Correlation detrended", "Correlation detrended of right width (autocorr)", "correlation_host_detrended", decimation_factor=10)

            if self.use_detrended:
                add_len = len(correlation_host) - \
                    len(correlation_host_detrended)
                correlation_host = np.concatenate(
                    (correlation_host_detrended, np.zeros(add_len)))
            else:
                correlation_host = correlation_host / \
                    correlation_host.max(axis=0)

            correlation_for_each_width.append(correlation_host)
            top_x_correlation = top_x_array(
                np.array(correlation_host), self.top_x, scale=1)
            print("top x correlation: " + str(top_x_correlation))
            widths_correlation.append(top_x_correlation)
            printProgressBar(len(widths_correlation), len(w_list))

        print("\n")
        print("-------AUTOSAD-------RESULTS-------------------------------")
        widths_correlation = np.array(widths_correlation)
        # np.save("widths_correlation_savepoint",widths_correlation)
        best_widths = top_x_array(widths_correlation[:, 0, 0], 100)
        filtered_best_widths = []
        for item in best_widths:
            if item[0] > 0.:
                filtered_best_widths.append(item)
        best_widths = np.array(filtered_best_widths)
        return best_widths, widths_correlation, correlation_for_each_width
