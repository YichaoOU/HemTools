#!/hpcf/apps/python/install/2.7.13/bin/python


import pandas as pd
import sys

def guess_sep(x):
	with open(x) as f:
		for line in f:
			tmp1 = len(line.strip().split(","))
			tmp2 = len(line.strip().split("\t"))
			# print (tmp1,tmp2)
			if tmp1 > tmp2:
				return ","
			if tmp2 > tmp1: 
				return "\t"
			else:
				print ("Can't determine the separator. Please input manually")
				exit()
				

liyc = pd.read_csv(sys.argv[1],sep=guess_sep(sys.argv[1]))

seq_len = int(sys.argv[2])
liyc['strand'] = liyc['strand'].map({'+':'D','-':'R'})
liyc['start1'] = liyc['start'] - seq_len
liyc['stop1'] = liyc['stop'] - seq_len
liyc['site'] = "site"
liyc = liyc[['sequence name','site','#pattern name','strand','start1','stop1']]
liyc['sequence name'] = liyc['sequence name'].apply(lambda x:x.split("|")[0])

try:
	liyc_motifs = str(sys.argv[3]).split(",")
except:
	liyc_motifs = list(set(liyc['#pattern name'].tolist()))
liyc = liyc[liyc['#pattern name'].isin(liyc_motifs)]

liyc.to_csv("feature_map.tsv",index=False,header=False,sep="\t")











