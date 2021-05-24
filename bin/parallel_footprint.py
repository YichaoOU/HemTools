#!/home/yli11/.conda/envs/py2/bin/python
from joblib import Parallel, delayed

import sys
import os
import pandas as pd
import glob
import os
import matplotlib
matplotlib.use('agg')
import pandas as pd
import matplotlib.pylab as plt
import argparse
import numpy as np
import sys

"""


meme opsbed

"""
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

def plot_flag(x):
    for i in ['GATA1','PU','CTCF',"NFIX","ZBTB7A","NFY","NFI","LRF"]:
        if i in x.upper():
            return True
    return False

def get_cutsite(bw,motif):
	try:
		command1 = "get_cut_freq_from_bw.py --bed {{motif_id}}/fimo.bed --bw %s -o {{motif_id}}/fimo.cuts.freq.txt -l 100"%(bw)
		os.system(command1.replace("{{motif_id}}",motif))
		# plot
		freq_file = "%s/fimo.cuts.freq.txt"%(motif)
		if os.path.isfile(freq_file):
			df = pd.read_csv(freq_file,sep="\t",header=None)
			freq_list = df.mean().tolist()
			draw_combined_figure(motif,freq_list,df.shape[0])
		
		## for signal plot
		input_list = ["fimo.cuts.freq.txt.filtered_fimo.bed",motif,bw,"cutsites","signal_plot.out"]
		write_file("%s/signal_plot.input"%(motif),"\t".join(input_list))
		signal_plot_sh = ['module purge','module load python/2.7.13','signal_plot.py --figure_type pdf --one_to_one signal_plot.input --computeMatrix_addon_parameters " --binSize 2 --missingDataAsZero " -u 100 -d 100 --plotHeatmap_addon_parameters " --colorList white,red --regionsLabel %s"'%(motif)]
		write_file("%s/signal_plot.sh"%(motif),"\n".join(signal_plot_sh))
		if plot_flag(motif):
			os.system("cd %s; bash signal_plot.sh"%(motif))
	except:
		pass
	
	
def abline2(val):
	"""Plot a line from slope and intercept"""
	axes = plt.gca()
	y_vals = np.array(axes.get_ylim())
	x_vals = [val]*len(y_vals)
	plt.plot(x_vals, y_vals, '--',alpha=0.6,c="grey")

def draw_combined_figure(motif_name,freq_list,num_sites):
	ext_length = 100
	
	cut = len(freq_list)/2
	print ("freq_list:",len(freq_list))
	mlen = float(cut - ext_length)
	plt.figure()
	plt.plot(np.arange(-cut,cut),freq_list)
	plt.xlim(-cut,cut)
	plt.ylim(max(min(freq_list)-1,0),max(freq_list)+1)
	abline2(-mlen/2)
	abline2(mlen/2)
	
	plt.title(motif_name+" | Num sites: %s"%(num_sites))
	plt.ylabel("Cut frequency")
	plt.xlabel("Dist. to motif")
	plt.savefig("%s/%s.footprint.png"%(motif_name,motif_name))

		
	
	
	
motif_list = glob.glob("*")
bw = sys.argv[1]
Parallel(n_jobs=10,verbose=10)(delayed(get_cutsite)(bw,m) for m in motif_list)


