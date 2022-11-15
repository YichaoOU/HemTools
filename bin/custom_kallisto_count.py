#!/usr/bin/env python

import sys
import os
import pandas as pd
import datetime
import getpass
import uuid
import argparse
import glob

"""

Input
-----

target fasta sequence

fastq files


output
------

count table,

each row is a sequence name in the target fasta sequence

each column is a fastq file


Steps
-----

Kallisto build index

Kallisto count

convert sam to bed

bed to count table
"""


def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="merge bedfiles into one")
	mainParser.add_argument('file', type=str, nargs='+')
	mainParser.add_argument('-f',"--fasta",  help="input fasta files",required=True)
	mainParser.add_argument('-o',"--output",  help="output files",required=True)
	mainParser.add_argument('--paired',  help=" PE data", action='store_true')
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	command = "module load kallisto bedops;kallisto index -i myKallistoIndex %s"%(args.fasta)
	os.system(command)
	for f in args.file:
		label = f.split("/")[-1].split(".fastq")[0]
		print (f)
		if args.paired:
			R2 = f.replace("R1","R2")
			command = "module load kallisto bedops;kallisto quant -i myKallistoIndex -o {0}.count --pseudobam {1} {2} > {0}.sam;sam2bed < {0}.sam | cut -f 1-6 - > {0}.bed".format(label,f,R2)
		else:
			command = "module load kallisto bedops;kallisto quant -i myKallistoIndex -o {0}.count --single -l 150 -s 10 --pseudobam {1} > {0}.sam;sam2bed < {0}.sam | cut -f 1-6 - > {0}.bed".format(label,f)
		os.system(command)
		print (command)
	df_list = []
	for f in args.file:
		label = f.split("/")[-1].split(".fastq")[0]
		df = pd.read_csv(label+".bed",sep="\t",header=None)
		
		df = df[df[5]=="+"] # a specific requirement for the insulator project
		df = df.sort_values(3)
		# print (f,"Before dedup",df.shape)
		before_dedup = df.shape[0]
		df = df.drop_duplicates(3)
		print (f,"Before",before_dedup,"After",df.shape[0])
		x=df[0].value_counts()
		x.name=label
		df_list.append(x)
		# os.system("rm {0}.sam; rm {0}.bed".format(label))
	df = pd.concat(df_list,axis=1)
	df = df.fillna(0)
	df.index.name = "sgRNA"
	current_columns = df.columns.tolist()
	df = df.reset_index()
	df['Gene'] = df.sgRNA.tolist()
	df = df[['sgRNA',"Gene"]+current_columns]
	df.to_csv(args.output,sep="\t",index=False)
	
if __name__ == "__main__":
	main()






















































