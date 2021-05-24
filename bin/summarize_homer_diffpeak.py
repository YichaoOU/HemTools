#!/usr/bin/env python

import pandas as pd
import sys

"""

summarize_homer_diffpeak.py wt_p9_pu1_vs_ko_p9_pu1.gain.peak wt_p9_pu1_vs_ko_p9_pu1.loss.peak 1 pu1_diffpeak.bed


output
-------

chr, start, end, gain/loss,p-value,strand

"""


gain_peak = sys.argv[1]
loss_peak = sys.argv[2]
flip = int(sys.argv[3])
out = sys.argv[4]
# FC = 4
# FC = 2
# p_value = 1e-5
FC = float(sys.argv[5])
p_value = float(sys.argv[6])
# p_value = 0.5

def parse_file(f,flip):
	df = pd.read_csv(f,sep="\t",header=None,comment="#")
	# chr,start,end,strand,p-value = 1,2,3,4,10
	df = df[df[9]>=FC]
	df = df[df[10]<=p_value]
	df = df[[1,2,3,0,10,4]]
	df.columns = [0,1,2,3,4,5]
	if flip:
		df[3] = "loss"
	else:
		df[3] = "gain"
	return df
	
df1 = parse_file(gain_peak,flip)
df2 = parse_file(loss_peak,not flip)
df = pd.concat([df1,df2])
df = df.sort_values(4)
df.to_csv(out,sep="\t",header=False,index=False)



