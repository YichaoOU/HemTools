#!/hpcf/apps/python/install/2.7.13/bin/python

# exec(open("CRISPRessoWGS_get_background.py").read())



"""
Program to get average editing frequency from CrispEsso.
"""

import matplotlib
import pandas as pd
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import string
import sys
import glob
import numpy as np
import os
import pandas as pd
import sys
import matplotlib
matplotlib.use('agg')
import os
import matplotlib as mpl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import argparse
import datetime
import getpass
import uuid
from scipy.interpolate import interp1d
import re, string
import matplotlib.colors as pltcolors



def revcomp(seq):
	try: ## python2
		tab = string.maketrans(b"ACTG", b"TGAC")
	except:  ## python3
		tab = bytes.maketrans(b"ACTG", b"TGAC")
	return seq.translate(tab)[::-1]

def check_header(input_gRNA,table_header_list):
	table_header=[x.split(".")[0] for x in table_header_list]
	table_header = "".join(table_header)
	if not input_gRNA in table_header:
		print ("something is wrong, Exist!")
		exit()
	return table_header.index(input_gRNA)
	

def parse_df(f,gRNA,my_conversion,snp):
	bases = ["A",'G','C','T']
	df = pd.read_csv(f,sep="\t",index_col=0)
	my_freq = []
	gRNA_pos = check_header(gRNA,df.columns.tolist())
	try:
		tmp = snp.loc[gRNA]
		# print (tmp)
		flag = True
	except:
		tmp = None
		flag = False
	# print (tmp)
	out = []
	
	for i in range(-1,20,1):
		pos = gRNA_pos+i
		column = df.columns[pos]
		base = column.split(".")[0]
		# print (i+1)
		if flag:
			if i+1 == tmp[1]:
				base = tmp[2]
		line = ["%s|%s"%(i+1,base)]
		column_names = []
		for i in range(len(my_conversion)):
			
			b = bases[i]
			others = my_conversion[i]
			column_names += ["%s->%s"%(b,o) for o in others]
			if b == base:
				for j in others:
					freq = df.at[j,column]
					line.append(freq)
			else:
				line += [0]*3

		out.append(line)
	df = pd.DataFrame(out)
	
	df.index = df[0].tolist()
	df = df.drop([0],axis=1)
	df.columns = column_names
	# print (df)
	# df.to_csv("test.tsv",sep="\t")
	return df

def correct_name(x):
	x = x.replace(":","_")
	x = x.replace(".","_")
	return x
	

def parse_indel(f):
	df = pd.read_csv(f,sep="\t",index_col=0)
	df['total_indel'] = df[['Deletions','Insertions']].sum(axis=1)
	df['indel_frequency'] = df['total_indel']/(df['Reads_total'])
	df = df.fillna(-1)
	return df
def parse_snp(f):
	df = pd.read_csv(f,sep="\t",header=None,index_col=0)
	return df

def plot_df(df,plot_filename):

	cm = ['Blues', 'Blues', 'Reds', 'Greys', 'Greys']
	cm = ["Reds"]*3+["Blues"]*3+["Greens"]*3+["Oranges"]*3
	f, axs = plt.subplots(1, df.columns.size, gridspec_kw={'wspace': 0})
	for i, (s, a, c) in enumerate(zip(df.columns, axs, cm)):
		# print (i,s, a, c)
		# print (df[s])
		sns.heatmap(np.array([df[s].values]).T, yticklabels=df.index, xticklabels=[s], annot=True, fmt='.2f', ax=a, cmap=c, cbar=False,vmin=0,vmax=0.9)
		if i>0:
			a.yaxis.set_ticks([])
	f.set_figheight(15)
	f.set_figwidth(10)
	f.savefig(plot_filename,bbox_inches='tight')

import sys
sample_name = sys.argv[1]
input = sys.argv[2]
try:
	SNP = parse_snp(sys.argv[3])
except:
	SNP=None

bases = ["A",'G','C','T']
my_conversion = []
for i in range(len(bases)):
	current = ["A",'G','C','T']
	b = bases[i]
	current.remove(b)
	my_conversion.append(current)

# SNP = parse_snp("SNP.tsv")
# CRISPRessoWGS_BE_yli11_2020-11-04_info.tsv


df = pd.read_csv(input,sep="\t",header=None)
out_df_list = []

for name,_,gRNA in df.values:
	file = "{0}_results/CRISPRessoWGS_on_{0}/CRISPResso_on_{1}/Nucleotide_percentage_table.txt".format(sample_name,correct_name(name))
	# get df
	if not os.path.isfile(file):
		continue
	tmp = parse_df(file,gRNA,my_conversion,SNP)
	tmp =tmp *100
	# save df
	tmp.to_csv("{0}_results/{1}.all_conversion.tsv".format(sample_name,name),sep="\t")
	# plot df
	plot_df(tmp,"{0}_results/{1}.all_conversion.pdf".format(sample_name,name))






# file = "Nucleotide_percentage_table.txt"
# gRNA="TTCTCCTCAGGAGTCAGATG"
# SNP = parse_snp("SNP.tsv")




# df = parse_df(file,gRNA,ref,alt,SNP)
# plot_df(df,"test.pdf")