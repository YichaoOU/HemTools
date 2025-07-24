#!/usr/bin/env python


import re
import gzip
import sys
import os
import itertools
# from Bio import SeqUtils
import pandas as pd
from fast_edit_distance import edit_distance

# -------------------- helper functions -----------------------

def fq(file):
    if re.search('.gz$', file):
        fastq = gzip.open(file, 'rt')
    else:
        fastq = open(file, 'r')
    with fastq as f:
        while True:
            l1 = f.readline().strip()
            if not l1:
                break
            l2 = f.readline().strip()
            l3 = f.readline().strip()
            l4 = f.readline().strip()
            yield [l1, l2, l3, l4]


input=sys.argv[1]
read = fq(input)
myDict={}
for r in read:
	
	seq=r[1]
	if seq in myDict:
		myDict[seq]+=1
	else:
		flag=True
		for key_seq in myDict:
			X = min(max(int(len(key_seq)*0.002)+1,10),20)
			if edit_distance(seq, key_seq, max_ed=X) <= X:
				myDict[key_seq]+=1
				flag=False
				break
		if flag:
			myDict[seq]=1
	if len(myDict)%1000==0:
		print (len(myDict))
		
		
		
		
		
		
df = pd.DataFrame.from_dict(myDict,orient="index")
df = df.sort_values(0,ascending=False)
print ("Input File has N unique reads: %s %s"%(input,df.shape[0]))
print (df)
df.to_csv(input+".unique_read_count.csv",header=False)
