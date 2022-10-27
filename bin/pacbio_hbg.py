#!/usr/bin/env python

import pandas as pd
import sys
import os
import argparse
import pysam
def parse_read_cigar(read):
	read_start = read.reference_start+1 # becomes 1-based
	out = []
	for i in read.cigartuples:
		if i[0] == 0:
			read_start += i[1]
			continue
		elif i[0] == 1:
			indel_length=i[1]
			indel_start = read_start
			indel_end = read_start 
			indel_type = "insertion"
		elif i[0] == 2:
			indel_length=i[1]
			indel_start = read_start
			read_start += i[1]
			indel_end = read_start 
			indel_type = "deletion"
		elif i[0]==4:
			continue
		elif i[0]==5:
			continue
		else:
			print ("not considered",read.cigarstring,read.query_name)
		out.append([indel_type,read.reference_name,indel_start,indel_end,indel_length])
	if out == []:
		out = [["",read.reference_name,-1,-1,-1]]
	return out

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output_label", help="output_label, raw read stats, and summary stats, csv", required=True)

	mainParser.add_argument('-f',"--input",  help="bam file from minimap2",required=True)
	mainParser.add_argument("--left_primer_start",  help="left_primer_start",default=5244000,type=int)
	mainParser.add_argument("--left_primer_end",  help="left_primer_end",default=5246000,type=int)
	mainParser.add_argument("--right_primer_start",  help="right_primer_start",default=5259000,type=int)
	mainParser.add_argument("--right_primer_end",  help="right_primer_end",default=5259800,type=int)


	mainParser.add_argument("--gRNA1_cut_pos",  help="gRNA1_cut_pos",default=5249973,type=int)
	mainParser.add_argument("--gRNA2_cut_pos",  help="gRNA2_cut_pos",default=5254897,type=int)
	mainParser.add_argument("--gRNA_cut_flank",  help="gRNA_cut_flank",default=5,type=int)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()

	# r_start_range = [args.left_primer_start,args.left_primer_end]
	# r_end_range = [5259000,5259800]
	# flank = 6
	# g34_1_range = [5249973-flank,5249973+flank]
	# g34_2_range = [5254897-flank,5254897+flank]

	r_start_range = [args.left_primer_start,args.left_primer_end]
	r_end_range = [args.right_primer_start,args.right_primer_end]
	flank = args.gRNA_cut_flank
	g34_1_range = [args.gRNA1_cut_pos-flank,args.gRNA1_cut_pos+flank]
	g34_2_range = [args.gRNA2_cut_pos-flank,args.gRNA2_cut_pos+flank]
	# """
	bam = pysam.AlignmentFile(args.input, "rb")

	# read_list = list()

	out = []
	for r in bam.fetch():
		tmp = [r.query_name,r.reference_start+1,r.reference_end]
		for x in parse_read_cigar(r):
			out.append(tmp+x)
	df = pd.DataFrame(out)	   	
	def is_valid(r):
		if r_start_range[0]<r[1]<r_start_range[1]:
			if r_end_range[0]<r[2]<r_end_range[1]:
				return True
		return False
	df['is_valid'] = df.apply(is_valid,axis=1)
	def is_edit(r):
		if set(range(*g34_1_range)).intersection(set(range(r[5],r[6]))):
			return True
		if set(range(*g34_2_range)).intersection(set(range(r[5],r[6]))):
			return True
		# if g34_1_range[0]<r[5]<g34_1_range[1]:
			# return True
		# if g34_2_range[0]<r[5]<g34_2_range[1]:
			# return True
		# if g34_1_range[0]<r[6]<g34_1_range[1]:
			# return True
		# if g34_2_range[0]<r[6]<g34_2_range[1]:
			# return True
		return False
	df['is_edit'] = df.apply(is_edit,axis=1)
	df.to_csv(f"{args.output_label}.read_stats.csv",index=False)
	# """
	df = pd.read_csv(f"{args.output_label}.read_stats.csv")
	df.columns = [0,1,2,3,4,5,6,7,"is_valid","is_edit"]
	total_reads = df[0].nunique()
	# print (df.head())
	print (df[4].unique())
	
	invalid_read_list = list(set(df[df.is_valid==False][0].tolist()))
	df2 = df[~df[0].isin(invalid_read_list)]
	N_valid = df2[0].nunique()
	# print (df2[4].unique())
	# print (df2[df2[4].isnull()])
	# df2[4] = [x.split("_")[0] for x in df2[4]] # specifically for chr11_ori and chr11_SNP
	edited_reads = list(set(df2[df2.is_edit==True][0].tolist()))
	total_indel_frequency = len(edited_reads)/N_valid
	
	df3 = df2[df2[0].isin(edited_reads)][df2.is_edit==True]
	df3 = df3.sort_values(7,ascending=False) # for each read, if it has multiple indel surounding gRNA, keep the longest
	df3 = df3.drop_duplicates(0)

	df4 = pd.DataFrame(df3.groupby([4,5,6]).size()).reset_index()
	df4 = df4.sort_values(0,ascending=False)
	df4['deletion_length'] = df4[6]-df4[5]
	df4['frequency'] = df4[0]/N_valid
	df4.columns = ['chr','start','end','read_count','deletion_length','frequency']
	df4.to_csv(f"{args.output_label}.read_indel.csv",index=False)
	large_deletion = df4[df4.deletion_length.between(4900,5100)].frequency.sum()
	print (args.output_label,total_reads,N_valid,total_indel_frequency,large_deletion)


if __name__ == "__main__":
	main()


















