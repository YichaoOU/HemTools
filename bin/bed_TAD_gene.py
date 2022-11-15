#!/usr/bin/env python


import sys
import os
import uuid
import pandas as pd
## used to find genes that are in the same TAD as input peaks
uid = str(uuid.uuid4()).split("-")[-1]

peaks = sys.argv[1]
tad = sys.argv[2]
gtf = sys.argv[3]

def gtf_to_simple_bed(f,out):
	df = pd.read_csv(f,sep="\t",header=None,comment="#")
	df['name'] = df[8].apply(lambda x:x.split("gene_name")[-1].split()[0].replace('"','').replace(';',''))
	df[[0,3,4,"name"]].to_csv(out,sep="\t",header=False,index=False)

# command1 = "module load bedtools;bedtools intersect -a %s -b %s -u > %s.step1"%(tad,peaks,uid)
# os.system(command1)
# out = "%s.bed"%(uid)
# gtf_to_simple_bed(gtf,out)
# command2 = "module load bedtools;bedtools intersect -b %s.step1 -a %s.bed -u > %s.TAD.gene.bed;rm %s*"%(uid,uid,peaks,uid)
# os.system(command2)

command1 = "module load bedtools;bedtools intersect -a %s -b %s -wa -wb > %s.step1"%(tad,peaks,uid)
os.system(command1)
out = "%s.bed"%(uid)
gtf_to_simple_bed(gtf,out)
command2 = "module load bedtools;bedtools intersect -a %s.step1 -b %s.bed -wa -wb > %s.TAD.gene.bed;rm %s*"%(uid,uid,peaks,uid)
os.system(command2)

# import pandas as pd


