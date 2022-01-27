#!/usr/bin/python3
import numpy as np

class Evaluator:

    def __init__(self,trace_container,do_plots=False,save_hist = None,max_rnd_offset_adj = 300, epsilon = 0.005):
        self.right_idx = trace_container.known_start_idx_aes
        self.found_idx = trace_container.calculated_start_idx_aes
        self.right_width = trace_container.get_known_width()
        self.found_width = trace_container.calculated_width
        self.no_similar_rounds = trace_container.no_similar_rounds
        self.sorted_found_idx=None
        self.sorted_right_idx=None
        self.epsilon = epsilon
        self.mean = 0
        self.std_dev = 0
        self.quantile_95 = 0
        self.success = False
        self.evaluate(do_plots=do_plots,save_hist = save_hist,print_info = True,max_rnd_offset_adj = max_rnd_offset_adj)

    def __print(self,strng,print_info = True):
        if print_info: print(strng)


    def evaluate(self,print_info = False,do_plots = True, check_width=False, save_hist = None, max_rnd_offset_adj=False):
        self.__print("Evaluator started...",print_info)
        if not check_width or self.right_width == self.found_width:
            self.success = True


            self.__print("Right width found!",print_info)
            self.sorted_right_idx = np.sort(self.right_idx)
            self.sorted_found_idx = np.sort(self.found_idx)
            #residuum_idx = self.sorted_found_idx - self.sorted_right_idx
            closest_to_zero = lambda residuums_i:max((-x*x,x)for x in residuums_i)[1]
            residuum_idx = [closest_to_zero(self.sorted_found_idx-self.sorted_right_idx[i]) for i in range(len(self.sorted_found_idx))]
            
            #print("Correct = " + str(self.sorted_right_idx))
            #print("Found   = " + str(self.sorted_found_idx))
            #print("offsets = " + str(residuum_idx))
            
            zero = len(np.where(np.abs(residuum_idx)<=self.epsilon)[0])
            #self.__print("Perfect fit: " + str(zero) + " --> " + str(zero/len(residuum_idx)*100) + "percent hitrate.",print_info)

            #find adjustment width:
            max_zero = zero
            best_adj_offstet = 0
            for adj_offset in np.arange(-self.right_width*max_rnd_offset_adj,self.right_width*max_rnd_offset_adj,step = 1, dtype=int):
                residuum_idx_adj = residuum_idx + adj_offset
                if len(np.where(np.abs(residuum_idx_adj)<=self.epsilon)[0]) > max_zero:
                    max_zero = len(np.where(np.abs(residuum_idx_adj)<=self.epsilon)[0])
                    best_adj_offstet = adj_offset
            self.best_residuum_idx_adj = [each_idx + best_adj_offstet for each_idx in residuum_idx] 
            self.hitrate = max_zero/len(residuum_idx)
            #self.__print("With adjustment with offset of : " + str(best_adj_offstet) + " samples we get: \n \t Perfect fit: " + str(max_zero) + " --> " + str(self.hitrate * 100) + "percent hitrate.",print_info)
            
            self.hist_bins = np.arange(-self.no_similar_rounds+0.5,self.no_similar_rounds+1.5,step=1,dtype=float)
            self.hist_bins_label = np.arange(-self.no_similar_rounds,self.no_similar_rounds+1,step=1,dtype=int)
            #Convert everything to rounds instead of samples:
            self.best_residuum_idx_adj = [x/self.right_width for x in self.best_residuum_idx_adj]
            
            self.hist = np.histogram(self.best_residuum_idx_adj,bins=self.hist_bins)
            #print(self.hist)
            self.mean = np.mean(self.best_residuum_idx_adj)
            self.std_dev = np.std(self.best_residuum_idx_adj)
            self.quantile_95 = np.quantile(np.abs(self.best_residuum_idx_adj),0.95)
            self.completely_midded_COs = len(np.where(np.abs(self.best_residuum_idx_adj)>=self.no_similar_rounds)[0])
            print("Statistics: \n\tmean: "+str(self.mean) + "    \n\tstd_dev: " + str(self.std_dev)+ " \n\t95% quantile: " + str(self.quantile_95) + "\n\t Totally missed COs: " + str(self.completely_midded_COs))

            if do_plots:
                import matplotlib.pyplot as plt
                from matplotlib import colors
                from matplotlib.ticker import PercentFormatter
                ax = plt.axes()
                plt.hist(self.best_residuum_idx_adj,bins = self.hist_bins ,align='mid', label=self.hist_bins_label)
                ax.yaxis.set_major_formatter(PercentFormatter(xmax=len(residuum_idx)))
                #plt.title("Histogram for residuums")
                plt.xlabel("Offset in Rounds")
                plt.xticks(self.hist_bins_label)
                plt.ylim((0,len(residuum_idx)+1))
                if save_hist!=None:
                    plt.savefig(save_hist,bbox_inches='tight',format='pdf')
                plt.show()

            self.best_residuum_idx_adj_plus_0_5 = [x + 0.5 for x in self.best_residuum_idx_adj]



