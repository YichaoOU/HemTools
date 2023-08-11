#!/usr/bin/env python


import pysam
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
import glob
from joblib import Parallel, delayed
import sys

bamFile=sys.argv[1]
label=sys.argv[2]
setting=int(sys.argv[3])
KJ002={}
# 1-based
KJ002['barcode_start'] = 1788
KJ002['barcode_end'] = 1802
KJ002['cas9_start'] = 229
KJ002['cas9_end'] = 960
KJ001={}
# 1-based
KJ001['barcode_start'] = 1422
KJ001['barcode_end'] = 1436
KJ001['cas9_start'] = 229
KJ001['cas9_end'] = 960
'''
def get_read_stats(r):
	tmp = pd.DataFrame(r.cigartuples)
	tmp_i = tmp[tmp[0]==1][1].sum()
	tmp_d = tmp[tmp[0]==2][1].sum()

	return [r.reference_start,r.reference_end,r.query_alignment_length,int(r.is_forward),tmp_i,tmp_d]
def get_barcode(r,start,end):
	ref = r.get_reference_sequence()[start-1:end]
	myList = r.get_aligned_pairs(with_seq=True)
	df = pd.DataFrame(myList)
	df = df[df[1].between(start-1,end-1)]
	df = df.dropna() # m64304e_230324_210653/1770266/ccs	0	KJ002	1	60	1335M1D451M15D217M	
	if df.shape[0]<=1:
		return "",ref

	query_start = int(df[0].min())
	query_end = int(df[0].max())+1
	query = r.query_sequence[query_start:query_end]
	return query,ref

def get_cas9(r,start,end):
	myList = r.get_aligned_pairs(with_seq=True)
	ref = r.get_reference_sequence()[start-1:end]
	df = pd.DataFrame(myList)
	df = df[df[1].between(start-1,end-1)]
	df = df.dropna() # m64304e_230324_210653/1770266/ccs	0	KJ002	1	60	1335M1D451M15D217M	
	if df.shape[0]<=1:
		return "",ref

	
	query_start = int(df[0].min())
	query_end = int(df[0].max())+1
	
	query = r.query_sequence[query_start:query_end]	
	return query,ref
def parse_bam(file,myDict):
	f = pysam.AlignmentFile(file)
	out = []
	for read in f.fetch():
		outline = [read.query_name]
		if read.is_supplementary:
			continue
		if not read.is_mapped:
			out.append(outline+[-1]*6+[""]*4)
			continue
		stats = get_read_stats(read)
		barcode_read,barcode_ref = get_barcode(read,myDict['barcode_start'],myDict['barcode_end'])
		cas9_read,cas9_ref = get_cas9(read,myDict['cas9_start'],myDict['cas9_end'])
		outline+=stats+[barcode_read,barcode_ref,cas9_read,cas9_ref]
		out.append(outline)
	df = pd.DataFrame(out)
	df.columns = ['read','start','end','read_length','strand','#I','#D','barcode','barcode_ref','cas9','cas9_ref']
	return df
	
def parse_read(read,myDict):
	# print (myDict)
	outline=[read.query_name]
	if not read.is_mapped:
		return outline+[-1]*6+[""]*4

	stats = get_read_stats(read)
	barcode_read,barcode_ref = get_barcode(read,myDict['barcode_start'],myDict['barcode_end'])
	cas9_read,cas9_ref = get_cas9(read,myDict['cas9_start'],myDict['cas9_end'])
	outline+=stats+[barcode_read,barcode_ref,cas9_read,cas9_ref]
	return outline
	# df = pd.DataFrame(out)
	# df.columns = ['read','start','end','read_length','strand','#I','#D','barcode','barcode_ref','cas9','cas9_ref']
	# return df

def read_to_dict(f):
	f = pysam.AlignmentFile(f)
	myDict = {}
	for read in f.fetch():
		if read.is_supplementary:
			continue  
		myDict[read.query_name]	=read
	return myDict
	
def read_to_list(bamFile):
	f = pysam.AlignmentFile(bamFile)
	myDict = []
	for read in f.fetch():
		if read.is_supplementary:
			continue  
		myDict.append(read)
	return myDict
'''

def read_to_list(f):
	f = pysam.AlignmentFile(f)
	myList = []
	# count = 0
	for read in f.fetch():
		if read.is_supplementary:
			continue
		# count += 1
		# if count > 100:
			# return myList
		readDict={}
		readDict['query_name'] = read.query_name
		readDict['is_mapped'] = read.is_mapped
		readDict['query_sequence'] = read.query_sequence
		readDict['reference_start'] = read.reference_start
		readDict['reference_end'] = read.reference_end
		readDict['query_alignment_length'] = read.query_alignment_length
		readDict['is_forward'] = read.is_forward
		readDict['cigartuples'] = pd.DataFrame(read.cigartuples)
		readDict['get_aligned_pairs'] = pd.DataFrame(read.get_aligned_pairs(with_seq=True))
		myList.append(readDict)
	return myList

def get_read_stats(r):
	tmp = r['cigartuples']
	tmp_i = tmp[tmp[0]==1][1].sum()
	tmp_d = tmp[tmp[0]==2][1].sum()
	tmp_s = r['get_aligned_pairs'].copy()
	tmp_s = tmp_s[tmp_s[2].isin(['a','c','g','t'])]
	tmp_s = tmp_s.shape[0]
	return [r['reference_start'],r['reference_end'],r['query_alignment_length'],int(r['is_forward']),tmp_i,tmp_d,tmp_s]
def get_barcode(r,start,end):
	df = r['get_aligned_pairs'].copy()
	tmp = df[df[1].between(start-1,end-1)] # in case of insertion, will not be included
	if tmp.dropna().shape[0]<=1:
		return ["",""]
	index_min = tmp.index.min() 
	index_max = tmp.index.max() 
	# try:
		# df = df.loc[list(range(index_min,index_max+1))]
	# except:
		# print (r)
		# print (index_min)
		# print (index_max)
	df = df.loc[list(range(index_min,index_max+1))]
	df = df.dropna() # m64304e_230324_210653/1770266/ccs	0	KJ002	1	60	1335M1D451M15D217M	

	# try:
	#	 query_start = int(df[0].min())
	# except:
	#	 print (r.query_name)
	#	 display(df)
	#	 query_start=-1
	query_start = int(df[0].min())
	query_end = int(df[0].max())+1
	query = r['query_sequence'][query_start:query_end]
	ref = "".join(df[2].tolist())
	return [query,ref]

def get_cas9(r,start,end):
	df = r['get_aligned_pairs'].copy()
	tmp = df[df[1].between(start-1,end-1)] # in case of insertion, will not be included
	if tmp.dropna().shape[0]<=1:
		return ["","",-1,-1,-1]
	index_min = tmp.index.min() 
	index_max = tmp.index.max() 
	df = df.loc[list(range(index_min,index_max+1))]
	df2 = df.dropna() # m64304e_230324_210653/1770266/ccs	0	KJ002	1	60	1335M1D451M15D217M	
		
	# try:
	#	 query_start = int(df2[0].min())
	# except:
	#	 print (r.query_name)
	#	 display(df2)
	#	 query_start=-1
	query_start = int(df2[0].min())
	query_end = int(df2[0].max())+1
	query = r['query_sequence'][query_start:query_end]
	ref = "".join(df2[2].tolist())
	tmp_i = df[1].isnull().sum()
	tmp_d = df[0].isnull().sum()
	tmp_s = df[df[2].isin(['a','c','g','t'])]
	tmp_s = tmp_s.shape[0]
	return [query,ref,tmp_i,tmp_d,tmp_s]
def parse_bam(file,myDict):
	f = pysam.AlignmentFile(file)
	out = []
	for read in f.fetch():
		outline = [read.query_name]
		if read.is_supplementary:
			continue
		if not read.is_mapped:
			out.append(outline+[-1]*6+[""]*4)
			continue
		
		stats = get_read_stats(read)
		barcode = get_barcode(read,myDict['barcode_start'],myDict['barcode_end'])
		cas9_read,cas9_ref = get_cas9(read,myDict['cas9_start'],myDict['cas9_end'])
		outline+=stats+[barcode_read,barcode_ref,cas9_read,cas9_ref]
		out.append(outline)
	df = pd.DataFrame(out)
	df.columns = ['read','start','end','read_length','strand','#I','#D','barcode','barcode_ref','cas9','cas9_ref']
	return df
def parse_read(read,myDict):
	"""Parse a read and get barcode and cas9 sequence
	
	Return
	------
	outline is a list, used for parallel processing
	
	The list contains:
	1. read name
	2. start
	3. end
	4. read_length
	5. strand
	6. total # insertion
	7. total # deletion
	8. total # substitution
	9. I/D/S in cas9 region
	12. barcode
	13. barcode ref
	14. cas9
	15. cas9 ref
	
	"""
	outline = [read["query_name"]]
	if not read["is_mapped"]:
		return outline+[-1]*7+[""]*4+[-1]*3
	try:
		# [r['reference_start'],r['reference_end'],r['query_alignment_length'],int(r['is_forward']),tmp_i,tmp_d,tmp_s]
		stats = get_read_stats(read)
		barcode = get_barcode(read,myDict['barcode_start'],myDict['barcode_end'])
		# [query,ref,tmp_i,tmp_d,tmp_s]
		cas9 = get_cas9(read,myDict['cas9_start'],myDict['cas9_end'])
		outline+=stats+barcode+cas9
	except:
		outline = [read["query_name"]+"|Failed"]+[-1]*7+[""]*4+[-1]*3
	return outline

myList = read_to_list(bamFile)
# parse_read(myList[0],KJ002)
if setting==2:
	out = Parallel(n_jobs=8,verbose=10,backend="loky",batch_size=32)(delayed(parse_read)(m,KJ002) for m in myList)
if setting==1:
	out = Parallel(n_jobs=8,verbose=10,backend="loky",batch_size=32)(delayed(parse_read)(m,KJ001) for m in myList)
# out = Parallel(n_jobs=-1,verbose=10,backend="multiprocessing")(delayed(parse_read)(myDict[m],KJ002) for m in myDict)
df = pd.DataFrame(out)
# df.columns = ['read','start','end','read_length','strand','#I','#D','barcode','barcode_ref','cas9','cas9_ref']
df.to_csv(f"{label}.read_stat.csv",index=False,header=False)