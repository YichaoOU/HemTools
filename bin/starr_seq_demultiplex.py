#!/usr/bin/env python

import gzip
import sys
import re
from Levenshtein import distance


def fq(file):
	if re.search('.gz$', file):
		fastq = gzip.open(file, 'rt')
	else:
		fastq = open(file, 'r')
	with fastq as f:
		while True:
			l1 = f.readline()
			if not l1:
				break
			l2 = f.readline()
			l3 = f.readline()
			l4 = f.readline()
			yield [l1, l2, l3, l4]

def output_to_fastq_gz(file_name,list_of_lines):
	f = gzip.open(file_name,"wt")
	[f.write(x) for x in list_of_lines]
	f.close()


def demulti(file,outFile,DNA_BC1,DNA_BC2,RNA_BC,num_mismatch):

	total_count = 0
	outlines_DNA = []
	outlines_RNA = []
	for read in fq(file):
		total_count += 1
		if total_count % 100000 == 0:
			print(total_count,len(outlines_DNA),len(outlines_RNA))
		name,barcode = read[0].strip().split()
		barcode = barcode.split(":")[-1].split("+")
		# print (barcode)
		# exit()
		R1 = barcode[0]
		R2 = barcode[1]
		RNA_dist = distance(R2[:8], RNA_BC)
		if RNA_dist<=num_mismatch: # RNA_read
			name = name + "_" + R1
			outlines_RNA.append(name+"\n")
			outlines_RNA.append(read[1])
			outlines_RNA.append(read[2])
			outlines_RNA.append(read[3])
		else:
			DNA_dist1 = distance(R1[:8], DNA_BC1)
			DNA_dist2 = distance(R2[:8], DNA_BC2)
			if DNA_dist1<=num_mismatch and DNA_dist2<=num_mismatch:
				outlines_DNA.append(name+"\n")
				outlines_DNA.append(read[1])
				outlines_DNA.append(read[2])
				outlines_DNA.append(read[3])
	output_to_fastq_gz(outFile.replace("type","RNA"),outlines_RNA)
	output_to_fastq_gz(outFile.replace("type","DNA"),outlines_DNA)

DNA_BC1=sys.argv[1]
DNA_BC2=sys.argv[2]
RNA_BC=sys.argv[3]
num_mismatch=int(sys.argv[4])


R1="Undetermined_S0_R1_001.fastq.gz"
R2="Undetermined_S0_R2_001.fastq.gz"

demulti(R1,"type.R1.fastq.gz",DNA_BC1,DNA_BC2,RNA_BC,num_mismatch)
demulti(R2,"type.R2.fastq.gz",DNA_BC1,DNA_BC2,RNA_BC,num_mismatch)