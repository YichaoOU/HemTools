#!/usr/bin/env python

import sys
import os
import argparse
import pandas as pd
import glob
"""calculate PE efficiecny given crisprEsso2_output, amplicon_fasta, sgRNA, start, end, pos, ref, alt

only for SNV

2	grna	strand	rel_pos	ref	alt
0	293Ctrl_HEK3_S1_L001	GGCCCAGACTGAGCACGTGA	NaN	NaN	NaN	NaN
1	293R1_HEK3_S17_L001	GGCCCAGACTGAGCACGTGA	NaN	NaN	NaN	NaN

"""
tab = str.maketrans("ACTG", "TGAC")
def revcomp(seq):
	return seq.translate(tab)[::-1]
		
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument('-f',"--input",  help="tsv 6 columns",required=True)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def append_efficiency(line):

	name = line[0]
	sgRNA = line[1]
	strand = line[2]
	pos = line[3]
	ref = line[4]
	alt = line[5]
	
	
	# start = line[3]+1 # should be 1-index
	# end = line[4]
	# pos = line[5]
	# ref = line[6]
	# alt = line[7]
	# strand = line[8]
	try:
		inFile = glob.glob("%s/*/Nucleotide_percentage_table.txt"%(name))[0]
	except:
		return -1
	try:
		df = pd.read_csv(inFile,sep="\t",index_col=0)
	except:
		return -1
	current_seq = "".join([x.split(".")[0] for x in df.columns])
	if strand == "-":
		sgRNA = revcomp(sgRNA)
	x = current_seq.index(sgRNA)
	# print ("gRNA start pos: ",x)
	# print ("input rel pos: ",pos)
	pos = x+pos
	if current_seq[pos] != ref:
		print (x,current_seq[x:(x+20)])
		print (current_seq[x-10:(x+30)])
		print (sgRNA)
		print ("Error: ref at %s not match"%(pos),current_seq[pos],line)
		# check if crisprEsso will change input amplicon sequence
		exit()

	editing_frequency = df.at[alt,df.columns[pos]]
	return editing_frequency

def minus_control(x,v):
	if "ncd3" in x[0]:
		return x['eff']-v
	return x['eff']
def main():
	args = my_args()
	df = pd.read_csv(args.input,sep="\t",header=None)
	df['eff'] = df.apply(append_efficiency,axis=1)
	# print (args.input)
	# print (df.head())
	df = df.sort_values("eff",ascending=False)
	df.to_csv("editing_efficiency.tsv",sep="\t",header=False,index=False)
	df = df[~df[0].str.contains("K562")]
	control_v = df[df[0]=="293Ctrl_ncd3_S4_L001"]['eff'].tolist()[0]
	df = df[~df[0].str.contains("Ctrl")]
	df = df[~df[0].str.contains("HEK3")]
	df['eff'] = df.apply(lambda x:minus_control(x,control_v),axis=1)
	df['eff'] = df['eff'].replace(-1,0)
	# print (df)
	print (df[[0,6,"eff"]])
	print (df[[6,"eff"]].corr())

if __name__ == "__main__":
	main()

























