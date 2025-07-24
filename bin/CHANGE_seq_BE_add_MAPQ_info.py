#!/usr/bin/env python

import pandas as pd
import numpy as np
import scipy.stats as sts
import gzip as gz
import pysam
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
import glob
from joblib import Parallel, delayed
import sys
import argparse
import plotly.express as px
import plotly.io as pio
import os
from Bio.Seq import Seq
from Bio import SeqIO
import swifter
import sys
import plotly.express as px
from Levenshtein import distance

label=sys.argv[1]

file=f"{label}_identified_matched.txt"
df = pd.read_csv(file,sep="\t")
read = pd.read_csv(f"{label}.PE.read_stats.csv")
mapq = pd.read_csv(f"{label}.mapq.tsv",sep="\t",index_col=0)
c="Genomic Coordinate"

def get_overlap_second_start_position(r):
	"""original change-seq code only save read start, but we really need the overlap start"""
	if r.strand1=="+":
		return r.pos1+r.overlap_bp-1
	else:
		return r.pos2+r.overlap_bp-1	
def get_read_list(r,mid,flank):
	if r.strand1=="+":
		pos = r.pos1+r.overlap_bp/2
	else:
		pos = r.pos2+r.overlap_bp/2
	if mid-flank-10<=pos<=mid+flank+10: # mid-10 is gRNA start, mid + 10 is gRNA end, capture read overlap with off-target region
		return True
	return False
def get_distance_to_overlap_end(r):
	myList = r.converted_pos_list
	if r.strand1=="+":
		pos1 = r.pos1
		pos2 = r.second_overlap_start
	else:
		pos1 = r.pos2
		pos2 = r.second_overlap_start
	out = []
	for i in myList:
		out.append(min(abs(pos1-i),abs(pos2-i)))
	return out   
def get_AG_vector(read,OT_name,chr,start,end,seq,strand,RC,flank=30):
	# output frequency of A-G for each position
	# chr="chr15"
	# start = 57472645
	# end = 57472669
	# strand = "-"
	# seq="TTCTCCACAGGAGTCAGGAGAGAC"
	# RC=780
	# get_AG_vector(read,chr,start,end,seq,strand,RC,flank=50)
	out = {}
	# read belongs to this site
	start = start+1
	q = read[read.chr==chr]
	q = q[q.is_outie==True]
	mid = int((start+end)/2)
	q["is_site"] = q.apply(lambda r:get_read_list(r,mid,flank),axis=1)
	q["second_overlap_start"] = q.apply( get_overlap_second_start_position
,axis=1)
	q = q[q.is_site==True]
	q = q.sort_values("pos1")
	q = q[q.overlap_bp>=0]
	q = q[q.overlap_bp<=20]
	total_N = q.shape[0]
	q['MAPQ'] = q.read.apply(lambda x:mapq.at[x,'mapq'])
	if total_N!=RC/2:
		if abs(total_N-RC/2)>=1: # differ by at least 1 reads. The pipeline counts each pair as two reads and uses the read start to count off-targets. Depending on the overlap length, the two read starts for the same pair might not counted toward the same window_seq (which is used to find off-targets and assign counts). 
		# e.g., chr18	78437551	78437575 is a repeat region.
		# e.g. https://ppr.stjude.org/?study=HemPipelines/yli11/create_tracks_yli11_2024-02-142268e316c90d/tracks.json, chr3:187997273-187997371, NB551526:165:H2FWWAFX3:1:11108:19724:14749	chr3	187997290	-	187997337	+	True	13. This pair has >10bp overlap, one end is the off-target window_seq, the other end is not because 10bp without any signal will create a new window bin by our pipeline.
			print (chr,start,end,seq,RC,total_N,"NOT MATCH")
			q.to_csv(f"{OT_name}_{RC}_{total_N}.NOT_MATCH.csv")
	# q = q[q.converted_pos_list!="[]"]
	if q.shape[0]==0: # no converted reads
		out={}
		out['total_AG_frequency'] = 0
		out['total_converted'] = 0
		out['total_N'] = total_N
		return pd.DataFrame.from_dict(out,orient="index"),q
	q.converted_pos_list = q.converted_pos_list.apply(lambda x:eval(x))
	q['distance_to_overlap_end'] = q.apply(get_distance_to_overlap_end,axis=1)
	distance_to_overlap_end_flag=[]
	total_converted = 0
	for i,r in q.iterrows():
		myList = r.converted_pos_list
		flag = False
		for p in myList:
			if strand == "+":
				relative_pos = p+1-start
			else:
				relative_pos = end-(p+1)
			try:
				base = seq[relative_pos]
			except:
				# suggesting incorrect off-target sequence identification, chr16:56994522-56994561. Or BE activity outside spacer.
				print ("relative_pos outside",start,end,p,relative_pos,r.read,seq)  
				continue
			if base !="A":
				# this is possible because the "is converted" function in the pipeline code happends before off-target identification, so we don't know the off-target strand, any A-G or C-T is assumed to be converted. 
				print ("relative_pos not A",start,end,p,relative_pos+1,base,r.read,seq)	
			else:
				relative_pos+=1
				flag = True
				if relative_pos in out:
					out[relative_pos] +=1
				else:
					out[relative_pos] =1
		if flag:
			total_converted+=1
		distance_to_overlap_end_flag.append(flag)

	for k in out:
		if total_N==0:
			out[k] = 0
		else:
			out[k] = out[k]/total_N
	if total_N==0:
		out['total_AG_frequency'] = -1
	else:
		out['total_AG_frequency'] = total_converted/total_N
	out['total_converted'] = total_converted
	out['total_N'] = total_N
	q['OT_name']=OT_name
	q['distance_to_overlap_end_flag']=distance_to_overlap_end_flag
    
	return pd.DataFrame.from_dict(out,orient="index"),q
out = []
out2 = []
for i,r in df.iterrows():
	# if r[c]!="chr10:29443233-29443257":
	#	 continue
	chr = r['#Chromosome']
	start = r.Start
	end = r.End
	seq = r.Site_Sequence
	if str(seq)=="nan":
		seq = r.Site_Sequence_Gaps_Allowed.replace("-","")
		print (seq)
	strand = r.Strand
	RC = r.Nuclease_Read_Count
	tmp,tmp_q = get_AG_vector(read,r[c],chr,start,end,seq,strand,RC,flank=30)
	# out2.append(tmp_q)
	tmp.columns = [r[c]]
	# print (r[c],"finished")
	out.append(tmp)
	out2.append(tmp_q)
ori_df = df.copy()
df = pd.concat(out,axis=1)
df.to_csv(f"{label}.A_to_G_frequency.csv")
AG = pd.read_csv(f"{label}.A_to_G_frequency.csv",index_col=0)
# df2 = ori_df.merge(AG.T[['total_converted','total_N','total_AG_frequency']],left_on=c,right_index=True)
df2 = ori_df.merge(AG.T,left_on=c,right_index=True)
df2.to_csv(f"{label}_identified_matched.add_AG_frequency.csv")

df = pd.concat(out2)
df.to_csv(f"{label}.A_to_G_overlap_distance.csv")