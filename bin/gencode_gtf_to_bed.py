#!/hpcf/apps/python/install/2.7.13/bin/python


import sys
import pandas as pd

infile = sys.argv[1]
outfile = "_".join(infile.split(".")[:2])

df = pd.read_csv(infile,sep="\t",comment="#",header=None)
df2 = df[df[2]=="gene"]
df2['gene_name']=[x.split('gene_name "')[-1].split('";')[0] for x in df2[8]]
df2['gene_name_length'] = [len(x) for x in df2.gene_name]
print (df2['gene_name_length'].unique())

df3 = df2[df2[6]=="+"]
df4 = df2[df2[6]=="-"]
df3['start'] = df3[3]
df3['end'] = df3[3]+1
df4['end'] = df4[4]+1
df4['start'] = df4[4]
df5 = pd.concat([df3,df4])


df5[[0,"start","end","gene_name",5,6]].to_csv("%s.tss.bed"%(outfile),index=False,header=False,sep="\t")


df5[[0,3,4,"gene_name",5,6]].to_csv("%s.gene_body.bed"%(outfile),index=False,header=False,sep="\t")



