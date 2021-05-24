#!/hpcf/apps/python/install/2.7.13/bin/python
# exec(open("/home/yli11/HemTools/bin/change_seq_off_target_bed.py").read())


import sys
import pandas as pd
import numpy as np
import os

file = sys.argv[1]
is_PAM_end = int(sys.argv[2])
PAM_length = int(sys.argv[3])

if is_PAM_end == 0:
	print ("not implemented")
	exit()

df = pd.read_csv(file,sep="\t")
df['Site_Sequence'] = df['Site_Sequence'].fillna("")
def get_seq(r):
	
	if r['Site_Sequence'] != "":
		return r['Site_Sequence']
	else:
		# print (r.name,r['Site_Sequence_Gaps_Allowed'].replace("-",""))
		return r['Site_Sequence_Gaps_Allowed'].replace("-","")
		
print (df.shape)
df['seq'] = df.apply(get_seq,axis=1)
df['seq'] = [x[:-PAM_length] for x in df.seq]
df['seq_length'] = [len(x) for x in df.seq]



def get_new_start(r,PAM_length):
	if r['Strand'] == "+":
		return r['Start']
	else:
		return r['Start']+PAM_length

df['new_start'] = df.apply(lambda r:get_new_start(r,PAM_length),axis=1)

df['new_end'] = df['new_start']+df['seq_length']

df[['#Chromosome','new_start','new_end','seq','Nuclease_Read_Count','Strand']].to_csv("test.bed",sep="\t",header=False,index=False)
command = "module load bedtools/2.25.0;bedtools getfasta -fi /home/yli11/Data/Human/hg38/fasta/hg38.fa -fo test.tab -bed test.bed -s -name -tab"
os.system(command)
tmp = pd.read_csv("test.tab",sep="\t",header=None)
for a,b in tmp.values:
	if a.upper() != b.upper():
		print (a,b)

for s,d in df.groupby('seq_length'):
	out = "off_target_%sbp.bed"%(s)
	d[['#Chromosome','new_start','new_end','seq','Nuclease_Read_Count','Strand','Genomic Coordinate']].to_csv(out,sep="\t",header=False,index=False)
	
	
	
	
	