#!/usr/bin/env python

import sys
import os
import argparse
import pandas as pd
import glob
import string
"""calculate PE efficiecny given crisprEsso2_output (label), sgRNA, RTT



"""
def revcomp(seq):
	try: ## python2
		tab = string.maketrans(b"ACTG", b"TGAC")
	except:  ## python3
		tab = bytes.maketrans(b"ACTG", b"TGAC")
	return seq.translate(tab)[::-1]


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument('-f',"--input",  help="tsv 3 columns",required=True)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def find_eff(df,ref,alt,index):
	count = 0
	eff = -1
	for i in range(len(ref)):
		ref_base = ref[i]
		alt_base = alt[i]
		if alt_base != ref_base:
			count += 1
			eff = df.at[alt_base,df.columns[index+i]]
	if count != 1:
		print ("something is wrong")
		eff = -1
	return eff

def append_efficiency(name,sgRNA,RTT):


	try:
		inFile = glob.glob("%s/*/Nucleotide_percentage_table.txt"%(name.replace(".fastq.gz","")))[0]
	except:
		return -1
	try:
		df = pd.read_csv(inFile,sep="\t",index_col=0)
	except:
		return -1
	current_seq = "".join([x.split(".")[0] for x in df.columns])
	
	gRNA_revcomp = revcomp(sgRNA)
	print (name,sgRNA,RTT)
	print (current_seq)
	print (df.head())
	try:
		gRNA_start = current_seq.index(sgRNA)
	except:
		gRNA_start = -1
	try:
		gRNA_revcomp_start = current_seq.index(gRNA_revcomp)
	except:
		gRNA_revcomp_start = -1
	
	if gRNA_start == -1 and gRNA_revcomp_start == -1:
		print ("gRNA not found for:",name)
		exit()
	if gRNA_start != -1 and gRNA_revcomp_start != -1:
		print ("gRNA and its revcomp are found:",name)
		print ("This might cause error, exit!")
		exit()
	
	if gRNA_start > -1:
		RTT_revcomp = revcomp(RTT)
		RTT_start_pos = gRNA_start + len(sgRNA) - 3
		ref = current_seq[RTT_start_pos:RTT_start_pos+len(RTT_revcomp)]
		eff = find_eff(df,ref,RTT_revcomp,RTT_start_pos)
	if gRNA_revcomp_start > -1:

		RTT_start_pos = gRNA_revcomp_start + 3-len(RTT)
		ref = current_seq[RTT_start_pos:RTT_start_pos+len(RTT)]
		eff = find_eff(df,ref,RTT,RTT_start_pos)

	return eff


def main():
	args = my_args()
	df = pd.read_csv(args.input,sep="\t",header=None)
	df['eff'] = df.apply(lambda r:append_efficiency(r[0],r[1],r[2]),axis=1)
	df.to_csv("SNV_editing_efficiency.tsv",sep="\t",header=False,index=False)

if __name__ == "__main__":
	main()

