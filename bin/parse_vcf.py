#!/usr/bin/env python
import pandas as pd
import sys
df = pd.read_csv(sys.argv[1],header=None,comment="#",sep="\t")
total_variants = float(df.shape[0])
AG_conversion = df[(df[3]=="A")&(df[4]=="G")].shape[0]
CT_conversion = df[(df[3]=="C")&(df[4]=="T")].shape[0]
print AG_conversion,AG_conversion/total_variants,CT_conversion,CT_conversion/total_variants,total_variants

for x in df[3].unique().tolist():
	if len(x) <=2:
		print x
for x in df[4].unique().tolist():
	if len(x) <=2:
		print x














