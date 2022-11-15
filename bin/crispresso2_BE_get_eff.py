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
try:
	gRNA_column = int(sys.argv[2])
	sample_column = int(sys.argv[3])
	ref=sys.argv[4]
	alt=sys.argv[5]
except:
	gRNA_column = 1
	# gRNA_column = 0
	sample_column = 0
	# sample_column = 5
	ref=sys.argv[2]
	alt=sys.argv[3]
gRNA_list = df[gRNA_column].tolist()
sample_list = df[sample_column].tolist()
# print (sample_list)
# exit()
outfile = "crispresso2_BE.edit_eff.tsv"
outfile2 = "crispresso2_BE.frame_indel.tsv"
outfile4 = "crispresso2_BE.indel_outcome_frequency.tsv"
outfile3 = "crispresso2_BE.indel_outcome_counts.tsv"
outfile5 = "crispresso2_BE.editing_window_frequency.tsv"
outfile6 = "crispresso2_BE.MMEJ.tsv"

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

def parse_allele_freq_table(f):
	# get the total number of bases that is removed or added comparing to WT
	df = pd.read_csv(f,sep="\t")
	df = df[df['Unedited']==False]
	df = df[(df.n_inserted!=0)|(df.n_deleted!=0)] # remove SNPs
	df['total'] = df['n_inserted']-df['n_deleted']
	df['#frame'] = df['total'].apply(lambda x: (abs(x)%3)*np.sign(x))
	# df.to_csv("test.csv")
	Pread = df.groupby("#frame")['%Reads'].sum().to_dict()
	for i in range(-2,3):
		if not i in Pread:
			Pread[i] = 0
	Pread_list = [Pread[0],Pread[1]+Pread[-2],Pread[2]+Pread[-1]]
	Cread = df.groupby("#frame")['#Reads'].sum().to_dict()
	for i in range(-2,3):
		if not i in Cread:
			Cread[i] = 0
	Cread_list = [Cread[0],Cread[1]+Cread[-2],Cread[2]+Cread[-1]]
	return Pread_list+Cread_list

"""
Aligned_Sequence	Reference_Sequence	Unedited	n_deleted	n_inserted	n_mutated	#Reads	%Reads
GTTGGCCAGCCTTGCCTTGACCAATAGCCTTGACAAGGCA	GTTGGCCAGCCTTGCCTTGACCAATAGCCTTGACAAGGCA	TRUE	0	0	0	13347	49.05181918
GTTGGCCAGCCTTGCCTTGA--AATAGCCTTGACAAGGCA	GTTGGCCAGCCTTGCCTTGACCAATAGCCTTGACAAGGCA	FALSE	2	0	0	2329	8.559353179
GTTGGCCAGCCTTGCCTTGA-------------CAAGGCA	GTTGGCCAGCCTTGCCTTGACCAATAGCCTTGACAAGGCA	FALSE	13	0	0	2110	7.754502021
GTTGGCCAGCCTTGCCTTGACCCAATAGCCTTGACAAGGC	GTTGGCCAGCCTTGCCTTGA-CCAATAGCCTTGACAAGGC	FALSE	0	1	0	1812	6.659316428


"""

def parse_allele_freq_table3(f,label):
	"""get individual indel counts or freq

	"""
	df = pd.read_csv(f,sep="\t")
	df['indel'] = df['n_inserted']-df['n_deleted']
	df1 = pd.DataFrame(df.groupby('indel')['#Reads'].sum())
	df2 = pd.DataFrame(df.groupby('indel')['%Reads'].sum())
	df1.columns = [label]
	df2.columns = [label]
	return df1,df2


def window_is_edit(r,ref,alt,gRNA_length,start_pos,window_length,strand="+"):
	# update: fix for 19bp and 21 bp sgRNA
	if strand == "+":
		offset = 20-gRNA_length
		read = r.Aligned_Sequence[10+offset:30]
		gRNA = r.Reference_Sequence[10+offset:30]
	else:
		offset = gRNA_length-20
		read = revcomp(r.Aligned_Sequence[10+offset:30])
		gRNA = revcomp(r.Reference_Sequence[10+offset:30])
	# print (gRNA)
	if read == gRNA:
		return False
	for i in range(start_pos-1,start_pos-1+window_length):
		a = read[i]
		b = gRNA[i]
		if (b == ref) and (a == alt):
			return True
	return False

def parse_allele_freq_table4(f,ref,alt,gRNA,label):
	"""get individual indel counts or freq

	"""
	df = pd.read_csv(f,sep="\t")
	df['is_gRNA'] = [gRNA in x for x in df.Reference_Sequence]
	df2 = df[df.is_gRNA == True]
	strand = "+"
	if df2.shape[0]==0:
		print ("using revcomp of gRNA, please double check the results")
		strand = "-"
	out_columns  = []
	out_values = []
	for start_pos in [1,2,3,4,5]:
		for window_length in [4,5,6,7,8,9,10]:
			name = "%s_%s"%(start_pos,window_length)
			df[name] = df.apply(lambda r:window_is_edit(r,ref,alt,len(gRNA),start_pos,window_length,strand),axis=1)
			out_columns.append(name)
			out_values.append(df[df[name]==True]['%Reads'].sum())
	df = pd.DataFrame(out_values)
	df.index = out_columns
	df.columns = [label]
	return df.T


def find_deletion(x):
    deletion_list = []
    first_char_in_deletion = True
    for i in range(len(x)):
        if x[i] == "-":
            if first_char_in_deletion:
                start = i
                first_char_in_deletion = False
        else:
            if not first_char_in_deletion:
                if start != i-1:   # deletion > 1bp
                    deletion_list.append([start,i-1])
                first_char_in_deletion=True
    return deletion_list            
# find_deletion("aaa-aaa--aaa---aaa----aaaaa--a--a----------a")    
def find_cut_position(pos,ref):
    # print (start,end,ref)
    rel_pos = -1
    for i in range(len(ref)):
        if ref[i]=="-":
            continue
        else:
            rel_pos += 1
        if rel_pos == pos:
            return i
# find_cut_position(153,ref)
# find_deletion("aaa-aaa--aaa---aaa----aaaaa--a--a----------a")    
def is_MMEJ_single(up_stream,deletion_seq,down_stream):
    # case 1
    # print (deletion_seq[0:2],down_stream[0:2])
    if deletion_seq[0:2] == down_stream[0:2]:
        return True
    # case 2
    # print (deletion_seq[-2:] , up_stream[-2:])
    if deletion_seq[-2:] == up_stream[-2:]:
        return True    
    return False

def is_MMEJ(q,ref,cut_pos):
    # all start, end positions are zero-based
    all_deletions = find_deletion(q)
    # print (all_deletions)
    cut_pos = find_cut_position(cut_pos,ref)
    # print (cut_pos)
    all_deletions = [x for x in all_deletions if x[0]-1<=cut_pos<=x[1]+1] # default CRISPResso window size for cas9
    if len(all_deletions)>1:
        print ("something is wrong, more than 2 deletions found around cut position")
    # print (all_deletions[0])
    if len(all_deletions)==0:
        return False
    start,end = all_deletions[0]
    # print (start,end)
    deletion_length = end-start+1
    up_stream = q[start-deletion_length:start]
    deletion_seq = ref[start:start+deletion_length]
    down_stream = q[end+1:end+1+deletion_length]
    # print (up_stream)
    # print (deletion_seq)
    # print (down_stream)
    return is_MMEJ_single(up_stream,deletion_seq,down_stream)  

def get_cut_position(file):
	df2 = pd.read_csv(file,sep="\t")
	return eval(df2['sgRNA_cut_points'][0])[0]

def get_MMEJ_table(file,cut_pos):
	df = pd.read_csv(file,sep="\t")
	df['is_MMEJ'] = df.apply(lambda r:is_MMEJ(r.Aligned_Sequence,r.Reference_Sequence,cut_pos),axis=1)
	outFile = file.replace("Alleles_frequency_table.zip","Alleles_frequency_table.processed.csv")
	df.to_csv(outFile,index=False)
	deletion_df = df[df.n_deleted>0]
	MMEJ = deletion_df[deletion_df.is_MMEJ==True]
	N_MMEJ = MMEJ['#Reads'].sum()
	N_deletion = deletion_df['#Reads'].sum()
	P_MMEJ = N_MMEJ/float(N_deletion)
	TOTAL_indel = df[(df.n_deleted>0)|(df.n_inserted>0)]['#Reads'].sum()
	return [N_MMEJ,N_deletion,P_MMEJ,TOTAL_indel,df['#Reads'].sum()]


'''
out = []
for s in df[sample_column]:
	print (s)
	try:
		edit_file = glob.glob("%s*/CRISPResso_on_*/Nucleotide_percentage_table.txt"%(s))[0]
		gRNA_file = glob.glob("%s*/CRISPResso_on_*/Alleles_frequency_table_around_sgRNA_*"%(s))[0]
	except:
		print ("NOT FOUND",s)
		# print ( glob.glob("%s*/CRISPResso_on_*/Nucleotide_percentage_table.txt"%(s)))
		# exit()
		out.append([-1 for x in range(-16,20,1)])
		continue
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
'''
## indel ##
import traceback
out = []
out2 = []
indel_outcome_counts = []
indel_outcome_freq = []
window_df_list = []
MMEJ_df_list = []

for s in df[sample_column]:
	print (s)
	MMEJ_list=[-1]*5
	try:
		edit_file = glob.glob("%s*/CRISPResso_on_*/Nucleotide_percentage_table.txt"%(s))[0]
		raw_alignment_file = glob.glob("%s*/CRISPResso_on_*/Alleles_frequency_table.zip"%(s))[0]
		info_file = glob.glob("%s*/CRISPResso_on_*/CRISPResso_reference_info.txt"%(s))[0]
		gRNA_file = glob.glob("%s*/CRISPResso_on_*/Alleles_frequency_table_around_sgRNA_*"%(s))[0]
		my_gRNA = gRNA_file.split("Alleles_frequency_table_around_sgRNA_")[-1].replace(".txt","")
		my_revcomp = revcomp(my_gRNA)
		indel_file = glob.glob("%s*/CRISPResso_on_*/CRISPResso_quantification_of_editing_frequency.txt"%(s))[0]
		indel_df = pd.read_csv(indel_file,sep="\t")
		current_out2 = parse_allele_freq_table(gRNA_file)
		indel_counts_df,indel_freq_df = parse_allele_freq_table3(gRNA_file,s)
		window_edit_df = parse_allele_freq_table4(gRNA_file,ref,alt,my_gRNA,s)
		cut_pos = get_cut_position(info_file)
		MMEJ_list = get_MMEJ_table(raw_alignment_file,cut_pos)
		
	except Exception as e:
		print ("NOT FOUND",s)
		traceback.print_exc()
		## IndexError: list index out of range is OK
		out.append([-1 for x in range(-16,20,1)]+[-1])
		out2.append([-1]*7)
		MMEJ_df_list.append(MMEJ_list)
		continue
	Mod = indel_df.at[0,"Modified"]
	only_sub = indel_df.at[0,"Only Substitutions"]
	total = indel_df.at[0,"Reads_aligned"]
	indel_reads = Mod-only_sub
	indel = float(indel_reads)/total
	
	
	if my_gRNA in gRNA_list:
		lines = parse_df(edit_file,my_gRNA,ref,alt)
		out.append(lines+[total,indel_reads,indel])
	elif my_revcomp in gRNA_list:
		print ("using revcomp, result might be incorrect")
		lines = parse_df(edit_file,my_gRNA,revcomp(ref),revcomp(alt))
		out.append(lines+[total,indel_reads,indel])
	else:
		print (my_gRNA,"and its revcomp are not found in the provided gRNA list, skip")
	out2.append(current_out2+[total])
	indel_outcome_counts.append(indel_counts_df)
	indel_outcome_freq.append(indel_freq_df)
	window_df_list.append(window_edit_df)
	MMEJ_df_list.append(MMEJ_list)
df = pd.DataFrame(out)

df.columns = [x+1 for x in range(-16,20,1)]+['Total_Aligned_Reads',"Indel_reads",'indel_rate']
df['sample_id']=sample_list
df['gRNA_list']=gRNA_list
# print (df)
df = df[['sample_id','gRNA_list']+[x+1 for x in range(-16,20,1)]+['Total_Aligned_Reads',"Indel_reads",'indel_rate']]
df = df.fillna(0)
df.to_csv(outfile,sep="\t",index=False)	


df2 = pd.DataFrame(out2)
df2.columns = ['0','+1,-2','+2,-1','RC_0','RC_+1,-2','RC_+2,-1','total_reads']
df2['sample_id']=sample_list
df2['gRNA_list']=gRNA_list
df2 = df2[['sample_id','gRNA_list','0','+1,-2','+2,-1','RC_0','RC_+1,-2','RC_+2,-1','total_reads']]

df2.to_csv(outfile2,sep="\t",index=False)	


indel_outcome_counts = pd.concat(indel_outcome_counts,axis=1).fillna(0)
indel_outcome_freq = pd.concat(indel_outcome_freq,axis=1).fillna(0)
indel_outcome_counts.to_csv(outfile3,sep="\t")
indel_outcome_freq.to_csv(outfile4,sep="\t")

window_edit_df = pd.concat(window_df_list)
window_edit_df.to_csv(outfile5,sep="\t")


# MMEJ

MMEJ_df = pd.DataFrame(MMEJ_df_list)
# print (MMEJ_df)
MMEJ_df.columns = ['N_MMEJ','N_deletion','%MMEJ','total_indel','total reads']
MMEJ_df.index = sample_list
MMEJ_df.to_csv(outfile6,sep="\t")