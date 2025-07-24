#!/usr/bin/env python


import pandas as pd
import os
import sys
"""
get gRNA A bed file
"""
gRNA_bed = sys.argv[1]
"""gRNA_bed example, all columns are used expect 5th column
chr19	13215423	13215443	CTATGCGCAAGCCCGTGGCC	0	+
chr6	135501700	135501720	GACATGTGACAATACGACGG	0	+
chr6	135495884	135495904	GCCTGTAATCACAACACTTT	0	+
chr6	135376041	135376061	CGCATGCGCACTGCTGTGCA	0	+
chr19	12983928	12983948	AGTGGCCAAAGGGGGTGGGT	0	+
chr2	58274505	58274525	CGGCTTCTGGGTACCTTCCC	0	-
chr6	135376614	135376634	TCTCACTCACTTTGTCGCCC	0	-
chr19	13207639	13207659	GGCCCGGGCCGGAGCGTGCC	0	+
"""
base = sys.argv[2]
editing_window = sys.argv[3] # 0-index
editing_window = [int(x) for x in editing_window.split(",")]
output = sys.argv[4]
df = pd.read_csv(gRNA_bed,sep="\t",header=None)
def row_apply(x):
	chr = x[0]
	gRNA_start = x[1]
	gRNA_end = x[2]
	gRNA = x[3]
	value = x[4]
	strand = x[5]
	output_list = []
	for i in editing_window:
		if base == gRNA[i]:
			if strand == "-":
				edit_end = gRNA_end-i # 1-index
				edit_start = gRNA_end-(i+1) # 0-index
			if strand == "+":	
				edit_start = gRNA_start+i # 0-index
				edit_end = gRNA_start+i+1 # 1-index
			output_list.append([chr,edit_start,edit_end,gRNA,i+1,strand])
	return output_list		

my_list = df.apply(row_apply,axis=1).tolist()
out_list = []
for x in my_list:
	if x == []:
		continue
	out_list+=x
df = pd.DataFrame(out_list)
print (df.head())
print (df.shape)
# df[6] = df[0]+df[1].astype(str)+df[2].astype(str)
# df = df.drop_duplicates(6)
print (df.shape)
df[[0,1,2,3,4,5]].to_csv(output,sep="\t",header=False,index=False)

