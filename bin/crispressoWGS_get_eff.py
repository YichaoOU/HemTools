#!/hpcf/apps/python/install/2.7.13/bin/python





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

def correct_name(x):
	x = x.replace(":","_")
	x = x.replace(".","_")
	return x
	
	
def revcomp(seq):
	try: ## python2
		tab = string.maketrans(b"ACTG", b"TGAC")
	except:  ## python3
		tab = bytes.maketrans(b"ACTG", b"TGAC")
	return seq.translate(tab)[::-1]

def check_header(input_gRNA,table_header_list):
	# update: get starting column id
	table_header=[x.split(".")[0] for x in table_header_list]
	table_header = "".join(table_header)
	if input_gRNA in table_header:
		start = table_header.index(input_gRNA)
		return start+1,start+len(input_gRNA)
	else:
		print ("gRNA %s not found, Exist!"%(input_gRNA))
		exit()
def check_header2(input_gRNA,table_header_list):
	table_header=[x.split(".")[0] for x in table_header_list]
	table_header = "".join(table_header)
	if input_gRNA != table_header:
		print ("something is wrong, Exist!")
		exit()
	

def parse_df(f,gRNA,ref,alt,snp):
	### update: use all amplcion df
	df = pd.read_csv(f,sep="\t",index_col=0)
	# print (f)
	# print (df.head())
	my_freq = []
	start,end = check_header(gRNA,df.columns.tolist())
	try:
		tmp = snp.loc[gRNA]
		print (tmp)
		flag = True
	except:
		tmp = None
		flag = False
	
	count = 1
	n_th_column = 0
	check_gRNA = []
	for c in df.columns:
		n_th_column+= 1
		if start<=n_th_column<=end:
			base = c.split(".")[0]
			check_gRNA.append(base)
			if flag:
				if count == tmp[1]:
					base = tmp[2]
			freq = 0
			if base == ref:
				freq = df.at[alt,c]
				my_freq.append(freq)
			else:
				my_freq.append(freq)
			count += 1
	if "".join(check_gRNA) != gRNA:
		print ("gRNA not match!")
		exit()
	return my_freq
	
def parse_df2(f,gRNA,ref,alt,snp):

	df = pd.read_csv(f,sep="\t",index_col=0)
	# print (f)
	# print (df.head())
	my_freq = []
	check_header(gRNA,df.columns.tolist())
	try:
		tmp = snp.loc[gRNA]
		print (tmp)
		flag = True
	except:
		tmp = None
		flag = False
	
	count = 1
	for c in df.columns:
		base = c.split(".")[0]
		if flag:
			if count == tmp[1]:
				base = tmp[2]
		freq = 0
		if base == ref:
			freq = df.at[alt,c]
			my_freq.append(freq)
		else:
			my_freq.append(freq)
		count += 1
	return my_freq
	
def parse_indel(f):
	df = pd.read_csv(f,sep="\t",index_col=0)
	cols=["Only Insertions","Only Deletions","Insertions and Deletions","Insertions and Substitutions","Deletions and Substitutions","Insertions Deletions and Substitutions"]
	df['total_indel'] = df[cols].sum(axis=1)
	df['indel_frequency'] = df['total_indel']/(df['Reads_total'])
	df = df.fillna(-1)
	return df
def parse_snp(f):
	df = pd.read_csv(f,sep="\t",header=None,index_col=0)
	return df

sample_id_list = [sys.argv[1]]
df = pd.read_csv(sys.argv[2],sep="\t",header=None)
ref=sys.argv[3]
alt=sys.argv[4]

try:
	SNP = parse_snp(sys.argv[5])
except:
	SNP=None


for s in sample_id_list:
	outfile = {}
	outfile[18] = "%s.18.edit_eff.tsv"%(s)
	outfile[19] = "%s.19.edit_eff.tsv"%(s)
	outfile[20] = "%s.20.edit_eff.tsv"%(s)
	outfile[21] = "%s.21.edit_eff.tsv"%(s)
	outfile[22] = "%s.22.edit_eff.tsv"%(s)
	out = {}
	out[18] = []
	out[19] = []
	out[20] = []
	out[21] = []
	out[22] = []
	index_list = {}
	index_list[18] = []
	index_list[19] = []
	index_list[20] = []
	index_list[21] = []
	index_list[22] = []
	count = 0
	for name,_,gRNA in df.values:
		# file = "{0}_results/CRISPRessoWGS_on_{0}/CRISPResso_on_{1}/Quantification_window_nucleotide_percentage_table.txt".format(s,name)
		file = "{0}_results/CRISPRessoWGS_on_{0}/CRISPResso_on_{1}/Nucleotide_percentage_table.txt".format(s,correct_name(name))
		myLength = len(gRNA)
		# print (name,_,gRNA)
		if os.path.isfile(file):
			freq = parse_df(file,gRNA,ref,alt,SNP)
		else:
			freq = [-1]*len(gRNA)
		out[myLength].append([gRNA]+freq)
		index_list[myLength].append(count)
		count+=1
	# SAMPLES_QUANTIFICATION_SUMMARY.txt
	file = "{0}_results/CRISPRessoWGS_on_{0}/SAMPLES_QUANTIFICATION_SUMMARY.txt".format(s)
	df2 = parse_indel(file)
	for k in out:
		if len(out[k])==0:
			continue
		
		tmp = pd.DataFrame(out[k])
		tmp.index = df.loc[index_list[k]][0].tolist()
		tmp[['indel_frequency','total_indel','Reads_total']]=df2[['indel_frequency','total_indel','Reads_total']]
		tmp.to_csv(outfile[k],sep="\t")
	
'''
	
for s in sample_id_list:
	outfile = "%s.edit_eff.tsv"%(s)
	out = []
	for name,_,gRNA in df.values:
		file = "{0}_results/CRISPRessoWGS_on_{0}/CRISPResso_on_{1}/Quantification_window_nucleotide_percentage_table.txt".format(s,name)
		if os.path.isfile(file):
			freq = parse_df(file,gRNA,ref,alt,SNP)
		else:
			freq = [-1]*len(gRNA)
		out.append([gRNA]+freq)
	# SAMPLES_QUANTIFICATION_SUMMARY.txt
	file = "{0}_results/CRISPRessoWGS_on_{0}/SAMPLES_QUANTIFICATION_SUMMARY.txt".format(s)
	df2 = parse_indel(file)
	
	out = pd.DataFrame(out)
	out.index = df[0].tolist()
	out[['indel_frequency','total_indel','Reads_total']]=df2[['indel_frequency','total_indel','Reads_total']]
	out.to_csv(outfile,sep="\t")
	
'''