#!/usr/bin/env python
import sys
from Bio.Seq import Seq
from Bio import SeqIO
def write_fasta(file_name,myDict):
	out = open(file_name,"wt")
	for k in myDict:
		out.write(">"+k+"\n")
		out.write(myDict[k]+"\n")
	out.close()
def read_fasta(f):
	my_dict = {}
	for r in SeqIO.parse(f, "fasta"):
		my_dict[r.id] = str(r.seq).upper()
	return my_dict	

## specifically designed for crispe esso in silico PCR
fasta_in = sys.argv[1]
fasta_out = sys.argv[2]
min_length = int(sys.argv[3])
max_length = int(sys.argv[4])

myDict = read_fasta(fasta_in)
outDict = {}
for k in myDict:
    seq = myDict[k]
    if min_length <= len(seq) <= max_length:
        outDict[k] = myDict[k]
write_fasta(fasta_out,outDict)