#!/usr/bin/env python

import pandas as pd
import sys
import os
import argparse


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output", help="output file", default="my_table.json")

	# group.add_argument('--outward',  help="get outward reads", action='store_true')
	# group.add_argument('--inward',  help="get inward reads", action='store_true')
	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-p','--pipeline_name',  help="which pipeline to run, e.g., atac_seq")
	group.add_argument("--list_pipelines",  help="list all available pipelines",action='store_true')		
	group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')
	group.add_argument("--user_lsf",  help="user defined lsf file")
	
	
	mainParser.add_argument('-f',"--input",  help="tab delimited any number of columns (tsv file), the last column is output prefix. For example, a paired-end fastq input could be: Read 1 fastq, Read 2 fastq, sample ID")
	mainParser.add_argument('-q',"--queue",  help="submit queue",default="standard")


	mainParser.add_argument('-f2',"--input2",  help="for jobs with dependencies. tab delimited any number of columns (tsv file), the last column is output prefix. For example, a paired-end fastq input could be: Read 1 fastq, Read 2 fastq, sample ID")
	
	
	# mainParser.add_argument("--single",  help="default is paired-end data, specify this parameter if you have single-end data",action='store_true')		
	mainParser.add_argument("--csv",  help="convert tsv to csv when doing guess_input",action='store_true')		
	mainParser.add_argument("--email",  help="send user the fastq.tsv file",action='store_true')		

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="BWA index file", default=myData['hg19_BWA_index'])
	genome.add_argument('-b','--black_list',  help="Blacklist file", default=myData['hg19_black_list'])
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])
	genome.add_argument('-e','--effectiveGenomeSize',  help="effectiveGenomeSize for bamCoverage", default=myPars['hg19_effectiveGenomeSize'])
	mainParser.add_argument('--interactive',  help="run pipeline interatively", action='store_true')

	mainParser.add_argument('-s',"--sample_list",  help="table rows, a list of samples, these are supposed to be folder names, one column",required=True)
	mainParser.add_argument('-f','--feature_list',  help="table columns, map file name to specific feature name",required=True)
	# mainParser.add_argument('--softlinks',  help=argparse.SUPPRESS,default="")
	# mainParser.add_argument('--treatment_bam',  help=argparse.SUPPRESS)
	# mainParser.add_argument('--port',  help=argparse.SUPPRESS)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()



if __name__ == "__main__":
	main()


















