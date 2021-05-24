#!/usr/bin/env python


import pandas as pd
import sys

fimo_file = sys.argv[1]
output = sys.argv[2]
df = pd.read_csv(fimo_file,sep="\t",skiprows = 1,header=None)
df['name'] = df[0]+df[1]
df = df.drop_duplicates('name')
motif_list = df[0].unique().tolist()
seq_list = df[1].unique().tolist()
test = pd.crosstab(df[0], df[1])
test2 = test.dot(test.T)
test3 = test2.copy()
test3['motif'] = test2.index.tolist()
a=pd.melt(test3,id_vars=['motif'],value_vars=test2.columns)
a.index = a['motif']+"||"+a[0]
a = a.sort_values("value",ascending=False)
a['value'].to_csv(output)

