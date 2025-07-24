#!/usr/bin/env python

import pandas as pd
import numpy as np



cutoff=1000

df = pd.read_csv("summary.tsv",sep="\t",header=None)
df[9] = df[6]/df[8]
df = df.fillna(-1)
chr=["chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX","chrY"]
chr_dict = {}
for i in range(len(chr)):
    chr_dict[chr[i]] = i
df['chr_order'] = df[2].map(chr_dict)
df = df[~df.chr_order.isnull()]
df = df.sort_values(["chr_order",3])

df = df[df[8]>=cutoff]
df[10] = df[0].apply(lambda x:x.split("_")[0])
df
df.head()
def get_sample_label(x):
    for i in range(50):
        x = x.replace(f"_S{i}.bam","")
    return x
df['sample_label'] = df[0].apply(get_sample_label)
## read user label
info = pd.read_csv("user_label.tsv",sep="\t",header=None)

info_dict = info.set_index(1)[0].to_dict()
df['user_label'] = df.sample_label.map(info_dict)
df2 = df.groupby([1,"user_label"]).mean().reset_index()
df2 = df2.pivot(index=1,columns="user_label",values=9).T
df2 = df2*100
df2 = df2.reset_index()
df2['chr'] = df2[1].map(df.set_index(1)[2].to_dict())
df2['start'] = df2[1].map(df.set_index(1)[3].to_dict())
df2['chr_order'] = df2['chr'].map(chr_dict)
df2 = df2.sort_values(["chr_order",'start'])
df2.columns = ['name']+df2.columns[1:].tolist()
df2.to_csv("data_for_Manhattan_plot.csv",index=False)


