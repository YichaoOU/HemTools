#!/hpcf/apps/python/install/2.7.13/bin/python

import sys
import pandas as pd

fimo = sys.argv[1]
flag=""
try:
	flag = sys.argv[2]
except:
	pass
df = pd.read_csv(fimo,sep="\t")
df['name'] = df['#pattern name']
# df['name'] = df['sequence name']+df['start'].astype(str)+df['stop'].astype(str)
df['start'] = df['start']-1
# df = df.drop_duplicates('name')
if flag == "mode":
	start = df['start'].mode().tolist()[0]-1
	stop = df['stop'].mode().tolist()[0]+1
	df['start']=start
	df['stop']=stop
	df[['sequence name','start','stop']].to_csv("%s.mode.bed"%(fimo),sep="\t",header=False,index=False)
else:
	if flag !="":
		df['name'] = flag
	df[['sequence name','start','stop','name','score','strand']].to_csv("%s.bed"%(fimo),sep="\t",header=False,index=False)
	df[['sequence name','start','stop','matched sequence','score','strand']].to_csv("%s.seq.bed"%(fimo),sep="\t",header=False,index=False)
	df[['sequence name','start','stop','matched sequence','p-value','strand']].to_csv("%s.pvalue.bed"%(fimo),sep="\t",header=False,index=False)













