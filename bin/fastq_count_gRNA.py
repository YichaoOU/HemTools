#!/usr/bin/env python


import re
import gzip
import sys
import os
import itertools
from Bio import SeqUtils
import pandas as pd
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

def find_gRNA(seq):
    for i in range(17,24):
        gRNA="N"*i
        pattern = f"CACCG{gRNA}GTTTT"
        ss = SeqUtils.nt_search(seq, pattern)
        if len(ss) > 1:
            start = ss[1]+5
            return seq[start:(start+len(gRNA))]
    return "No_match"
input=sys.argv[1]


read = fq(input)
gRNA_list = []
no_match_list = []
for r in read:
	seq=r[1]
	label = find_gRNA(seq)
	gRNA_list.append(label)
	if label == "No_match":
		no_match_list.append(seq)
df = pd.DataFrame(gRNA_list)
counts = df[0].value_counts()
counts.to_csv(input+".gRNA_counts.tsv",sep="\t",header=False)
pd.DataFrame(no_match_list).to_csv(input+".no_match.list",header=False,index=False)