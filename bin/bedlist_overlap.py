#!/usr/bin/env python


import pandas as pd
import sys
import os

"""making a binary matrix for subsequent analysis

input
-----

bed list 1
bed list 2

File names will be used as column or row names.

output
------

my_overlap_matrix.tsv

last column is name

example
--------


/home/yli11/Data/Mouse/mouse_blood/mouse_blood_ATAC.list

"""
main_chr=['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY', 'chrM']


def read_bed(f,flag,extend):
	print ("Reading: %s"%(f))
	# df = pd.read_csv(f,sep="\t",header=None,names=list(range(30)),engine='python')
	df = pd.read_csv(f,sep="\t",header=None,names=list(range(30)))
	# df = pd.read_csv(f,sep="\t",names=list(range(16)))
	# print (df.head(n=2))
	label = f.split("/")[-1].split(".")[0]
	df = df[df[0].isin(main_chr)]
	df[1] = df[1].astype(int)-extend
	df[2] = df[2].astype(int)+extend
	df[3] = df[0]+"_"+df[1].astype(str)+"_"+df[2].astype(str)+"_"+df[3].astype(str)+"_"+label
	if flag:
		df[3] = label
	return df[[0,1,2,3]]

def make_feature_bed(myList,out,flag,extend):
	if not flag:
		df_list = [read_bed(myList,flag,extend)]
	else:
		df_list = [read_bed(f,flag,extend) for f in pd.read_csv(myList,header=None)[0].tolist()]
	df = pd.concat(df_list)
	df.to_csv(out,sep="\t",header=False,index=False)
extend = int(sys.argv[3])
make_feature_bed(sys.argv[1],"tmp1.bed",False,0)
make_feature_bed(sys.argv[2],"tmp2.bed",True,extend)
command = "module load bedtools/2.29.2;bedtools intersect -a tmp1.bed -b tmp2.bed -wao > tmp3.bed"
os.system(command)
df = pd.read_csv("tmp3.bed",sep="\t",header=None,names=list(range(9)))
# print (df[3].nunique())

df[7] = df[7].fillna("dummy")
df[7] = df[7].replace(".","dummy")
# print (df.head())
# print (df[7].unique().tolist())
df2 = pd.crosstab(index=df[3], columns = df[7])
# print (df2.head())
try:
	df2 = df2.drop(['dummy'],axis=1)
except:
	pass
df2 = (df2>0).astype(int)
df2['class'] = [x.split("_")[-1] for x in df2.index.tolist()]
df2.to_csv("my_overlap_matrix.%s.tsv"%(extend),sep="\t")
df3 = df2.drop(['class'],axis=1)
df3 = df3.sum()/df3.shape[0]
df3.to_csv("peak_overlap_percent.%s.tsv"%(extend),sep="\t",header=False)
# print (df3.head())
# for c in df2.columns:
	# if c =="class":
		# continue
	# print (c,df2[c].sum()/float(df2.shape[0]))

# os.system("rm tmp1.bed")
# os.system("rm tmp2.bed")
# os.system("rm tmp3.bed")
## output individual overlapped peaks for homer analysis
# df = pd.read_csv("tmp3.bed",sep="\t",header=None,names=list(range(9)))
# df = df.dropna()
# df = df[df[3].str.contains("NFIX")]
# print (df.shape)
# print (df[7].unique().tolist())
# for s,d in df.groupby(7):
	# d = d.drop_duplicates(3)
	# d[[0,1,2]].to_csv("%s_NFIX_close.bed"%(s),sep="\t",header=False,index=False)







