#!/usr/bin/env python
import pysam
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
import glob
from pyfasta import Fasta
from skbio.alignment import StripedSmithWaterman
import re
import itertools
from operator import itemgetter
import os





def correct_read(i):
	# step 1, parse cigar to determine if it is qualified for mapping correction
	df,correction_flag = cigar_tuple_to_df(i,gRNA1,gRNA2)
	new_cigar = i.cigarstring
	swap_flag=False
	# display(df)
	if correction_flag:
		# step 2, get to be corrected sequence
		to_be_corrected_seq = "".join(df[(df[6]==True)&(df[4]!="D")].read_seq.tolist())
		# trim this sequence if the second gRNA is M
		if df[(df[8]==True)&(df[4]=="M")].shape[0]>0:
			# trim_length = df[(df[8]==True)&(df[4]=="M")][1].tolist()[0]-gRNA2+1
			trim_length = df[(df[8]==True)&(df[4]=="M")][1].tolist()[-1]-gRNA2
			
			# print ("trim",trim_length)
			if trim_length>0:
				to_be_corrected_seq = to_be_corrected_seq[:-trim_length]
			
		else:
			trim_length=0
		# print (len(to_be_corrected_seq),to_be_corrected_seq)
		reference_seq = df[(df[7]==True)&(df[4]=="D")].genome_seq.tolist()[0]
		# step 3, align to the beining deleted sequence
		query = StripedSmithWaterman(to_be_corrected_seq)
		if len(to_be_corrected_seq)<100:
			return i
		alignment = query(reference_seq)
		# print (alignment.optimal_alignment_score)
		# display(alignment)
		
		
		# if alignment.query_begin==0 and \
		#	 alignment.query_end == len(to_be_corrected_seq)-1 and \
		#	 alignment.target_begin == 0 and \
		#	 alignment.optimal_alignment_score >=1.5*len(to_be_corrected_seq):
		#	 swap_flag = True
		alignment_cigar = alignment.cigar
		if alignment.optimal_alignment_score >=1.8*len(to_be_corrected_seq):
			# print ("pass")
			swap_flag = True
			if alignment.query_begin>0:
				alignment_cigar = f"{alignment.query_begin}I"+alignment_cigar
			if alignment.query_end <len(to_be_corrected_seq)-1:
				alignment_cigar = alignment_cigar+f"{len(to_be_corrected_seq)-1-alignment.query_end}I"
			if alignment.target_begin>0:
				alignment_cigar =  f"{alignment.target_begin}D"+alignment_cigar
			
			if alignment.query_begin != 0 and alignment.target_begin !=0:
				swap_flag = False
			if alignment.query_begin != 0 and alignment.query_end !=len(to_be_corrected_seq)-1:
				swap_flag = False
		# print (alignment.cigar)
		# print (alignment_cigar)
		if swap_flag:
			# step 4, if alignment is good, update new cigar

			# 1. the new deletion length should be: old_D - new_ref_aligned + old_ref_aligned
			# 2. if the last Match is splitted at the second gRNA cut site, we should update this M, the new size is: second_gRNA_cut to previous end
			# cigar_to_be_deleted = df[(df[6]==True)&(df[4]!="D")].index.tolist()
			cigar_to_be_deleted = df[(df[6]==True)&(df[7]==False)&(df[8]==False)].index.tolist()

			# old_ref_length = len("".join(df[(df[6]==True)&(df[4]!="D")].genome_seq.tolist()))
			old_ref_length = df[(df[6]==True)&(df[7]==False)&(df[8]==False)&(df[4]!="I")][5].sum()
			# print ("first",old_ref_length)
			if df[df[8]==True].shape[0]>=2 and df[df[8]==True][4].tolist()[-1]=="D":
				old_ref_length+=df[(df[8]==True)&(df[4]=="M")][5].sum()
			# print ("first",old_ref_length)
			if trim_length>0:
				old_ref_length+=df[(df[8]==True)&(df[4]=="M")][5].sum()
				old_ref_length = old_ref_length-trim_length
			new_ref_length = alignment.target_end_optimal+1
			# print (old_ref_length,new_ref_length)
			try:
				if df[df[8]==True][4].tolist()[-1]=="M":
					cigar_to_be_modified = df[(df[8]==True)&(df[4]=="M")].index.tolist()[-1]
				else:
					if df[df[8]==True][4].tolist()[-1]=="D":
						last_index = df[df[8]==True].tail(n=1).index.tolist()[0]
						df.at[last_index,6]=False
					cigar_to_be_modified = -1
			except:
				cigar_to_be_modified = -1
			# print ("cigar_to_be_deleted",cigar_to_be_deleted)
			if df[df[8]==True].shape[0]>1:
				cigar_to_be_deleted += list(set(df[(df[6]==True)&(df[7]==False)&(df[4]!="D")].index)-set([cigar_to_be_modified]))
			# print ("cigar_to_be_modified",cigar_to_be_modified)
			# print ("cigar_to_be_deleted",cigar_to_be_deleted)
			gRNA1_D_index = df[(df[6]==True)&(df[4]=="D")].index.tolist()[0]
			
			new_df = df.copy()
			new_df.at[gRNA1_D_index,5] = new_df.at[gRNA1_D_index,5]-(new_ref_length)+old_ref_length
			# print ( new_df.at[gRNA1_D_index,5]-new_ref_length+old_ref_length)
			new_cigar = ""
			for index,row in new_df.iterrows():
				# print (index,row[5],row[4])
				# print (index,gRNA1_D_index,new_cigar)
				if index in cigar_to_be_deleted:
					continue
				if index == cigar_to_be_modified:
					# print ("to be modified",gRNA2-row[0])
					# new_cigar+= f"{row[5]-(gRNA2-row[0]-1)}{row[4]}"
					new_cigar+= f"{row[5]-(gRNA2-row[0])}{row[4]}"
					# print (new_cigar)
				elif index==gRNA1_D_index:
					new_cigar+=alignment_cigar
					new_cigar+= f"{row[5]}{row[4]}"
				else:
					new_cigar+= f"{row[5]}{row[4]}"
			new_cigar = merge_cigar(new_cigar)

	if i.cigarstring!=new_cigar:
		old_l = get_cigar_reference_length(i.cigarstring)
		new_l =get_cigar_reference_length(new_cigar)
		if old_l != new_l:
			print (bam_file)
			print (i.query_name)
			print ("old",i.cigarstring,old_l)
			print ("new",new_cigar,new_l)
			print (cigar_to_be_deleted,cigar_to_be_modified,old_ref_length,new_ref_length)
			print(alignment)
	# print (correction_flag,swap_flag)
	
	i.cigarstring = new_cigar
	
	return i
# merge cigar
def merge_cigar(cigar):
	m = re.findall(r'(\d+)([A-Z]{1})', cigar)
	rebuilt_list = []
	# https://www.appsloveworld.com/pandas/100/126/merge-adjacent-row-based-on-condition
	for cigar_type, length in itertools.groupby(m, itemgetter(1)):
		speaker = cigar_type
		comment_group  = length
		comments = [speaker] # To make sure you have the speaker id as first value
		for comment in comment_group:
			comments.extend([int(comment[0])])
		n=sum(comments[1:])
		if n>0:
			rebuilt_list.append(f"{n}{comments[0]}")
	return "".join(rebuilt_list)   


def cigar_tuple_to_df(read,gRNA1,gRNA2):
	gRNA_range = range(gRNA1,gRNA2+1)
	myList = read.get_aligned_pairs(with_seq=True)
	if read.is_reverse:
		myList = myList[::-1]
	seq = pd.DataFrame(myList)
	read_sequence  = read.query_sequence
	correction_flag = False
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
		if tmp[0]<=gRNA1<=tmp[1]:
			tmp.append(True)
		else:
			tmp.append(False)	
		if tmp[0]<=gRNA2<=tmp[1]:
			tmp.append(True)
		else:
			tmp.append(False)  
			# tmp[-3] = False
		out.append(tmp)
	df = pd.DataFrame(out)
	if df[df[7]==True].shape[0]==0:
		return df,False
	if df[df[7]==True][4].tolist()[0]=="D":
		correction_flag=True
		# print ("asd")
		if df[(df[7]==True)&(df[8]==True)][4].shape[0]>0:
			correction_flag=False
	df['read_seq'] = df.apply(lambda r: read_sequence[r[2]:r[3]],axis=1)
	df['genome_seq'] = df.apply(lambda r: genome['chr11'][r[0]:r[1]].upper(),axis=1)
	return df,correction_flag

def get_cigar_reference_length(cigar):
	m = re.findall(r'(\d+)([A-Z]{1})', cigar)
	total = 0
	for length,t in m:
		if t=="I":
			continue
		total += int(length)
	return total


import sys
bam_file = sys.argv[1]
output = sys.argv[2]


# bam_file = input
# 0-based
gRNA1=5249972 
gRNA2=5254896
chr11="/research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/sequencing/PacBio/220907_SRM279463_amplicon_tsaigrp/Q80_demultiplex/masked_chr11/chr11.fa"
genome = Fasta(chr11)
bam = pysam.AlignmentFile(bam_file, "rb")
# read_list = list(bam.fetch())
outBAM = pysam.AlignmentFile(output, "wb", template=bam)
count = -1
for read in bam.fetch('chr11'):
	count+=1
	if count %10000 == 0:
		print (read.query_name)
		print (count)
	try:
		i = correct_read(read)
		outBAM.write(i)
	except Exception as e:
		print (bam_file,"Failed",read.query_name) 
		print (e)

outBAM.close()

os.system(f"samtools index {output}")