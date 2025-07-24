#!/hpcf/apps/python/install/2.7.13/bin/python





"""
Program to get average editing frequency from CrispEsso.
"""

# import matplotlib
import pandas as pd
# matplotlib.use('agg')
# import matplotlib.pyplot as plt
# import seaborn as sns
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
	


def is_edit2(r,ref,alt,input_gRNA,SNP_dict=None):
	# update: fix for 19bp and 21 bp sgRNA
	gRNA_length = len(input_gRNA)
	offset = 20-gRNA_length
	# specific to our case where plot length is 24bp
	read = r.Aligned_Sequence[2+offset:22]
	gRNA = r.Reference_Sequence[2+offset:22]
	# print (gRNA)
	if read == gRNA:
		return False
	count = 1
	
	for i in range(0,10): # first 10bp
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

def is_edit_other(r,ref,alt,input_gRNA,SNP_dict=None):
	# update: fix for 19bp and 21 bp sgRNA
	gRNA_length = len(input_gRNA)
	offset = 20-gRNA_length
	read = r.Aligned_Sequence[2+offset:22]
	gRNA = r.Reference_Sequence[2+offset:22]
	if read == gRNA:
		return False
	count = 1
	
	for i in range(0,10): # first 10bp
		a = read[i]
		b = gRNA[i]
		try:
			SNP_base = SNP_dict[count]
			b = SNP_base
			# if r['%Reads'] >1:
				# print (read,gRNA,r['%Reads'],a,b,SNP_base)
		except:
			pass
		if (b == ref) and (a != alt) and (a != ref) and (a != "N"):
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
	df['Reference_Sequence_remove_indel'] = df.Reference_Sequence.apply(lambda x:x.replace("-",""))
	df['is_gRNA'] = [gRNA in x for x in df.Reference_Sequence]
	df['is_gRNA_remove_indel'] = [gRNA in x for x in df.Reference_Sequence_remove_indel]

	df2 = df[df.is_gRNA_remove_indel == True]
	df = df[df.is_gRNA == True]
	# print (df.head())
	if df2.shape[0]==0:
		print (f,gRNA,"gRNA not found, Exit!")
		return -1,-1,-1,-1
		# exit()
	if df.shape[0]==0:
		return 0,0,0,0
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
	# print (f)
	# df['is_edit'] = df.apply(lambda r: is_edit(r,ref,alt,SNP_pos,SNP_base),axis=1)
	df['is_edit'] = df.apply(lambda r: is_edit2(r,ref,alt,gRNA,SNP_dict),axis=1)
	edited_N = df[(df.Unedited == False)&(df.is_edit == True)]['#Reads'].sum()
	edited_P = df[(df.Unedited == False)&(df.is_edit == True)]['%Reads'].sum()
	df['is_edit_other'] = df.apply(lambda r: is_edit_other(r,ref,alt,gRNA,SNP_dict),axis=1)
	edited_N_other = df[(df.Unedited == False)&(df.is_edit_other == True)]['#Reads'].sum()
	edited_P_other = df[(df.Unedited == False)&(df.is_edit_other == True)]['%Reads'].sum()
	return edited_N,edited_P,edited_N_other,edited_P_other

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
	N_list_other = []
	P_list_other = []
	gRNA_list = []
	name_list = []
	for name,_,gRNA in df.values:
		# print (name,gRNA)
		# file = "{0}_results/CRISPRessoWGS_on_{0}/CRISPResso_on_{1}/Alleles_frequency_table_around_sgRNA_{2}.txt".format(s,name,gRNA)
		file = "{0}_results/CRISPRessoWGS_on_{0}/CRISPResso_on_{1}/Alleles_frequency_table_around_sgRNA_{2}.txt".format(s,correct_name(name),gRNA)
		# print (file)
		if os.path.isfile(file):
			# print (name,gRNA)
			N,P,N_other,P_other = parse_df(file,gRNA,ref,alt,SNP)
		else:
			N=-1
			P=-1
			N_other=-1
			P_other=-1
		N_list.append(N)
		P_list.append(P)
		N_list_other.append(N_other)
		P_list_other.append(P_other)
		gRNA_list.append(gRNA)
		name_list.append(name)


	out = pd.DataFrame()
	out['Sample'] = name_list
	out['gRNA'] = gRNA_list
	out['#Reads'] = N_list
	out['%Reads'] = P_list
	out['#Reads_other'] = N_list_other
	out['%Reads_other'] = P_list_other
	out.to_csv(outfile,sep="\t",index=False)
