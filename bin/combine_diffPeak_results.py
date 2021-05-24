#!/hpcf/apps/python/install/2.7.13/bin/python


import glob
import pandas as pd
import sys
deseq_results = glob.glob("*/control*txt")[0]
count_table = glob.glob("*/*count_table.bed")[0]

name_pattern = sys.argv[1]

def parse_df(x,sel_cols,name_pattern=None):
	df = pd.read_csv(x,sep="\t",index_col=0)
	addtional_cols = []
	if name_pattern:
		for c in df.columns:
			if name_pattern in c:
				addtional_cols.append(c)
	addtional_cols = sorted(addtional_cols)
	return df[sel_cols+addtional_cols]
	
	
deseq = parse_df(deseq_results,['logFC','adj.P.Val'])
count = parse_df(count_table,['Chr','Start','End'],name_pattern)

df = pd.concat([count,deseq],axis=1)

print ("deseq",deseq.shape)
print ("count",count.shape)
print ("df",df.shape)

df.to_csv("%s.DESEQ2.csv"%(name_pattern))


















