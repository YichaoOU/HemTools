#!/usr/bin/env python

import pysam
import sys
import argparse
import datetime
import pandas as pd
import getpass
import uuid
def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	# group = mainParser.add_mutually_exclusive_group(required=True)
	# group.add_argument('-bam',  help="input bam file")
	# group.add_argument('-bed',  help="input bed file")
	# group = mainParser.add_mutually_exclusive_group(required=True)
	# group.add_argument('--outward',  help="get outward reads", action='store_true')
	# group.add_argument('--inward',  help="get inward reads", action='store_true')

	# mainParser.add_argument('-t','--target',  help="if user input target, only reads in this target is considered", default=None)
	mainParser.add_argument('-b','--bam',  help="input bam", required=True)
	# mainParser.add_argument('--sns_style',  help="searborn figure style, default is whitegrid, which is used by ggplot2. You can also use white", default="whitegrid")
	# mainParser.add_argument('--ylabel',  help="define Y-label", default="User values")
	# mainParser.add_argument('--log2',  help="log2 transform raw values", action='store_true')
	# mainParser.add_argument('--yscale_log',  help="log y-axis", action='store_true')
	# mainParser.add_argument('--kde',  help="plot kde density plot", action='store_true')
	mainParser.add_argument('-o',"--output",  help="output prefix",default="outward_"+username+"_"+str(datetime.date.today())+".bed")
	
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

		# if not read.is_proper_pair:
		if not read.is_paired:
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
# reference_start is 0-index
def is_outie(x,y):	
	if x.is_reverse:
		if not y.is_reverse:
			if x.reference_start < y.reference_start:
				return True,x.reference_end - y.reference_start
	else:
		if y.is_reverse:
			if y.reference_start < x.reference_start:
				return True,y.reference_end - x.reference_start
	return False,-1




def get_read_coord(r):
	if r.is_reverse:
		return "%s:%s-%s(-)"%(r.reference_name,r.reference_start,r.reference_end )
	return "%s:%s-%s(+)"%(r.reference_name,r.reference_start,r.reference_end )

def get_mapping_location(x,y):
	chr = x.reference_name
	start = min(x.reference_start,y.reference_start)
	end = max(x.reference_end,y.reference_end)
	return chr,start,end


def main():


	args = my_args()
	# print (args)
	
	# if args.bam:
		# args.bed = get_bed(args.bam)
	# if args.target:
		# args.bam = subset_bam(args.bam)
	bam = pysam.AlignmentFile(args.bam,"rb")
	df = read_pair_generator(bam)
	qnames = []
	mapq = []
	overlap = []

	for k in df:
		# if args.outward:
		
		# if k == 'MN01246:46:000H3F5W7:1:11102:19439:5139':
			# print (df[k])
		if df[k][0] == None:
			continue
		if df[k][1] == None:
			continue
		qnames.append(k)
		mapq.append(min(df[k][0].mapq,df[k][1].mapq))
		if df[k][0].reference_name != df[k][1].reference_name:
			overlap.append(-1)
		else:
			flag,v = is_outie(df[k][0],df[k][1])
			overlap.append(v)
		
		


	df = pd.DataFrame()

	df['name'] = qnames
	df['mapq'] = mapq
	df['overlap'] = overlap
	df.to_csv(args.output,index=False,sep="\t")

	


if __name__ == "__main__":
	main()


















"""



"""

# input


# bam to bed


# parse bed




# output tsv

# read name, R1_coord, R2_coord, overlap_bp
# negative value means gap bp, ie, not overlap








