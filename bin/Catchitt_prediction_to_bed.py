#!/usr/bin/env python

import pandas as pd
import os
import sys

input = sys.argv[1]
cutoff = float(sys.argv[2])
# cutoff=0.4
out = sys.argv[3]


try:
	binSize = int(sys.argv[4])
except:
	binSize=50

df = pd.read_csv(input,sep="\t",header=None)

def cutoff_bed(tmp,out,binSize,cutoff):
	out = str(cutoff)+out
	df = tmp.copy()
	df[3] = df[1]+binSize
	df = df[df[2]>=cutoff]
	df = df[[0,1,3,2]]
	df.to_csv(out+".tmp",sep="\t",header=False,index=False)
	command = "module load bedtools;sort -k1,1 -k2,2n %s.tmp | bedtools merge -i - -c 4 -o max > %s;rm %s.tmp"%(out,out,out)
	os.system(command)

cutoff_bed(df,out,binSize,cutoff)
# cutoff_bed(df,out,binSize,0.5)
# cutoff_bed(df,out,binSize,0.6)
# cutoff_bed(df,out,binSize,0.7)
# cutoff_bed(df,out,binSize,0.71)
# cutoff_bed(df,out,binSize,0.72)
# cutoff_bed(df,out,binSize,0.73)
# cutoff_bed(df,out,binSize,0.74)
# cutoff_bed(df,out,binSize,0.75)
# cutoff_bed(df,out,binSize,0.8)
# cutoff_bed(df,out,binSize,0.9)

exit()
df[3] = df[1]+binSize
# df2 = df[df[2]>=0.4]
# df3 = df[df[2]>=0.3]
df = df[df[2]>=cutoff]
df = df[[0,1,3,2]]
# df2 = df2[[0,1,3,2]]
# df3 = df3[[0,1,3,2]]
df.to_csv(out+".tmp",sep="\t",header=False,index=False)
# df2.to_csv(out+".tmp2",sep="\t",header=False,index=False)
# df3.to_csv(out+".tmp3",sep="\t",header=False,index=False)
# merge bed
command = "module load bedtools;sort -k1,1 -k2,2n %s.tmp | bedtools merge -i - -c 4 -o max > %s;rm %s.tmp"%(out,out,out)
os.system(command)

# command = "module load bedtools;sort -k1,1 -k2,2n %s.tmp2 | bedtools merge -i - -c 4 -o max > %s.04;rm %s.tmp2"%(out,out,out)
# os.system(command)

# command = "module load bedtools;sort -k1,1 -k2,2n %s.tmp3 | bedtools merge -i - -c 4 -o max > %s.03;rm %s.tmp3"%(out,out,out)
# os.system(command)

# df = pd.read_csv(out,sep="\t",header=None)
# df2 = pd.read_csv("%s.04"%(out),sep="\t",header=None)
# if df.shape[0]<5000:
	# df2 = df2.sort_values(3,ascending=False)
	# df2 = df2.head(n=5000)
	# df2.to_csv(out,sep="\t",header=False,index=False)
# os.system("rm %s.04"%(out))
