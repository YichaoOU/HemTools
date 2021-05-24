#!/home/yli11/.conda/envs/Sci_L3/bin/python

import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
import argparse
import gzip
# from Bio.Seq import Seq
# from Bio import SeqIO
import logging
import Colorer
import itertools
import subprocess
import sys
from Levenshtein import distance
import gzip
from multiprocessing import Pool
from functools import partial
import os
import argparse
import pandas as pd
import subprocess
import glob
def revcomp(seq):
	try: ## python2
		import string
		tab = string.maketrans(b"ACTG", b"TGAC")
	except:  ## python3
		tab = bytes.maketrans(b"ACTG", b"TGAC")
	return seq.translate(tab)[::-1]


def setup_custom_logger(jid):
	logFormatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
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

	mainParser.add_argument("-r1","--read1",  help="R1 fastq file", required=True)
	mainParser.add_argument("-r2","--read2",  help="R2 fastq file", required=True)
	mainParser.add_argument("--sample_ID",  help="sample_ID", required=True)
	mainParser.add_argument("--barcode_1_list",  help="list of barcodes 1", required=True)
	mainParser.add_argument("--barcode_2_list",  help="list of barcodes 2", required=True)
	mainParser.add_argument("--barcode_3_list",  help="list of barcodes 3", required=True)
	mainParser.add_argument("--BC1_error",  help="barcode 1 allowed number of mismatches", type=int,default=1)
	mainParser.add_argument("--BC2_error",  help="barcode 2 allowed number of mismatches", type=int,default=1)
	mainParser.add_argument("--BC3_error",  help="barcode 3 allowed number of mismatches", type=int,default=1)
	mainParser.add_argument("--spacer1_length",  help="spacer1_length", type=int, default=15)
	mainParser.add_argument("--barcode1_length",  help="barcode1_length", type=int, default=8)
	mainParser.add_argument("--spacer2_length",  help="spacer2_length", type=int, default=30)
	mainParser.add_argument("--barcode2_length",  help="barcode2_length", type=int, default=8)
	mainParser.add_argument("--spacer3_length",  help="spacer3_length", type=int, default=30)
	mainParser.add_argument("--barcode3_length",  help="barcode3_length", type=int, default=8)
	mainParser.add_argument("--revcomp",  help="reverse complement barcode sequence",action='store_true')

	mainParser.add_argument('--input', help=argparse.SUPPRESS)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def dict3d_to_df(x):
	bc3 = []
	bc2 = []
	bc1 = []
	counts = []
	for i in x:
		for j in x[i]:
			for k in x[i][j]:
				bc1.append(i)
				bc2.append(j)
				bc3.append(k)
				counts.append(x[i][j][k])
	df = pd.DataFrame()
	df['barcode_1'] = bc1
	df['barcode_2'] = bc2
	df['barcode_3'] = bc3
	df['total_reads'] = counts
	df = df.sort_values("total_reads",ascending=False)
	return df
	

def k_mer_distance(k,error):
	out_dict={}
	bases=['A','T','G','C']
	k_mer = [''.join(p) for p in itertools.product(bases, repeat=k)]
	for ii in range(len(k_mer)):
		i = k_mer[ii]
		out_dict[i]={}
		for jj in range(ii,len(k_mer)):
			j = k_mer[jj]
			dist = distance(i, j)
			# dist = 0
			# if i != j:
				# dist = 1
			if dist <= error:
				out_dict[i][j] = dist
				if not j in out_dict:
					out_dict[j]={}
				out_dict[j][i] = dist
	return out_dict

def get_barcode_dict(bc1,bc2,bc3):
	out = {}
	for i in bc1:
		out[i]={}
		for j in bc2:
			out[i][j]={}
			for k in bc3:
				out[i][j][k]=0
	return out

def find_dist(kmer_dict,target_barcode,barcode_list):
	for x in barcode_list:
		try:
			kmer_dict[x][target_barcode] 
			return True,x
		except:
			pass
	return False,None
	


def output_to_fastq_gz(file_name,list_of_lines):
	f = gzip.open(file_name,"wb")
	[f.write(x) for x in list_of_lines]
	f.close()

def share_seq_demultiplexing(Read1,Read2,label, barcode_1_list, barcode_2_list, barcode_3_list, BC1_error, BC2_error, BC3_error,sp1_length,bc1_length,sp2_length,bc2_length,sp3_length,bc3_length):
	"""general utils for demultiplexing read in PE mode
	
	
	"""
	
	output_folder = label+"_renamed_fastq"
	
	logging.info("Output fastq files will be stored in %s"%(output_folder))
	os.system("mkdir -p %s"%(output_folder))
	
	
	barcode_dict = get_barcode_dict(barcode_1_list,barcode_2_list,barcode_3_list) # used to count reads
	
	junk_list_R1 = []
	junk_list_R2 = []
	matched_list_R1 = []
	matched_list_R2 = []
	f1 = gzip.open(Read1)
	f2 = gzip.open(Read2)	
	logging.info("Using BC3 error: %s"%(BC3_error))
	# edit distance is better than hamming distance
	bc3_kmer = k_mer_distance(bc3_length,BC3_error)
	# bc2_kmer = k_mer_distance(bc2_length,BC2_error)
	# bc1_kmer = k_mer_distance(bc1_length,BC1_error)
	# bc3_kmer = None
	bc2_kmer = bc3_kmer
	bc1_kmer = bc3_kmer
	logging.info("Finish enumerate possible kmers")
	bc1_start = sp1_length
	bc1_end = bc1_start+bc1_length
	bc2_start = bc1_end+sp2_length
	bc2_end = bc2_start+bc2_length
	bc3_start = bc2_end+sp3_length
	bc3_end = bc3_start+bc3_length
	
	bc3_count =0
	bc2_count =0
	bc1_count =0
	line1 = f1.readline()
	line2 = f2.readline()
	count = 0
	total_valid_reads = 0
	while (line1):
		count +=1
		if count % 10000 == 0:
			logging.info("%s reads processed"%(count))
		name,barcode_r1 = line1.split()
		# print (line2)
		_ = line2.split()
		name_r1 = name +" 1\n"
		name_r2 = name +" 2\n"
		barcode_r1 = barcode_r1.split(":")[-1]

		line1 = f1.readline()
		line2 = f2.readline()
		bc3 = barcode_r1[bc3_start:bc3_end]
		bc2 = barcode_r1[bc2_start:bc2_end]
		bc1 = barcode_r1[bc1_start:bc1_end]
		# print (barcode_r1,bc1,bc2,bc3)
		bc1_dist,barcode_1 = find_dist(bc1_kmer,bc1,barcode_1_list)
		bc2_dist,barcode_2 = find_dist(bc2_kmer,bc2,barcode_2_list)
		bc3_dist,barcode_3 = find_dist(bc3_kmer,bc3,barcode_3_list)

		if bc1_dist:
			bc1_count+=1
		if bc2_dist:
			bc2_count+=1
		if bc3_dist:
			bc3_count+=1

		if bc1_dist and bc2_dist and bc3_dist :
			barcode_dict[barcode_1][barcode_2][barcode_3]+=1
			first_line_r1 = '@' + ",".join(["NNNN",barcode_1,barcode_2,barcode_3]) + ',' + name_r1[1:]
			first_line_r2 = '@' + ",".join(["NNNN",barcode_1,barcode_2,barcode_3])+ ',' + name_r2[1:]
			matched_list_R1.append(first_line_r1)
			matched_list_R2.append(first_line_r2)

			matched_list_R1.append(line1)
			matched_list_R2.append(line2)	
			
			third_line_r1 = f1.readline()
			third_line_r2 = f2.readline()
			matched_list_R1.append(third_line_r1)
			matched_list_R2.append(third_line_r2)	
	
			four_line_r1 = f1.readline()
			four_line_r2 = f2.readline()
			matched_list_R1.append(four_line_r1)
			matched_list_R2.append(four_line_r2)	
			total_valid_reads += 1

		else:
			junk_list_R1.append(name_r1)
			junk_list_R2.append(name_r2)
			junk_list_R1.append(line1)
			junk_list_R2.append(line2)
			
			third_line_r1 = f1.readline()
			third_line_r2 = f2.readline()
			junk_list_R1.append(third_line_r1)
			junk_list_R2.append(third_line_r2)	
	
			four_line_r1 = f1.readline()
			four_line_r2 = f2.readline()
			junk_list_R1.append(four_line_r1)
			junk_list_R2.append(four_line_r2)	
				
			
		line1 = f1.readline()
		line2 = f2.readline()

	junk_R1_output = output_folder + "/" + label + ".junk.R1.fastq.gz"
	junk_R2_output = output_folder + "/" + label + ".junk.R2.fastq.gz"
	output_to_fastq_gz(junk_R1_output,junk_list_R1)
	output_to_fastq_gz(junk_R2_output,junk_list_R2)
	
	matched_R1_output = output_folder + "/" + label + ".matched.R1.fastq.gz"
	matched_R2_output = output_folder + "/" + label + ".matched.R2.fastq.gz"
	output_to_fastq_gz(matched_R1_output,matched_list_R1)
	output_to_fastq_gz(matched_R2_output,matched_list_R2)
	df = dict3d_to_df(barcode_dict)
	df.to_csv(output_folder + "/" + label + ".total_number_reads.tsv",sep="\t",index=False)
	print ("Sample: %s has %s BC1 %s BC2 %s BC3"%(label,bc1_count,bc2_count,bc3_count))
	print ("Sample: %s has %s total valid reads"%(label,total_valid_reads))

def main():

	args = my_args()
	
	# read barcode
	logging.info("Reading barcode file")
	barcode_1_list = pd.read_csv(args.barcode_1_list,header=None)[0].tolist()
	barcode_2_list = pd.read_csv(args.barcode_2_list,header=None)[0].tolist()
	barcode_3_list = pd.read_csv(args.barcode_3_list,header=None)[0].tolist()
	
	
	barcode_1_list = [x.replace(" ","") for x in barcode_1_list]
	barcode_2_list = [x.replace(" ","") for x in barcode_2_list]
	barcode_3_list = [x.replace(" ","") for x in barcode_3_list]
	if args.revcomp:
		barcode_1_list = [revcomp(x) for x in barcode_1_list]
		barcode_2_list = [revcomp(x) for x in barcode_2_list]
		barcode_3_list = [revcomp(x) for x in barcode_3_list]
	# sci_l3_demultiplexing(args.read1,args.read2,args.sample_ID, barcode_1_list, barcode_2_list, barcode_3_list, args.BC1_error, args.BC2_error, args.BC3_error,args.UMI_length,args.bc3_length,args.sp2_length,args.bc2_length,args.sp1_length,args.bc1_length)
	share_seq_demultiplexing(args.read1,args.read2,args.sample_ID, barcode_1_list, barcode_2_list, barcode_3_list, args.BC1_error, args.BC2_error, args.BC3_error,args.spacer1_length,args.barcode1_length,args.spacer2_length,args.barcode2_length,args.spacer3_length,args.barcode3_length)
	
if __name__ == "__main__":
	main()

























