#!/usr/bin/env python

import pandas as pd

import sys


bed = sys.argv[1]
out = sys.argv[2]
df = pd.read_csv(bed,sep="\t",comment = "#",header=None)
df['name'] = df[0]+df[1].astype(str)+df[2].astype(str)
df = df.sort_values(4)
df = df.drop_duplicates('name')
df[[0,1,2,3,4,5]].to_csv(out,sep="\t",header=False,index=False)


