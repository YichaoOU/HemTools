#!/usr/bin/env python


import re
import gzip
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
# -------------------- helper functions -----------------------

def fq(file):
    if re.search('.gz$', file):
        fastq = gzip.open(file, 'rb')
    else:
        fastq = open(file, 'r')
    with fastq as f:
        while True:
            l1 = f.readline().rstrip('\n')
            if not l1:
                break
            l2 = f.readline().rstrip('\n')
            l3 = f.readline().rstrip('\n')
            l4 = f.readline().rstrip('\n')
            yield [l1, l2, l3, l4]

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

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o1',  help="output R1 fastq file name", required=True)	
	mainParser.add_argument('-o2',  help="output R2 fastq file name", required=True)	
	mainParser.add_argument('-r1',  help="read1 fastq", required=True)	
	mainParser.add_argument('-r2',  help="read2 fastq", required=True)	
	mainParser.add_argument('-i1',  help="index1 fastq", required=True)	
	mainParser.add_argument('-i2',  help="index2 fastq", required=True)	

	# mainParser.add_argument('--config_list',help=argparse.SUPPRESS)


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	logging.info("Reading read fastq")
	read1 = fq(args.r1)
	read2 = fq(args.r2)
	logging.info("Reading index fastq")
	index1 = fq(args.i1)
	index2 = fq(args.i2)
	logging.info("Writing merged fastq")
	o1 = gzip.open(args.o1, 'wb')
	o2 = gzip.open(args.o2, 'wb')

	for r1,r2,i1,i2 in itertools.izip(read1, read2,index1,index2):

		read_name = r1[0].split()[0]
		index1 = i1[1]
		index2 = i2[1]
		read_name_long1 = "%s 1:N:0:%s+%s"%(read_name,index1,index2)
		read_name_long2 = "%s 2:N:0:%s+%s"%(read_name,index1,index2)
		
		# print(read_name_long1, file=o1)
		# print(read_name_long2, file=o2)
		
		# print(r1[1], file=o1)
		# print(r2[1], file=o2)
		
		# print(r1[2], file=o1)
		# print(r2[2], file=o2)
		
		# print(r1[3], file=o1)
		# print(r2[3], file=o2)
		
		o1.write(read_name_long1+"\n")
		o1.write(r1[1]+"\n")
		o1.write(r1[2]+"\n")
		o1.write(r1[3]+"\n")

		o2.write(read_name_long2+"\n")
		o2.write(r2[1]+"\n")
		o2.write(r2[2]+"\n")
		o2.write(r2[3]+"\n")


if __name__ == "__main__":
	main()






