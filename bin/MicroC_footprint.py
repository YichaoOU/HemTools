#!/usr/bin/env python


import pandas as pd
import sys
import os

input = sys.argv[1]
output = sys.argv[2]
df = pd.read_csv(input,sep="\t",header=None)
df.head()
df = df[df[0]=="chr11"]
df = df[df[4]=="chr11"]

df1 =  df.copy()
df1['chr'] = df1[0]
df1['end'] = df1[1]
df1['start'] = df1[1]-1
df1['OE_pos'] = df1[5]
df1 = df1[['chr','start','end','OE_pos']]
df2 =  df.copy()
df2['chr'] = df2[0]
df2['end'] = df2[5]
df2['start'] = df2[5]-1
df2['OE_pos'] = df2[1]
df2 = df2[['chr','start','end','OE_pos']]

df3 = pd.concat([df1,df2])
df3
df3.to_csv("test.bed",sep="\t",header=False,index=False)
os.system("bedtools intersect -a test.bed -b /home/yli11/dirs/MicroC_yli11_2022-10-21/LCR.bed -u > test.out")
df4 = pd.read_csv("test.out",sep="\t",header=None)
df5 = pd.DataFrame(df4[3].value_counts().sort_values(ascending=False))
df5 = df5.reset_index()

df5[1] = df5['index']-1
df5[2] = df5[1] + 1
df5[0] = "chr11"
df5[[0,1,2,3]].to_csv(output,sep="\t",header=False,index=False)

