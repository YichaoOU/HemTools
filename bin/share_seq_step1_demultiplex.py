#!/usr/bin/env python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
import argparse
import gzip
from Bio.Seq import Seq
from Bio import SeqIO
import logging
import Colorer
import itertools
import string

def revcomp(seq):
	try: ## python2
		tab = string.maketrans(b"ACTG", b"TGAC")
	except:  ## python3
		tab = bytes.maketrans(b"ACTG", b"TGAC")
	return seq.translate(tab)[::-1]


def mismatch_sequence(seq,n):
	bases=['A','T','G','C']
	k_mer = [''.join(p) for p in itertools.product(bases, repeat=len(seq))]
	result = []
	for k in k_mer:
		if hamming_distance(seq,k)<=n:
			result.append(k)
	return result

def hamming_distance(s1, s2):
	return sum(ch1 != ch2 for ch1,ch2 in zip(s1,s2))

def setup_custom_logger(jid):
	logFormatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
	rootLogger = logging.getLogger("root")
	fileHandler = logging.FileHandler(jid+".log")
	fileHandler.setFormatter(logFormatter)
	rootLogger.addHandler(fileHandler)
	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	rootLogger.addHandler(consoleHandler)
	rootLogger.setLevel(logging.INFO)
	return rootLogger

current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	# mainParser.add_argument('-o',"--output",  help="output fastq file name", default="output.fastq.gz")	
	mainParser.add_argument('-r1',  help="input undetermined R1 fastq.gz", required=True)	
	mainParser.add_argument('-r2',  help="input undetermined R2 fastq.gz", required=True)	
	mainParser.add_argument('-b',"--barcode",  help="barcode file in fasta format", required=True)	
	mainParser.add_argument('-n',"--num_mismatch",  help="number of mismatch allowed", default=1,type=int)	
	mainParser.add_argument("--revcomp",  help="revcomp barcode",action='store_true')
	# mainParser.add_argument('--config_list',help=argparse.SUPPRESS)


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def read_fasta(f,rc=False):
	my_dict = {}
	for r in SeqIO.parse(f, "fasta"):
		seq = str(r.seq).upper()
		if rc:
			seq = revcomp(seq)
		my_dict[r.id] = seq
	return my_dict	
	

def main():

	args = my_args()
	
	# read barcode
	barcode = read_fasta(args.barcode,rc = args.revcomp)
	print (barcode)
	# open files
	R1 = {}
	R2 = {}
	for b in barcode:
		R1[barcode[b]] = gzip.open("%s.R1.fastq.gz"%(b), 'wb')
		R2[barcode[b]] = gzip.open("%s.R2.fastq.gz"%(b), 'wb')
		
	# add mismatch
	if args.num_mismatch>0:
		for b in barcode:
			print (b)
			for k in mismatch_sequence(barcode[b],args.num_mismatch):
				R1[k] = R1[barcode[b]]
				R2[k] = R2[barcode[b]]
	
	R1['unmatched'] = gzip.open("unmatched.R1.fastq.gz", 'wb')
	R2['unmatched'] = gzip.open("unmatched.R2.fastq.gz", 'wb')
	# read fastq
	logging.info("Reading barcode file")
	n = 4
	count = 0
	# https://www.biostars.org/p/317524/
	with gzip.open(args.r1, 'r') as fh:
		lines = []
		for line in fh:
			lines.append(line.strip())
			if len(lines) == n:
				# print (lines)
				
				# logging.info("%s reads processed"%(count))
				if count %50000 == 0:
					# print (count,"reads has been processed")
					logging.info("%s matched reads processed"%(count))
				# @NB551526:91:HC27NAFX2:1:11101:17620:1055 1:N:0:CTGCCTAA
				myString = lines[0].split("+")[-1]
				# print (myString)
				try:
					count += 1
					R1[myString].write("\n".join(lines)+"\n")
				except:
					R1['unmatched'].write("\n".join(lines)+"\n")
				lines=[]

	n = 4
	count = 0
	# https://www.biostars.org/p/317524/
	with gzip.open(args.r2, 'r') as fh:
		lines = []
		for line in fh:
			lines.append(line.strip())
			if len(lines) == n:
				# print (lines)
				
				# logging.info("%s reads processed"%(count))
				if count %50000 == 0:
					# print (count,"reads has been processed")
					logging.info("%s matched reads processed"%(count))
				# @NB551526:91:HC27NAFX2:1:11101:17620:1055 1:N:0:CTGCCTAA
				myString = lines[0].split("+")[-1]
				# print (myString)
				try:
					count += 1
					R2[myString].write("\n".join(lines)+"\n")
				except:
					R2['unmatched'].write("\n".join(lines)+"\n")
				lines=[]

	
if __name__ == "__main__":
	main()

























