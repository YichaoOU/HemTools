#!/usr/bin/env python

import gzip
import sys
import re


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


def rename(file,outFile):

	total_count = 0
	outlines = []
	for read in fq(file):
		total_count += 1
		if total_count % 100000 == 0:
			print(total_count)
		name,barcode = read[0].strip().split()
		umi = barcode.split(":")[-1]
		name = name+"_"+umi
		outlines.append(name+"\n")
		outlines.append(read[1])
		outlines.append(read[2])
		outlines.append(read[3])
	output_to_fastq_gz(outFile,outlines)


rename(sys.argv[1],sys.argv[2])
