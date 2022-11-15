#!/usr/bin/env python

import pandas as pd
import sys
import os

bed_file = sys.argv[1]
bedpe_file = sys.argv[2]
flag = "no_chr" in bedpe_file
bed = pd.read_csv(bed_file,sep="\t",comment = "#",header=None)


bedpe = pd.read_csv(bedpe_file,sep="\t",comment = "#",header=None)
# print (bedpe.head())
if flag:
	bedpe[0] = "chr"+bedpe[0]
	bedpe[3] = "chr"+bedpe[3]

bedpe['source'] = bedpe[0]+"-"+bedpe[1].astype(str)+"-"+bedpe[2].astype(str)
bedpe['target'] = bedpe[3]+"-"+bedpe[4].astype(str)+"-"+bedpe[5].astype(str)
bedpe['score'] = 1
bedpe = bedpe.drop_duplicates(['source','target'])
bedpe[[0,1,2,3,4,5,'score','score']].to_csv("input.bedpe",sep="\t",header=False,index=False)
# print (bedpe.head())
t1=bedpe[[0,1,2]]
t2 = bedpe[[3,4,5]]
t2.columns = [0,1,2]
out = pd.concat([t1,t2])
# print (out.head())
out.to_csv("bedpe.bed",sep="\t",header=False,index=False)
command = "bedtools intersect -a %s -b bedpe.bed -wo > tmp.bed"%(bed_file)
print (command)
os.system(command)

df = pd.read_csv("tmp.bed",sep="\t",header=None)
# print (df.head())
chr = df.columns[-4]
start = df.columns[-3]
end = df.columns[-2]
df.index = df[chr]+"-"+df[start].astype(str)+"-"+df[end].astype(str)
out = []
subset_interactions = []
for i,r in df.iterrows():
	line = r.tolist()
	# print ("line",line,i)
	t1 = bedpe[bedpe.source==i][[3,4,5]]
	t2 = bedpe[bedpe.target==i][[0,1,2]]
	t1.columns = [0,1,2]
	tmp = pd.concat([t1,t2])
	tmp = tmp.drop_duplicates([0,1,2])
	print (tmp)
	for i,x in tmp.iterrows():
		# print (x)
		line2 = line+x.tolist()
		out.append(line2)
out = pd.DataFrame(out)
print (out)
out.to_csv("bed_overlap_bedpe.tsv",sep="\t",header=False,index=False)

