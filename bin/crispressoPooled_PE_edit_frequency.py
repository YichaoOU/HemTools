#!/usr/bin/env python

"""
Program to get editing frequency from CrispEsso.

for prime editor.

Given RTT template, calculate subtitution rate

also calculate indel rate

User may want to use subtitution rate for pegRNA and sgRNA type
and indel rate for nickRNA type

supposed to run inside the jobID folder

[yli11@noderome182 crispressoPooled_PE_yli11_2022-09-06]$ ls
24EDIT_results  24UT_results  36EDIT_results  36UT_results  51EDIT_results  51UT_results  BaseE.lsf  email.lsf  log_files

[yli11@noderome182 crispressoPooled_PE_yli11_2022-09-06]$ ls *

24EDIT_results:
CRISPRessoPooled_on_24EDIT  CRISPRessoPooled_on_24EDIT.html

24UT_results:
CRISPRessoPooled_on_24UT  CRISPRessoPooled_on_24UT.html

36EDIT_results:
CRISPRessoPooled_on_36EDIT  CRISPRessoPooled_on_36EDIT.html

36UT_results:
CRISPRessoPooled_on_36UT  CRISPRessoPooled_on_36UT.html

51EDIT_results:
CRISPRessoPooled_on_51EDIT  CRISPRessoPooled_on_51EDIT.html

51UT_results:
CRISPRessoPooled_on_51UT  CRISPRessoPooled_on_51UT.html

padnas >0.23


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
import os
import argparse

def parse_nuc_frequecy_file(f):
	df = pd.read_csv(f,sep="\t",index_col=0)
	table_header=[x.split(".")[0] for x in df.columns.tolist()]
	table_header = "".join(table_header)
	return table_header

def revcomp(seq):
	try: ## python2
		tab = string.maketrans(b"ACTG", b"TGAC")
	except:  ## python3
		tab = bytes.maketrans(b"ACTG", b"TGAC")
	return seq.translate(tab)[::-1]

def correct_name(x):
	x = x.replace(":","_")
	x = x.replace(".","_")
	return x

def process_output(allele_frequency_file,nuc_frequecy_file,gRNA,RTT,cas9_cut):
	df = pd.read_csv(allele_frequency_file,sep="\t")
	ref = parse_nuc_frequecy_file(nuc_frequecy_file)
	reads_total = -1
	is_indel_total = -1
	is_indel_percent = -1
	is_sub_total = -1
	is_sub_percent = -1
	is_crispresso_total = -1
	try:
		gRNA_pos_in_ref=ref.index(gRNA) # 0-index
	except:
		print ("Reference amplicon:",ref)
		print ("gRNA sequence",gRNA)
		print (allele_frequency_file)
		print ("##################failed to locate gRNA##################")
		# return [reads_total,is_indel_total,is_indel_percent,is_sub_total,is_sub_percent,is_crispresso_total]
		return [reads_total,is_indel_total,is_indel_percent,is_sub_total,is_sub_percent]
	df[['is_indel', 'is_sub', 'gRNA_cut_in_aligned','aligned_gRNA']] = df.apply(lambda r:PE_indel_sub(r.Aligned_Sequence,r.Reference_Sequence,gRNA_pos_in_ref,gRNA,RTT,cas9_cut), axis=1, result_type="expand")
	df['CRISPRESSO_indel'] = df.n_deleted+df.n_inserted
	reads_total = df['#Reads'].sum()
	is_indel_total = df[df.is_indel==True]['#Reads'].sum()
	is_indel_percent = df[df.is_indel==True]['%Reads'].sum()
	is_sub_total = df[df.is_sub==True]['#Reads'].sum()
	is_sub_percent = df[df.is_sub==True]['%Reads'].sum()
	is_crispresso_total = df[df.CRISPRESSO_indel>0]['#Reads'].sum() # for debug purpose
	df.to_csv(allele_frequency_file.replace(".zip",".PE.info.csv"),index=False)
	# return [reads_total,is_indel_total,is_indel_percent,is_sub_total,is_sub_percent,is_crispresso_total]
	return [reads_total,is_indel_total,is_indel_percent,is_sub_total,is_sub_percent]


def PE_indel_sub(aligned_read,aligned_ref,gRNA_pos_in_ref,gRNA,RTT,cas9_cut):
	# aligned_read="GTGAAGCCAGC-ACCTCAATTCCTGCCTCCTCAGAAGAGAGAATTTGACCAA"
	# aligned_ref ="GTGAAGCCAGCAACCTCA-TTCCTGCCAGCTCAGAAGAGAGAATTTGACCAA"
	# ref=          "GTGAAGCCAGCAACCTCATTCCTGCCAGCTCAGAAGAGAGAATTTGACCAA"
	# gRNA="AGCAACCTCATTCCTGCCAG"
	# RTT="CTCCTCAGA"
	# cas9_cut=-3
	# aim to get aligned gRNA , aligned RTT, and gRNA_cut_in_aligned

	aligned_gRNA=[]
	aligned_RTT=[]
	gRNA_cut_in_aligned=-1
	
	# make sure gRNA is found in ref
	# try:
		# gRNA_pos_in_ref=ref.index(gRNA) # 0-index
		# to speed up, let user input the index
		# and doing the check outside this function
	# except:
		# print 
	
	aligned_pos=0
	ref_pos=-1
	
	gRNA_end_in_ref = gRNA_pos_in_ref+len(gRNA) # 1-index
	gRNA_cut_in_ref = gRNA_end_in_ref+cas9_cut # 1-index
	gRNA_cut_in_ref_flag = True
	for i in range(len(aligned_ref)):
		if aligned_ref[i]=="-":
			aligned_gRNA.append("-")
		else:
			ref_pos+=1
			if gRNA_end_in_ref>ref_pos>=gRNA_pos_in_ref:
				aligned_gRNA.append(aligned_ref[i])
				if ref_pos==gRNA_cut_in_ref and gRNA_cut_in_ref_flag:
					gRNA_cut_in_ref_flag=False
					gRNA_cut_in_aligned=i
			else:
				aligned_gRNA.append("-")
	# print (gRNA_cut_in_aligned)
	is_indel=False
	is_sub=False # first mismatch
	if "-" in [aligned_gRNA[gRNA_cut_in_aligned-1],aligned_gRNA[gRNA_cut_in_aligned],aligned_read[gRNA_cut_in_aligned-1],aligned_read[gRNA_cut_in_aligned]]:
		is_indel=True

	if not is_indel: # check sub
		for i in range(len(RTT)):
			read_base = aligned_read[gRNA_cut_in_aligned+i]
			ref_base = aligned_ref[gRNA_cut_in_aligned+i]
			RTT_base = RTT[i]
			if ref_base!=RTT_base: # first mismatch, if not the RTT base, this mutation is not caused by PE
				if read_base==RTT_base:
					is_sub=True
					# print (read_base,ref_base,RTT_base,i)
				break
	return is_indel,is_sub,gRNA_cut_in_aligned,''.join(aligned_gRNA)


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output", help="output frequency table (csv)", required=True)

	mainParser.add_argument('-f',"--fastq_tsv",  help="fastq tsv, second column is sample name", required=True)
	mainParser.add_argument('-i','--info',  help="gRNA_info tsv, 3 columns amp name, amp seq, gRNA seq", required=True)
	mainParser.add_argument('-rtt',  help="RTT sequence", required=True)
	mainParser.add_argument('-c','--cas9_cut',  help="cas9_cut", type=int,default=-3)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	df = pd.read_csv(args.fastq_tsv,sep="\t",header=None)
	info = pd.read_csv(args.info,sep="\t",header=None)
	out = []
	for sample in df[1].tolist():
		for i,r in info.iterrows():
			
			site=r[0]
			gRNA=r[2]
			site = correct_name(site)
			line = [sample,site]
			# print (sample,site)
			allele_frequency_file = "{0}_results/CRISPRessoPooled_on_{0}/CRISPResso_on_{1}/Alleles_frequency_table.zip".format(sample,site)
			nuc_frequecy_file = "{0}_results/CRISPRessoPooled_on_{0}/CRISPResso_on_{1}/Nucleotide_frequency_table.txt".format(sample,site)
			line += process_output(allele_frequency_file,nuc_frequecy_file,gRNA,args.rtt,args.cas9_cut)
			out.append(line)
			print (line)
	df = pd.DataFrame(out)
	# df.columns = ['sample','site',"reads_total","is_indel_total","is_indel_percent","is_sub_total","is_sub_percent","is_crispresso_total"]
	df.columns = ['sample','site',"reads_total","is_indel_total","is_indel_percent","is_sub_total","is_sub_percent"]
	df.to_csv(args.output,index=False)
if __name__ == "__main__":
	main()


