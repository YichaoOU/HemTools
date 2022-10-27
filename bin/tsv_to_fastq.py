#!/usr/bin/env python

import sys
import pandas as pd
import os

# discard reads less than 25bp
min_length = 25
input = sys.argv[1]
output = sys.argv[2]


def write_fasta(file_name,myDict):
	out = open(file_name,"wt")
	for k in myDict:
		out.write(">"+k+"\n")
		out.write(myDict[k]+"\n")
	out.close()
def parse_tsv(f):
	df = pd.read_csv(f,sep="\t",header=None,index_col=0,names = list(range(12)))
	df = df[df[1]!=-1]
	df = df.fillna("")
	df['len'] = [len(x) for x in df[6]]
	df = df[df['len']>=min_length]
	return df
	
df = parse_tsv(input)
write_fasta(output+".fa",df[6].to_dict())

command = "module load bbmap/37.28; reformat.sh in={0}.fa out={0}.fastq qfake=35;gzip {0}.fastq".format(output)
print (command)
os.system(command)