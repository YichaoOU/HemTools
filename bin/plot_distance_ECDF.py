#!/usr/bin/env python
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pylab as plt
import numpy as np
import scipy
import glob
import sys

def ecdf(data):
	""" Compute ECDF """
	x = np.sort(data)
	n = x.size
	y = np.arange(1, n+1) / float(n)
	return(x,y)

def read_data(f):
	lines = []
	with open(f) as ff:
		for line in ff:
			line = line.strip().split()
			lines.append(np.log10(int(line[-1])+1))
	return lines

df = pd.read_csv(sys.argv[1],sep="\t",header=None)
plt.figure()
for i,r in df.iterrows():
	print (i,r)
	values = read_data(r[0])
	x,y = ecdf(values)
	plt.plot(x,y,label=r[1],linewidth=2, c=r[2],alpha=0.8)
	# plt.plot(x,y,linewidth=2, c='blue',alpha=0.9)
	
plt.legend(loc="lower right")
plt.ylabel("Cumulative Probability")
plt.xlabel("Distance to nearest peak (log10)")	
# plt.title("Top %s %s results"%(n,label))
plt.ylim(0,1)
plt.xlim(-0.1,8)
# plt.savefig("%s_ecdf.png"%(label))
plt.savefig("%s_ecdf.pdf"%(sys.argv[2]), bbox_inches='tight')
