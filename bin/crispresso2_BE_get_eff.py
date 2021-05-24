#!/hpcf/apps/python/install/2.7.13/bin/python




"""

[yli11@nodecn125 crispresso2_BE_yli11_2020-11-22]$ crispresso2_BE_get_eff.py ../input2.list A G
[yli11@nodecn125 crispresso2_BE_yli11_2020-11-22]$ pwd
/research/rgs01/project_space/chenggrp/blood_regulome/chenggrp/Sequencing_runs/chenggrp_targeted_deep_sequencing_112020/crispresso2_BE_yli11_2020-11-22
[yli11@nodecn125 crispresso2_BE_yli11_2020-11-22]$ 



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


def revcomp(seq):
	try: ## python2
		tab = string.maketrans(b"ACTG", b"TGAC")
	except:  ## python3
		tab = bytes.maketrans(b"ACTG", b"TGAC")
	return seq.translate(tab)[::-1]

def check_header(input_gRNA,table_header_list):
	table_header=[x.split(".")[0] for x in table_header_list]
	table_header = "".join(table_header)
	if input_gRNA != table_header:
		print ("something is wrong, Exist!")
		exit()
	

def parse_df(f,gRNA,ref,alt,snp):

	df = pd.read_csv(f,sep="\t",index_col=0)
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
	df['total_indel'] = df[['Deletions','Insertions']].sum(axis=1)
	df['indel_frequency'] = df['total_indel']/(df['Reads_total'])
	df = df.fillna(-1)
	return df
def parse_snp(f):
	df = pd.read_csv(f,sep="\t",header=None,index_col=0)
	return df

def get_amp_seq(f):
	seq = open(f).readlines()[-1]
	return seq.strip()

## input list
# first col: sample ID
# second col: gRNA

# ref, alt

df = pd.read_csv(sys.argv[1],sep="\t",header=None)
gRNA_list = df[1].tolist()
sample_list = df[0].tolist()
ref=sys.argv[2]
alt=sys.argv[3]
outfile = "crispresso2_BE.edit_eff.tsv"

def check_header(input_gRNA,table_header_list):
    table_header=[x.split(".")[0] for x in table_header_list]
    table_header = "".join(table_header)
    if not input_gRNA in table_header:
        gRNA_rev = revcomp(input_gRNA)
        
        if not gRNA_rev in table_header:
            print (gRNA_rev,"something is wrong, Exist!")
            exit()
        return table_header.index(gRNA_rev),"-"
    return table_header.index(input_gRNA),"+"

def parse_df(f,gRNA,ref,alt):

    df = pd.read_csv(f,sep="\t",index_col=0)
    my_freq = []
    gRNA_pos,strand = check_header(gRNA,df.columns.tolist())
    out = []
    if strand == "+":
        for i in range(-16,20,1):
            amplicon_pos = gRNA_pos+i
            column = df.columns[amplicon_pos]
            amplicon_base = column.split(".")[0]
            if amplicon_base == ref:
                freq = df.at[alt,column]
            else:
                freq = np.nan
            out.append(freq)
        return out
    else:
        ref = revcomp(ref)
        alt = revcomp(alt)
        for i in range(36):
            amplicon_pos = gRNA_pos+i
            column = df.columns[amplicon_pos]
            amplicon_base = column.split(".")[0]
            if amplicon_base == ref:
                freq = df.at[alt,column]
            else:
                freq = np.nan
            out.append(freq)
        return out[::-1]



out = []
for s in df[0]:
	try:
		edit_file = glob.glob("%s*/CRISPResso_on_*/Nucleotide_percentage_table.txt"%(s))[0]
		gRNA_file = glob.glob("%s*/CRISPResso_on_*/Alleles_frequency_table_around_sgRNA_*"%(s))[0]
	except:
		print (s)
		print ( glob.glob("%s*/CRISPResso_on_*/Nucleotide_percentage_table.txt"%(s)))
		exit()
	my_gRNA = gRNA_file.split("Alleles_frequency_table_around_sgRNA_")[-1].replace(".txt","")
	my_revcomp = revcomp(my_gRNA)
	if my_gRNA in gRNA_list:
		lines = parse_df(edit_file,my_gRNA,ref,alt)
		out.append(lines)
	elif my_revcomp in gRNA_list:
		print ("using revcomp, result might be incorrect")
		lines = parse_df(edit_file,my_gRNA,revcomp(ref),revcomp(alt))
		out.append(lines)
	else:
		print (my_gRNA,"and its revcomp are not found in the provided gRNA list, skip")
	
df = pd.DataFrame(out)
df.columns = [x+1 for x in range(-16,20,1)]
df['sample_id']=sample_list
df['gRNA_list']=gRNA_list
df = df[['sample_id','gRNA_list']+[x+1 for x in range(-16,20,1)]]
df = df.fillna(0)
df.to_csv(outfile,sep="\t",index=False)	
