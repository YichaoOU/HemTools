#!/usr/bin/env python

import pandas as pd

import sys


"""
GACGGGTGCGACCAGAGCGTNGG chr17   1582933 GACGGGTGCGACCAGAGCGTAGG +       0

browser details YourSeq    23     1    23    23   100.0%  chr17  +     1582934   1582956     23

GGACGGGCCTTACATCACAGNGG chr17   1579642 GGACGGGCCTTACATCACAGCGG -       0

browser details YourSeq    23     1    23    23   100.0%  chr17  -     1579643   1579665     23



"""
main_chrs = ["chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX","chrY","chr11_paternal"]
df = pd.read_csv(sys.argv[1],sep="\t",header=None)
df = df[df[1].isin(main_chrs)]
print ("finish reading file %s"%(sys.argv[1]))
print (df.head())

gRNA_length = int(sys.argv[2])
PAM_seq = sys.argv[3]

try:
	filter_G = sys.argv[4]
except:
	filter_G = None
# if filter_G != None:
	# df['first_two'] = [x[0:2] for x in df[3]]
	# df = df[df['first_two']!="CC"]
if df.shape[0]==0:
	print ("no rows, nothing to process")
	exit()
PAM_length = len(PAM_seq)
if PAM_length > 10:
	PAM_length = 0
def row_apply(x):
	if x[4] == "-":
		start = x[2]+PAM_length
	else:
		start = x[2]
	return start
# df['start'] = df.apply(row_apply,axis=1)
df['start'] = df[2]
# df['end'] = 
df['end'] = df['start']+gRNA_length+PAM_length
# df['seq'] = [x.replace(PAM_seq,"") for x in df[0].tolist()]
# df['seq'] = [x.upper()[:gRNA_length] for x in df[3].tolist()]
df['seq'] = [x.upper() for x in df[3].tolist()]
print (df.head())

if filter_G != None:
	df['first_base'] = [x[0] for x in df.seq]
	df = df[df['first_base']=="G"]
	df = df.drop(['first_base'],axis=1)
# df[[1,2,'end','seq',5,4]].to_csv("%s.bed"%(sys.argv[1]),sep="\t",header=False,index=False)
df[[1,'start','end','seq',5,4,0]].to_csv("%s.bed"%(sys.argv[1]),sep="\t",header=False,index=False)

## ABE
def is_ABE(x):
    for i in x[2:7]:
        if i == "A":
            return True
    return False
df['ABE'] = [is_ABE(x) for x in df['seq']]
df = df[df.ABE==True]
df[[1,'start','end','seq',5,4]].to_csv("%s.ABE.bed"%(sys.argv[1]),sep="\t",header=False,index=False)

def is_CBE(x):
    for i in x[2:7]:
        if i == "C":
            return True
    return False
df['CBE'] = [is_CBE(x) for x in df['seq']]
df = df[df.CBE==True]
df[[1,'start','end','seq',5,4]].to_csv("%s.CBE.bed"%(sys.argv[1]),sep="\t",header=False,index=False)