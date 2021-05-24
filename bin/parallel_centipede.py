#!/home/yli11/.conda/envs/py2/bin/python
from joblib import Parallel, delayed

import sys
import os
import pandas as pd
import glob
"""


meme opsbed

"""

def get_cutsite(bw,motif):
	command1 = "get_cut_freq_from_bw.py --bed {{motif_id}}/fimo.bed --bw %s -o {{motif_id}}/fimo.cuts.freq.txt -l 100"%(bw)
	# command2 = "run_centipede_parker.R {{motif_id}}/fimo.cuts.freq.txt {{motif_id}}/fimo.bed {{motif_id}}/fimo.png 8"
	os.system(command1.replace("{{motif_id}}",motif))
	# print (command1.replace("{{motif_id}}",motif))
	# os.system(command2.replace("{{motif_id}}",motif))
	# os.system("cd %s;draw_footprint_figure.py"%(motif))
	# os.system("cd %s;run_centipede_multiple_times.py"%(motif))

motif_list = glob.glob("*")
bw = sys.argv[1]
Parallel(n_jobs=10,verbose=10)(delayed(get_cutsite)(bw,m) for m in motif_list)



