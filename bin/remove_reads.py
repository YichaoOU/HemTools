#!/usr/bin/env python

import pandas as pd
import sys
import os
import argparse

import datetime

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default="rm_reads_"+str(datetime.date.today()))	

	mainParser.add_argument('-f',"--input",  help="tab delimited any number of columns (tsv file), the last column is output prefix. For example, a paired-end fastq input could be: Read 1 fastq, Read 2 fastq, sample ID",required=True)
	mainParser.add_argument('-fa',  help="fasta file, reads mapped here will be removed",required=True)



	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	
	# bwa index
	
	# bwa mem
	
	# samtools filter
	
	
	# bbmap remove
	
	
	command1=""



if __name__ == "__main__":
	main()




