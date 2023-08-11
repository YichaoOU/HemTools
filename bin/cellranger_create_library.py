#!/usr/bin/env python


import pandas as pd
import os
import glob
import sys

rna="Gene Expression"
atac="Chromatin Accessibility"

rna_dir=sys.argv[1]
atac_dir=sys.argv[2]
df = pd.read_csv(sys.argv[3],sep="\t",header=None)

df['rna'] = rna
df['atac'] = atac
df['rna_dir'] = rna_dir
df['atac_dir'] = atac_dir

s1 = df[['rna_dir',1,'rna']]
s2 = df[['atac_dir',1,'atac']]
s1.columns = ["fastqs","sample","library_type"]
s2.columns = ["fastqs","sample","library_type"]        
df2 = pd.concat([s1,s2])

for s,d in df2.groupby("sample"):
    d.to_csv(f"{s}.csv",index=False)


tmp = df2.drop_duplicates('sample')
tmp = tmp[['sample']]
tmp.to_csv("input.list",header=False,index=False)

# /home/yli11/dirs/hem_seq/chenggrp/pdoerfler_single-cell/pdoerfler_10XscRNAseq_rep2