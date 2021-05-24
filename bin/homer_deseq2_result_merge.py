#!/usr/bin/env python

import sys
import pandas as pd

main_chr = []
for i in range(0,22):
	main_chr.append("chr%s"%(i+1))
main_chr.append("chrX")
main_chr.append("chrY")
LFC_col = 'bg vs. target Log2 Fold Change'
FDR_col = 'bg vs. target adj. p-value'

def parse_df(f):
	if "user_peak.loss" in f:
		flag = True
	else:
		flag = False
	df = pd.read_csv(f,sep="\t")
	# LFC_col = 'bg vs. target Log2 Fold Change'
	# FDR_col = 'bg vs. target adj. p-value'
	df=df[['Chr','Start','End',LFC_col,FDR_col,"Strand"]]
	df=df[df.Chr.isin(main_chr)]
	if flag:
		df[LFC_col] = -df[LFC_col]
	return df
	
df_gain = parse_df(sys.argv[1])
df_loss = parse_df(sys.argv[2])
df = pd.concat([df_gain,df_loss])
df['name'] = df['Chr']+df['Start'].astype(str)+df['End'].astype(str)
df = df.sort_values(FDR_col)
df = df.drop_duplicates('name')
df = df.drop(['name'],axis=1)
df['Start'] = df['Start'].astype(int)
df['End'] = df['End'].astype(int)
df.to_csv(sys.argv[3]+".all.bed",sep="\t",index=False)
df = df[df[LFC_col].abs()>=1]
df = df[df[FDR_col]<=0.05]

df.to_csv(sys.argv[3]+".LFC_1.FDR_05.bed",sep="\t",header=False,index=False)

