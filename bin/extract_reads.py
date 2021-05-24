#!/hpcf/apps/python/install/2.7.13/bin/python


import pysam
import sys
import argparse
import datetime
import pandas as pd
# bam=sys.argv[1]

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output",  help="output table name", default="extract_reads_"+str(datetime.date.today())+".csv")

	mainParser.add_argument('-f',"--bam_file",  help="input bam file")

	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('--outward',  help="get outward reads", action='store_true')
	group.add_argument('--inward',  help="get inward reads", action='store_true')
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def read_pair_generator(bam, region_string=None):
	"""
	Generate read pairs in a BAM file or within a region string.
	Reads are added to read_dict until a pair is found.
	"""
	output = {}
	for read in bam.fetch(region=region_string):
		qname = read.query_name
		if not read.is_proper_pair:
			continue
		if read.is_supplementary:
			continue
		if qname not in output:
			output[qname] = [None,None]
			if read.is_read1:
				output[qname][0] = read
			else:
				output[qname][1] = read
		else:
			if read.is_read1:
				output[qname][0] = read
			else:
				output[qname][1] = read
	return output
	
def is_outie(x,y):	
	if x.is_reverse:
		if not y.is_reverse:
			if x.pos < y.pos:
				return True
	else:
		if y.is_reverse:
			if y.pos < x.pos:
				return True		
	return False

def is_innie(x,y):
	if x.is_reverse:
		if not y.is_reverse:
			if x.pos > y.pos:
				return True
	else:
		if y.is_reverse:
			if y.pos > x.pos:
				return True		
	return False



def main():

	args = my_args()
	bam = pysam.AlignmentFile(args.bam_file,"rb")
	df = read_pair_generator(bam)
	qnames = []
	read1 = []
	read2 = []
	for k in df:
		if args.outward:
			flag = is_outie(df[k][0],df[k][1])
		if args.inward:
			flag = is_innie(df[k][0],df[k][1])
		if flag:	
			qnames.append(k)
			read1.append(df[k][0].query)
			read2.append(df[k][1].query)
	print ("There are %s outward reads."%(len(qnames)))
	df = pd.DataFrame()
	df['Read_name'] = qnames
	df['R1_seq'] = read1
	df['R2_seq'] = read2
	df.to_csv(args.output,index=False)

	
if __name__ == "__main__":
	main()








