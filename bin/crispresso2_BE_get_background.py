#!/hpcf/apps/python/install/2.7.13/bin/python

# exec(open("crispressoPooled_get_background.py").read())



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

def correct_name(x):
	x = x.replace(":","_")
	x = x.replace(".","_")
	return x
	

def check_header(input_gRNA,table_header_list):
	table_header=[x.split(".")[0] for x in table_header_list]
	table_header = "".join(table_header)
	if not input_gRNA in table_header:
		print ("something is wrong, Exist!")
		exit()
	return table_header.index(input_gRNA)
	
def parse_df(f,gRNA,snp):

	df = pd.read_csv(f,sep="\t",index_col=0)
	my_freq = []
	gRNA_pos = check_header(gRNA,df.columns.tolist())
	bases = df.index.tolist()
	try:
		tmp = snp.loc[gRNA]
		print (tmp)
		flag = True
	except:
		tmp = None
		flag = False
	# print (tmp)
	out = []
	for i in range(-16,20,1):
		amplicon_pos = gRNA_pos+i
		gRNA_pos_1_index = i+1
		column = df.columns[amplicon_pos]
		amplicon_base = column.split(".")[0]
		bases = df.index.tolist()
		ref_base = amplicon_base
		if flag:
			if gRNA_pos_1_index == tmp[1]:
				ref_base = tmp[2]
		bases.remove(ref_base)
		freq = df.loc[bases][column].max() # max background freq
		out.append(freq)
	df = pd.DataFrame(out).T
	df.columns = [x+1 for x in range(-16,20,1)]
	# print (df)
	return df


def parse_df2(f,gRNA,ref,alt,snp):

	df = pd.read_csv(f,sep="\t",index_col=0)
	my_freq = []
	gRNA_pos = check_header(gRNA,df.columns.tolist())
	bases = df.index.tolist()
	try:
		tmp = snp.loc[gRNA]
		print (tmp)
		flag = True
	except:
		tmp = None
		flag = False
	# print (tmp)
	out = []
	for i in range(-16,20,1):
		amplicon_pos = gRNA_pos+i
		gRNA_pos_1_index = i+1
		column = df.columns[amplicon_pos]
		amplicon_base = column.split(".")[0]
		bases = df.index.tolist()
		ref_base = amplicon_base
		if flag:
			if gRNA_pos_1_index == tmp[1]:
				ref_base = tmp[2]
		bases.remove(ref_base)
		if ref_base == ref:
			bases.remove(alt)
		freq = df.loc[bases][column].max() # max background freq
		out.append(freq)
	df = pd.DataFrame(out).T
	df.columns = [x+1 for x in range(-16,20,1)]
	# print (df)
	return df

def parse_snp(f):
	df = pd.read_csv(f,sep="\t",header=None,index_col=0)
	return df


# get the most frequency base conversion for each position


file = "Nucleotide_percentage_table.txt"
import sys
sample_name = sys.argv[1]
input = sys.argv[2]
try:
	SNP = parse_snp(sys.argv[3])
except:
	SNP=None


# SNP = parse_snp("SNP.tsv")
# crispressoPooled_BE_yli11_2020-11-04_info.tsv
output = "%s.max_edit.tsv"%(sample_name)


df = pd.read_csv(input,sep="\t",header=None)
out_df_list = []
name_list = []
gRNA_list = []
for name,_,gRNA in df.values:
	file = "{0}_results/CRISPRessoPooled_on_{0}/CRISPResso_on_{1}/Nucleotide_percentage_table.txt".format(sample_name,correct_name(name))
	# tmp = parse_df(file,gRNA,ref,alt,SNP)
	if not os.path.isfile(file):
		continue
	tmp = parse_df(file,gRNA,SNP)
	out_df_list.append(tmp)
	name_list.append(name)
	gRNA_list.append(gRNA)

out = pd.concat(out_df_list)
out = out*100
out.index = name_list
out['gRNA'] = gRNA_list

out = out[[out.columns[-1]]+out.columns[:-1].tolist()]
out.to_csv(output,sep="\t")
