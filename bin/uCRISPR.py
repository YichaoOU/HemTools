#!/usr/bin/env python


import sys

import os

import argparse

import uuid


def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

def my_args():
	
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument("-i",help="chr_start_end_strand (bed format length should be 23bp)",required=True)	
	mainParser.add_argument('-o',"--output",  help="output file name",required=True)

	## https://stackoverflow.com/questions/21168120/python-argparse-errors-with-in-help-string
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def run_ucrispr(name,final_file):
	chr,start,end,strand = name.split("_")
	


	input = str(uuid.uuid4()).split("-")[-1]+".bed"
	
	write_file(input,"\t".join([chr,start,end,".",".",strand]))
	folder = str(uuid.uuid4()).split("-")[-1]
	temp1 = str(uuid.uuid4()).split("-")[-1]+".tab"
	temp2 = str(uuid.uuid4()).split("-")[-1]+".cut"
	hg19_fa = "/home/yli11/Data/Human/hg19/fasta/hg19.fa"
	command = "mkdir {5};export DATAPATH=/home/yli11/HemTools/share/script/RNAstructure/data_tables; bedtools getfasta -fi {0} -fo {5}/{2} -bed {1} -name -tab -s ; cd {5}; cut -f 2 {2} > {3} ; uCRISPR -on {3} > {4}; mv {4} ../; cd ..".format(hg19_fa,input,temp1,temp2,final_file,folder)
	# print (command)
	os.system(command)
	os.system("rm %s"%(input))
	# os.system("rm %s"%(temp1))
	# os.system("rm %s"%(temp2))
	os.system("rm -r %s"%(folder))

def main():
	args = my_args()
	run_ucrispr(args.i,args.output)
	
	


if __name__ == "__main__":
	main()



