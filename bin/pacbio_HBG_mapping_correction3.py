#!/usr/bin/env python

import pandas as pd
import numpy as np
import scipy
import glob
import sys
import pysam
from pyfasta import Fasta
import os

"""


12/8/2022

In the end, we decided to map the reads to WT and 5kb masked genome.

The reads with higher alignment score will be selected.

The correponding indel will be used.

alignment score from minimap2 need to be recomputed considering donor haplotype.


"""

# parse vcf from GATK

def var_type(r):
	if len(r.ref)==len(r.alt)==1:
		return "SNP"
	if len(r.ref)>len(r.alt):
		return "D"
	if len(r.ref)<len(r.alt):
		return "I"
	return "NA"
def get_var(r):
	if len(r.ref)==len(r.alt)==1:
		return r.alt
	if len(r.ref)>len(r.alt):
		return r.ref[len(r.alt):]
	if len(r.ref)<len(r.alt):
		return r.alt[len(r.ref):]
	return ""	
def parse_vcf_get_known_variants(vcf):
	df = pd.read_csv(vcf,sep="\t",header=None,comment="#")
	df.columns = ['chr','pos','ID','ref','alt','Q','Filter','INFO','format','meta']
	info_strings = '{"' + df.INFO.str.split(';').str.join('","').str.replace('=','":"').str.replace("\"\",", "") + '"}' 
	info_df = pd.json_normalize(info_strings.apply(eval))
	df = pd.concat([df,info_df],axis=1)
	df['var_type'] = df.apply(var_type,axis=1)
	df['var_seq'] = df.apply(get_var,axis=1)
	df.AF = df.AF.astype(float)
	df = df[df.AF>=0.5]
	return df

# calculation alignment score AS

def hamming_distance(chaine1, chaine2):
	return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))
def calculate_AS(r,read_seq,genome_seq):
	if r[4] == "M":
		myLength=len(r[read_seq])
		distance = hamming_distance(r[read_seq],r[genome_seq])
		return myLength-distance+mismatch*distance
	if r[4]=="I" or r[4]=="D":
		if r[read_seq]==r[genome_seq]: # this is for donor haplotype correct sequence
			return 0
		k=max(len(r[read_seq]),len(r[genome_seq]))
		return -min(gap[0]+k*E[0],gap[1]+k*E[1])
	return 0
def get_alternative_sequence(r,read_seq,genome_seq,SNP_dict,insert_dict,deletion_dict):
	if r[4] == "M":
		seq=list(r[genome_seq])
		ref_start = r[0]+1
		for i in range(len(seq)):
			current_pos = ref_start+i
			if current_pos in SNP_dict:
				seq[i] = SNP_dict[current_pos]
		return "".join(seq)
	if r[4]=="I" :
		current_pos = r[0]
		if current_pos in insert_dict:
			if insert_dict[current_pos] == r[read_seq]:
				return r[read_seq]
		return ""
	if r[4]=="D":
		current_pos = r[0]
		if current_pos in deletion_dict:
			if deletion_dict[current_pos] == r[genome_seq]:
				return ""
		return r[genome_seq]
		   
def cigar_tuple_to_df(read,gRNA1,gRNA2,flank,SNP_dict,insert_dict,deletion_dict):
	gRNA_range = range(gRNA1,gRNA2+1)
	# myList = read.get_aligned_pairs(with_seq=True)
	# if read.is_reverse:
		# myList = myList[::-1]
	# seq = pd.DataFrame(myList)
	read_sequence  = read.query_sequence
	if read_sequence == None:
		return pd.DataFrame()
	out = [] # start, end, type, length
	start = read.reference_start
	read_start = 0
	for i in read.cigartuples:
		if i[0] == 0: # M
			tmp = [start,start+i[1],read_start,read_start+i[1],"M",i[1]]
			# out.append(tmp)
			start += i[1]
			read_start += i[1]
			# continue
		elif i[0] == 1:
			indel_length=i[1]
			indel_start = start
			indel_end = start 
			indel_type = "I"
			tmp = [indel_start,indel_end,read_start,read_start+i[1],indel_type,i[1]]
			read_start += i[1]
			# out.append(tmp)
		elif i[0] == 2:
			indel_length=i[1]
			indel_start = start
			start += i[1]
			indel_end = start 
			indel_type = "D"
			tmp = [indel_start,indel_end,read_start,read_start,indel_type,i[1]]
			# out.append(tmp) 
		elif i[0]==4:
			tmp = [start,start,read_start,read_start+i[1],"S",i[1]]
			read_start += i[1]
		elif i[0]==5:
			tmp = [start,start,read_start,read_start+i[1],"H",i[1]]
			read_start += i[1]
		else:
			print ("not considered",read.cigarstring,read.query_name)
		if set(range(tmp[0],tmp[1]+1)).intersection(set(gRNA_range)):
			tmp.append(True)
		else:
			tmp.append(False)
		if tmp[0]-flank<=gRNA1<=tmp[1]+flank:
			tmp.append(True)
		else:
			tmp.append(False)	
		if tmp[0]-flank<=gRNA2<=tmp[1]+flank:
			tmp.append(True)
		else:
			tmp.append(False)			
		out.append(tmp)
	df = pd.DataFrame(out)
	df['read_seq'] = df.apply(lambda r: read_sequence[r[2]:r[3]],axis=1)
	df['genome_seq'] = df.apply(lambda r: genome['chr11'][r[0]:r[1]].upper(),axis=1)
	df['minimap2_score'] = df.apply(lambda r:calculate_AS(r,"read_seq","genome_seq"),axis=1)
	df["known_variant_corrected_sequence"] = df.apply(lambda r:get_alternative_sequence(r,"read_seq","genome_seq",SNP_dict,insert_dict,deletion_dict),axis=1)
	df['variant_correct_alignment_score'] = df.apply(lambda r:calculate_AS(r,"read_seq","known_variant_corrected_sequence"),axis=1)
	return df

def is_valid(read_start,read_end,primer_start,primer_end,flank=1000):
	if primer_start-flank<read_start<primer_start+flank:
		if primer_end-flank<read_end<primer_end+flank:
			return True
	return False

# mapping score used by minimap2, so that we can replicate the alignment score
match = 1
mismatch = -4
# gap=[6,26]
gap=[24,32]
E=[2,1]
# min{O1+k*E1,O2+k*E2}

# genome fasta
chr11="/research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/sequencing/PacBio/220907_SRM279463_amplicon_tsaigrp/Q80_demultiplex/masked_chr11/chr11.fa"
genome = Fasta(chr11)

# HBG parameters
# 1-based
gRNA1=5249973
gRNA2=5254897
flank = 3
primer_start = 5244760
primer_end = 5259510
bam_file_WT = sys.argv[1]
bam_file_MASK = sys.argv[2]
vcf_file = sys.argv[3]
output_prefix = sys.argv[4]


############ MAIN ##################

# print (bam_file_WT,bam_file_MASK,vcf_file,output_prefix)

# 1. read vcf
df = parse_vcf_get_known_variants(vcf_file)
SNP_df = df[df.var_type=="SNP"].set_index("pos")
insert_df = df[df.var_type=="I"].set_index("pos")
deletion_df = df[df.var_type=="D"].set_index("pos")
SNP_dict = SNP_df.var_seq.to_dict()
insert_dict = insert_df.var_seq.to_dict()
deletion_dict = deletion_df.var_seq.to_dict()

# 2. read bam WT
bam = pysam.AlignmentFile(bam_file_WT, "rb")
count=0
# read_list = list(bam.fetch())
out = []
for read in bam.fetch():
	count+=1
	# print (bam_file_WT,read.query_name)
	if count %10000 == 0:
		print ("%s reads processed"%(count))
	df = cigar_tuple_to_df(read,gRNA1,gRNA2,flank,SNP_dict,insert_dict,deletion_dict)
	if df.shape[0]==0:
		continue
	# in this df, we didn't store chromosome, because we only mapped reads to chr11
	read_start = df[0].min()
	read_end = df[1].max()
	read_name = read.query_name
	AS = df.variant_correct_alignment_score.sum()
	df = df[(df[7]==True)|(df[8]==True)]
	df = df[df[4]!="M"]
	if df.shape[0]==0:
		out.append([read_name,read_start,read_end,AS,-1,-1,"M",0])
		continue
	for i,r in df.iterrows():
		out.append([read_name,read_start,read_end,AS,r[0],r[1],r[4],r[5]])
df_WT = pd.DataFrame(out)
df_WT.columns = ['read_name','read_start','read_end','AS','indel_start','indel_end',"indel_type","indel_length"]
df_WT['genome']="WT"
df_WT.to_csv("%s.raw_WT.alginment.csv"%(output_prefix),index=False)

# 2. read bam MASK
bam = pysam.AlignmentFile(bam_file_MASK, "rb")
count=0
# read_list = list(bam.fetch())
out = []
for read in bam.fetch():
	count+=1
	if count %10000 == 0:
		print ("%s reads processed"%(count))
	df = cigar_tuple_to_df(read,gRNA1,gRNA2,flank,SNP_dict,insert_dict,deletion_dict)
	if df.shape[0]==0:
		continue
	# in this df, we didn't store chromosome, because we only mapped reads to chr11
	read_start = df[0].min()
	read_end = df[1].max()
	read_name = read.query_name
	AS = df.variant_correct_alignment_score.sum()
	df = df[(df[7]==True)|(df[8]==True)]
	df = df[df[4]!="M"]
	if df.shape[0]==0:
		out.append([read_name,read_start,read_end,AS,-1,-1,"M",0])
		continue
	for i,r in df.iterrows():
		out.append([read_name,read_start,read_end,AS,r[0],r[1],r[4],r[5]])
df_MASK = pd.DataFrame(out)
df_MASK.columns = ['read_name','read_start','read_end','AS','indel_start','indel_end',"indel_type","indel_length"]
df_MASK['genome']="MASK"
df_MASK.to_csv("%s.raw_MASK.alginment.csv"%(output_prefix),index=False)

# 3. merge
df = pd.concat([df_WT,df_MASK])
# df.to_csv("%s.raw_raw_merged.alginment.csv"%(output_prefix),index=False)

# df.columns = ['read_name','read_start','read_end','AS','indel_start','indel_end',"indel_type","indel_length"]
df.to_csv("%s.raw_merged.alginment.csv"%(output_prefix),index=False)

# Note, a read can only be in one genome
df['filter'] = df["read_name"]+"_"+df["AS"].astype(str)
df2 = df.sort_values("AS",ascending=False)
df2 = df2.drop_duplicates("read_name")
df = df[df['filter'].isin(df2['filter'].tolist())]
df = df.drop(['filter'],axis=1)
df['is_valid']=df.apply(lambda r:is_valid(r['read_start'],r['read_end'],primer_start,primer_end),axis=1)
df = df[df.is_valid==True]
df.to_csv("%s.best_alginment.csv"%(output_prefix),index=False)

# extract bam and merge
WT_list = df[df.genome=="WT"]
WT_list[['read_name']].to_csv("%s.WT.read.list"%(output_prefix),index=False,header=False)
MASK_list = df[df.genome=="MASK"]
MASK_list[['read_name']].to_csv("%s.MASK.read.list"%(output_prefix),index=False,header=False)
# module load samtools/1.12
os.system("samtools view -b -N {0}.WT.read.list {1} > {0}.WT_filtered.bam;samtools index {0}.WT_filtered.bam".format(output_prefix,bam_file_WT))
os.system("samtools view -b -N {0}.MASK.read.list {1} > {0}.MASK_filtered.bam;samtools index {0}.MASK_filtered.bam".format(output_prefix,bam_file_MASK))


# get indel stats
# total_reads = df.read_name.nunique()

