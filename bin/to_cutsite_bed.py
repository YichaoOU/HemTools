#!/usr/bin/env python
import sys
import os
import pandas as pd
import argparse

"""

myBaseName=$(basename -- ${COL1})

sort -k1,1 -k2,2n ${COL1} > {{jid}}/${myBaseName}.sorted
cd {{jid}}
module load ucsc/041619
bedGraphToBigWig ${myBaseName}.sorted {{chrom_size}} ${myBaseName%.sorted}.bw

"""

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output",  help="output file name, 4 columns", default="cutsite.bed")

	mainParser.add_argument('-f',"--input",  help="input bed file, 6 columns, chr, start, end, seq, value, strand",required=True)

	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument("--offset",  help="use cas9 cut site (e.g., -3) as gRNA score",type=int)
	group.add_argument('--ABE',  help="ABE mode not implemented", action='store_true')
	group.add_argument('--CBE',  help="CBE mode not implemented", action='store_true')


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def get_gRNA_cut_site(start,end,strand,offset=-3):
	# return 1-index pos
	# cut site = the first base before cut near PAM direction

	if strand == "+":
		return int(end + offset)
	if strand == "-":
		return int(start - offset +1)


def main():

	args = my_args()

	##------- add functions below ----------------------

	# read bed
	df = pd.read_csv(args.input,sep="\t",header=None)
	
	## re position
	if args.offset:
		df['end'] = df.apply(lambda r:get_gRNA_cut_site(r[1],r[2],r[5],args.offset),axis=1)
		df['start'] = df['end']-1
		
	df[[0,'start','end',3]].to_csv(args.output,sep="\t",header=False,index=False)

	
if __name__ == "__main__":
	main()

























