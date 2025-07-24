#!/hpcf/apps/python/install/2.7.13/bin/python





"""
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
	

def is_edit(r,ref,alt,SNP_pos=0,SNP_base=None):
	read = r.Aligned_Sequence[10:30]
	gRNA = r.Reference_Sequence[10:30]
	if read == gRNA:
		return False
	count = 1
	for i in range(len(read)):
		a = read[i]
		b = gRNA[i]
		if count == SNP_pos:
			b = SNP_base
			if r['%Reads'] >1:
				print (read,gRNA,r['%Reads'],a,b,SNP_base)
		if (b == ref) and (a == alt):
			return True
		count += 1
	return False
	
def is_edit2(r,ref,alt,gRNA_length,SNP_dict=None):
	# update: fix for 19bp and 21 bp sgRNA
	offset = 20-gRNA_length
	read = r.Aligned_Sequence[10+offset:30]
	gRNA = r.Reference_Sequence[10+offset:30]
	if read == gRNA and SNP_dict==None:
		return False
	count = 1

	for i in range(3,10):
	# for i in range(0,10): # for Varun ABE paper
		a = read[i]
		b = gRNA[i]
		# if gRNA=="TTGTTGCCCGCAAGGTTTGG" and count == 6 and r['%Reads']>50:
			
			# print (i,count,a,b,SNP_dict,read,gRNA)
		try:
			SNP_base = SNP_dict[count]
			b = SNP_base
			# if r['%Reads'] >1:
				# print (read,gRNA,r['%Reads'],a,b,SNP_base)
		except:
			pass
		if (b == ref) and (a == alt):
			# if gRNA=="TTGTTGCCCGCAAGGTTTGG":
				# print ("True",r['%Reads'])
			return True
		count += 1
	return False
	
def is_edit2_bk(r,ref,alt,gRNA_length,SNP_dict=None):
	# update: fix for 19bp and 21 bp sgRNA
	offset = 20-gRNA_length
	read = r.Aligned_Sequence[10+offset:30]
	gRNA = r.Reference_Sequence[10+offset:30]
	if read == gRNA:
		return False
	count = 1
	for i in range(len(read)):
		a = read[i]
		b = gRNA[i]
		try:
			SNP_base = SNP_dict[count]
			b = SNP_base
			# if r['%Reads'] >1:
				# print (read,gRNA,r['%Reads'],a,b,SNP_base)
		except:
			pass
		if (b == ref) and (a == alt):
			return True
		count += 1
	return False


def is_edit3(r,ref,alt,SNP_dict=None):
	read = r.Aligned_Sequence[10:30]
	gRNA = r.Reference_Sequence[10:30]
	if read == gRNA:
		return False
	count = 1
	for i in range(len(read)):
		a = read[i]
		b = gRNA[i]
		try:
			SNP_base = SNP_dict[count]
			b = SNP_base
			# if r['%Reads'] >1:
				# print (read,gRNA,r['%Reads'],a,b,SNP_base)
		except:
			pass
		if (b == ref) and (a == alt):
			return True
		count += 1
	return False
def get_SNP_dict(df):
	try:
		df.shape[1]
	except:
		df = pd.DataFrame(df).T
	df.index = df[1].tolist()
	return df[2].to_dict()

def parse_df(f,gRNA,ref,alt,snp):

	df = pd.read_csv(f,sep="\t")
	df['is_gRNA'] = [gRNA in x for x in df.Reference_Sequence]
	# print (df.head())
	df = df[df.is_gRNA == True]
	# print (df.head())
	if df.shape[0]==0:
		print (f,gRNA,"gRNA not found, Exit!")
		exit()
	try:
		tmp = snp.loc[gRNA]
		# print (tmp)
		flag = True
	except:
		tmp = None
		flag = False
	if flag:
		# SNP_pos = tmp[1]
		# SNP_base = tmp[2]
		SNP_dict = get_SNP_dict(tmp)
		# print (SNP_dict)
	else:
		# SNP_pos = 0
		# SNP_base = None
		SNP_dict = None
	# print (f,SNP_dict)
	# df['is_edit'] = df.apply(lambda r: is_edit(r,ref,alt,SNP_pos,SNP_base),axis=1)
	df['is_edit'] = df.apply(lambda r: is_edit2(r,ref,alt,len(gRNA),SNP_dict),axis=1)
	# edited_N = df[(df.Unedited == False)&(df.is_edit == True)]['#Reads'].sum()
	# edited_P = df[(df.Unedited == False)&(df.is_edit == True)]['%Reads'].sum()
	edited_N = df[(df.is_edit == True)]['#Reads'].sum()
	edited_P = df[(df.is_edit == True)]['%Reads'].sum()
	return edited_N,edited_P

def parse_snp(f):
	df = pd.read_csv(f,sep="\t",header=None,index_col=0)
	return df

sample_id_list = [sys.argv[1]]
df = pd.read_csv(sys.argv[2],sep="\t",header=None)
ref=sys.argv[3]
alt=sys.argv[4]

try:
	SNP = parse_snp(sys.argv[5])
except:
	SNP=None

def correct_name(x):
	x = x.replace(":","_")
	x = x.replace(".","_")
	return x
	
for s in sample_id_list:
	outfile = "%s.allele.edit.tsv"%(s)
	N_list = []
	P_list = []
	gRNA_list = []
	name_list = []
	for name,_,gRNA in df.values:
		# print (name,gRNA)
		# file = "{0}_results/CRISPRessoPooled_on_{0}/CRISPResso_on_{1}/Alleles_frequency_table_around_sgRNA_{2}.txt".format(s,name,gRNA)
		file = "{0}_results/CRISPRessoPooled_on_{0}/CRISPResso_on_{1}/Alleles_frequency_table_around_sgRNA_{2}.txt".format(s,correct_name(name),gRNA)
		# print (file)
		if os.path.isfile(file):
			# print (name,gRNA)
			N,P = parse_df(file,gRNA,ref,alt,SNP)
		else:
			N=-1
			P=-1
		N_list.append(N)
		P_list.append(P)
		gRNA_list.append(gRNA)
		name_list.append(name)


	out = pd.DataFrame()
	out['Sample'] = name_list
	out['gRNA'] = gRNA_list
	out['#Reads'] = N_list
	out['%Reads'] = P_list
	out.to_csv(outfile,sep="\t",index=False)
