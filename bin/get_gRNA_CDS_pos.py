#!/usr/bin/env python
import swifter
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO
import numpy as np
def read_fasta(f):
	my_dict = {}
	for r in SeqIO.parse(f, "fasta"):
		my_dict[r.id] = str(r.seq).upper()
	return my_dict	
CDS=read_fasta("/home/yli11/Data/Human/hg38/annotations/gencode_v47/CDS.fa")
def revcomp(seq):
	try: ## python2
		tab = string.maketrans(b"ACTGactg", b"TGACtgac")
	except:  ## python3
		tab = bytes.maketrans(b"ACTGactg", b"TGACtgac")
	return seq.translate(tab)[::-1]
gid = pd.read_csv("/home/yli11/Data/Human/hg38/annotations/gencode_v47/gencode.v47.TID.GName.tsv",sep="\t")
def get_CDS_pos(x,seq):
    x_revcomp = revcomp(x)
    # print (x,x_revcomp)
    if x in seq:
        return seq.index(x)
    if x_revcomp in seq:
        return seq.index(x_revcomp)
    return -1
def row_apply_CDS_pos(r):
    tlist = gid[gid.Gene_Name==r.Gene].Transcript_ID.tolist()
    # print (tlist)
    pos_list = []
    for t in tlist:
        try:
            # print (CDS[t])
            p=get_CDS_pos(r.seq,CDS[t])
            # print ("P",p)
            if p>-1:
                pos_list.append(p/len(CDS[t]))
        except:
            continue
    if len(pos_list)==0:
        return -1
    return np.mean(pos_list)
import sys
file = sys.argv[1]
df = pd.read_csv(file,sep="\t")

df['CDS%'] = df.swifter.apply(row_apply_CDS_pos,axis=1)
df.to_csv(f"{file}.addCDS.csv",index=False)