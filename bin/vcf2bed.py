#!/usr/bin/env python


import pandas as pd
import sys
output = sys.argv[2]
ext = int(sys.argv[3])
df = pd.read_csv(sys.argv[1],sep="\t",comment="#",header=None)
if not "chr" in df[0].tolist()[0]:
	df[0] = "chr"+df[0].astype(str)
if ext == 0:
	df['end'] = df[1]
	df[1] = df[1]-1
else:
	df['end'] = df[1]+ext
	df[1] = df[1]-ext
	df[1] = df[1].clip(lower=0)
df[[0,1,'end', 2,3,4]].to_csv(output,sep="\t",header=False,index=False)
