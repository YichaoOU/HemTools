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

def append_efficiency(f):


	df = pd.read_csv(f,sep="\t",index_col=0)
	if df.shape[0]<=1:
		return [f.split("/")[0],-1]
	total_aligned = df.Reads_aligned_all_amplicons.tolist()[0]
	HDR_results = df.at['HDR','Reads_aligned']
	return [f.split("/")[0],float(HDR_results)/total_aligned]


def main():
	files = glob.glob("*/*/CRISPResso_quantification_of_editing_frequency.txt")
	df = [append_efficiency(f) for f in files]
	df = pd.DataFrame(df)
	df.to_csv("HDR_eff.tsv",sep="\t",header=False,index=False)

if __name__ == "__main__":
	main()

