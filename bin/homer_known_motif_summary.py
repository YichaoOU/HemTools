#!/usr/bin/env python
import sys
import os
import pandas as pd
import glob
import numpy as np

files =glob.glob("*/knownResults.txt")
def parse_df(f,col='Log P-value'):
    m = pd.read_csv(f,sep="\t",index_col=0)
    m = m[m['P-value']<0.01]
    try:
        m[col] = [float(x.replace("%","")) for x in m[col]]
    except:
        m[col] = [-x for x in m[col]]
    m = m.sort_values(col,ascending=False)
    m = m[~m.index.duplicated(keep='first')]
    m=m[[col]]
    m.columns = [f.split("/")[-2]]
    return m
df_list = [parse_df(f,col='% of Target Sequences with Motif') for f in files]
motif_table = pd.concat(df_list,axis=1)
df = motif_table.fillna(0)
df.to_csv("Target_percent.summary.csv")


df_list = [parse_df(f,col='Log P-value') for f in files]
motif_table = pd.concat(df_list,axis=1)
df = motif_table.fillna(0)
df.to_csv("nlogP.summary.csv")





























