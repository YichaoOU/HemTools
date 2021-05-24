#!/usr/bin/env python
import pandas as pd
import sys
file = sys.argv[1]
out =sys.argv[2]
df = pd.read_csv(file,sep="\t",header=None)
df['center'] = (df[1]+df[2])/2
df['center'] = df['center'].astype(int)
df[2] = df['center'] + 1
if df.shape[1] > 5:
	df[[0,'center',2,3,4,5]].sort_values([0,'center']).to_csv(out,sep="\t",header=False,index=False)
else:
	df[[0,'center',2]].sort_values([0,'center']).to_csv(out,sep="\t",header=False,index=False)