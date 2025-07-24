#!/usr/bin/env python


import sys
import glob

import pandas as pd



def read_file(f):

	indel_df = pd.read_csv(f,sep="\t",header=None)
	total = indel_df[8].sum()
	indel_reads = indel_df[6].sum()
	if total == 0:
		total = -1
		indel_reads = -1
	indel = float(indel_reads)/total
	if total == 0:
		indel = -1
	out = [total,indel_reads,indel]
	out = pd.DataFrame(out).T
	out.columns = ['Total reads','indel reads','indel frequency']
	out.index = [f.split("/")[0]]
	return out


files = glob.glob("*/*.tsv")
print (files)
df_list = [read_file(f) for f in files]
df = pd.concat(df_list)

# for g34 indel types
def read_group_file2(x,file_list):
    try:
        df_list = [pd.read_csv(f,index_col=0) for f in file_list]
        df = pd.concat(df_list,axis=1)
        df = df.fillna(0)
        df = pd.DataFrame(df.sum(axis=1).astype(int).sort_values(ascending=False))
        df = df.reset_index()
        df['label'] = x
        df.columns = ['indel_type',"read_count","label"]
        # display(df.head(n=10).reset_index().values)
        # display(df.head(n=10))
        # display(df.head())
        return df
    except:
        df = pd.DataFrame()
        df.columns = ['indel_type',"read_count","label"]
        df.loc[0]=[0,0,x]
        return df



files = glob.glob("*/*indel_spectrum.sum.csv")
file_group = {}
for f in files:
	g = f.split("/")[0]
	if g in file_group:
		file_group[g].append(f)
	else:
		file_group[g]=[f]
out  = [read_group_file2(x,file_group[x]) for x in file_group]
out = pd.concat(out)
df2 = df.merge(out,left_index=True,right_on="label",how="left")
df2.to_csv("merged.indel.indel_spectrum.csv")






















# for g34 indel types
def read_group_file(x,file_list):
	try:
		df_list = [pd.read_csv(f,index_col=0) for f in file_list]
		df = pd.concat(df_list,axis=1)
		df = df.fillna(0)
		df = pd.DataFrame(df.sum(axis=1).astype(int).sort_values(ascending=False))
		return [x]+df.head(n=10).reset_index().values.flatten().tolist()
	except:
		return [x]



files = glob.glob("*/*indel_spectrum.sum.csv")
file_group = {}
for f in files:
	g = f.split("/")[0]
	if g in file_group:
		file_group[g].append(f)
	else:
		file_group[g]=[f]
out  = [read_group_file(x,file_group[x]) for x in file_group]
out = pd.DataFrame(out)
out = out.set_index(0)
# out.to_csv("merged.pivot.spectral.csv")
n=int(out.shape[1]/2)
cols = [["Top indels %s"%(i),"Top indels %s Frequency"%(i)] for i in range(1,n+1)]
print (out)
print (cols)
out.columns = [j for sub in cols for j in sub]
df = pd.concat([df,out],axis=1)
for c in df.columns:
	if "Frequency" in c:
		df[c] = df[c]/df['Total reads']
df.to_csv("summary.csv")



