#!/usr/bin/env python

import sys
import os
import argparse
import pandas as pd
import glob
"""calculate PE efficiecny given crisprEsso2_output, amplicon_fasta, sgRNA, start, end, pos, ref, alt

only for SNV

"""
tab = str.maketrans("ACTG", "TGAC")
def revcomp(seq):
	return seq.translate(tab)[::-1]
		
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument('-f',"--input",  help="tsv 5 columns",required=True)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def append_efficiency(line):

	dir = line[0]
	# print ("%s_amplicons.fasta"%(line[0]))
	dir = dir.replace("GTTTTTTCAAAGTAGGCCAC",'TCAAAGTAGGCCACCGGGCC')
	try:
		amplicon_fasta = open("%s_amplicons.fasta"%(dir)).readlines()[-1].strip()
	except:
		print ("%s_amplicons.fasta"%(line[0]))
		return -1
	sgRNA = line[2]

	start = line[3]+1 # should be 1-index
	end = line[4]
	pos = line[5]
	ref = line[6]
	alt = line[7]
	strand = line[8]
	if sgRNA =="GTTTTTTCAAAGTAGGCCAC":
		sgRNA = "TCAAAGTAGGCCACCGGGCC"
		strand = "+"
		start = 158582526
	if strand == "-":
		sgRNA = revcomp(sgRNA)
	try:
		inFile = glob.glob("%s/*/Nucleotide_percentage_table.txt"%(dir))[0]
	except:
		print ("%s/*/Nucleotide_percentage_table.txt"%(dir))
		return -1
	try:
		df = pd.read_csv(inFile,sep="\t",index_col=0)
	except:
		return -1
	current_seq = "".join([x.split(".")[0] for x in df.columns])
	if current_seq != amplicon_fasta:
		print (current_seq)
		print (amplicon_fasta)
		print ("Error: amplicon_seq do not match",line)
		exit()
	## find mutation position
	x = current_seq.index(sgRNA)
	rel_pos = x + pos - start 
	print (rel_pos)
	print (x,current_seq[x:(x+20)])
	if current_seq[rel_pos] != ref:
		print (x,current_seq[x:(x+20)])
		print (current_seq[x-10:(x+30)])
		print (sgRNA)
		print ("Error: ref at %s not match"%(rel_pos),current_seq[rel_pos],line)
		# check if crisprEsso will change input amplicon sequence
		exit()
	# editing_frequency = df.ix[alt,rel_pos]
	print (df.columns[rel_pos],ref,current_seq[rel_pos] )
	editing_frequency = df.at[alt,df.columns[rel_pos]]
	return editing_frequency

def get_name(line):
	dir = line[0]
	start = line[3]+1 # should be 1-index
	end = line[4]
	pos = line[5]
	ref = line[6]
	alt = line[7]
	strand = line[8]
	chr = dir.split("_")[1]
	return "%s:%s-%s"%(chr,pos-1,pos)

def main():
	args = my_args()
	df = pd.read_csv(args.input,sep="\t",header=None)
	df['output'] = df.apply(append_efficiency,axis=1)
	print (df)
	df = df.sort_values("output",ascending=False)
	df['name'] = df.apply(get_name,axis=1)
	df.to_csv(args.input+".editing_efficiency.tsv",sep="\t",header=False,index=False)


if __name__ == "__main__":
	main()

























