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
	mainParser.add_argument('-l','--length',  help="read start length to check",type=int,default=30)
	# mainParser.add_argument('--sns_style',  help="searborn figure style, default is whitegrid, which is used by ggplot2. You can also use white", default="whitegrid")
	# mainParser.add_argument('--ylabel',  help="define Y-label", default="User values")
	# mainParser.add_argument('--log2',  help="log2 transform raw values", action='store_true')
	# mainParser.add_argument('--yscale_log',  help="log y-axis", action='store_true')
	# mainParser.add_argument('--kde',  help="plot kde density plot", action='store_true')
	mainParser.add_argument('-o',"--output",  help="output prefix",default="bam_deamination_start_pos_"+username+"_"+str(datetime.date.today())+".bed")
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	

	return args



def get_deamination(r,ref="A",alt="G",length=20):
	out = []
	actual_start = 0
	myList = r.get_aligned_pairs(with_seq=True)
	qualities = r.query_qualities
	if r.is_reverse:
		myList = myList[::-1]
	q_seq = r.query_sequence
	for q,ref_pos,base in myList:
		if q == None:
			continue
		if actual_start >length:
			return out
		actual_start+=1
		if qualities[q]<=10:
			continue
		if ref_pos == None:
			continue
		# try:
			# q_seq[q]
		# except:
			# print (q,q_seq,ref_pos,base)
			# print (r.is_reverse)
			# print (r.query_name)
			# print ("%s:%s-%s"%(r.reference_name,r.reference_start,r.reference_end))
			# refseq = r.get_reference_sequence()
			# q_seq = r.query_sequence
			# print (refseq[:20])
			# print (q_seq[:20])
		if q_seq[q] == alt and base.upper() == ref:
			# out.append([actual_start,base,q_seq[q],[q,ref_pos,base]])
			out.append(actual_start)
	return out
def get_deamination2(r,ref="A",alt="G",length=20):
	out = []
	# actual_start = 0
	refseq = r.get_reference_sequence()
	q_seq = r.query_alignment_sequence
	if r.is_reverse:
		refseq = refseq[::-1]
		q_seq = q_seq[::-1]
	for i in range(0,length):
		try:
			ref_base = refseq[i]
			q_base = q_seq[i]
		except:
			print (i,refseq,q_seq)
			return [-1]
		if str(ref_base) == ref and q_base == alt:
			out.append([i+1,ref_base,q_base,refseq[:20],q_seq[:20]])
	return out

def get_ref_alt(r):
	if r.is_reverse: # reverse check A -> G
		return "A","G"
		
	else: # check T-C
		return "T","C"

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
		# if read.is_secondary:
			# continue
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
				return True,x.reference_end - y.reference_start,x.reference_end,y.reference_start
	else:
		if y.is_reverse:
			if y.reference_start < x.reference_start:
				return True,y.reference_end - x.reference_start,x.reference_start,y.reference_end
	return False,0,0,0

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


def get_read_coord(r):
	if r.is_reverse:
		return "%s:%s-%s(-)"%(r.reference_name,r.reference_start,r.reference_end )
	return "%s:%s-%s(+)"%(r.reference_name,r.reference_start,r.reference_end )



def main():


	args = my_args()
	# output
	# chr, start, end, qname, deamination_pos, out/inward, overlap_bp
	bam = pysam.AlignmentFile(args.bam,"rb")
	print ("Processing %s"%(args.bam))
	df = read_pair_generator(bam)
	qnames = []
	window = 3
	R1_start = []
	R2_start = []
	chr = []
	overlap=[]
	de_pos = []
	# if a read is outward and len_overlap-window<=pos_AG <=len_overlap+window
	for k in df:
		if df[k][0] == None:
			continue
		if df[k][1] == None:
			continue
		flag,v,r1_start_pos,r2_start_pos = is_outie(df[k][0],df[k][1])
		if flag:
			# if overlap
			out1 = []
			out2 = []
			# R1 deamination
			r = df[k][0]
			if len(r.query_alignment_sequence) > 30:
				ref,alt = get_ref_alt(r)
				out1 = get_deamination(r,ref,alt,args.length)
			r = df[k][1]
			if len(r.query_alignment_sequence) > 30:
				ref,alt = get_ref_alt(r)
				out2 = get_deamination(r,ref,alt,args.length)
			if len(out1) > 0 and len(out2) > 0:
				# ambigous skip
				continue
			if len(out1) == 0 and len(out2) == 0:
				# no deamination skip
				continue
			for i in out1+out2:
				if v <=i<=v+window:
					overlap.append(v)
					qnames.append(k)
					chr.append(df[k][0].reference_name)
					R1_start.append(r1_start_pos)
					R2_start.append(r2_start_pos)
					de_pos.append(i)

	df = pd.DataFrame()
	df['#chr'] = chr
	df['#R1_start'] = R1_start
	df['#R2_start'] = R2_start
	df['#Read_name'] = qnames
	df['#deamination_pos'] = de_pos
	df['#overlap'] = overlap

	df.to_csv(args.output,index=False,sep="\t")
	# chr, start, end, qname, deamination_pos, out/inward, overlap_bp
	


if __name__ == "__main__":
	main()


























