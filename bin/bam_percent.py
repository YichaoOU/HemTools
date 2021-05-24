#!/usr/bin/env python

import pysam
import sys
import argparse
import datetime
import pandas as pd
import getpass
import uuid
import os
def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-b','--bam',  help="input bam", required=True)
	mainParser.add_argument('--blacklist',  help="input bam", default="/home/yli11/Data/Blacklist/lists/hg38-blacklist.v2.bed.gz")
	mainParser.add_argument('-o',"--output",  help="output prefix",default="output.tsv")
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	

	return args

# bedtools intersect -a $test -b hg38-blacklist.v2.bed.gz -bed | head

def get_reads_in_blacklist(bam,blck_list,output):
	command = "bedtools intersect -a %s -b %s -bed > %s"%(bam,blck_list,output)
	os.system(command)
	df = pd.read_csv(output,sep="\t",header=None)
	myDict = {}
	for i in df[3].tolist():
		name = i.replace("/1","").replace("/2","")
		myDict[name] = None
	return myDict

def Tn5_percent(R1,R2):

	command1="cutadapt -O 10 --info-file {0}.R1.info.tsv -b CTGTCTCTTATACACATCT -o {0}.tmp.fq {0}".format(R1)
	command1="cutadapt -O 10 --info-file {0}.R2.info.tsv -b CTGTCTCTTATACACATCT -o {0}.tmp.fq {0}".format(R2)
	os.system(R1)
	os.system(R2)
	df1 = pd.read_csv("%s.R1.info.tsv"%(R1),sep="\t",header=None,names=list(range(14)))
	df2 = pd.read_csv("%s.R2.info.tsv"%(R2),sep="\t",header=None,names=list(range(14)))
	df1 = df1[df1[1]!=-1]
	df2 = df2[df2[1]!=-1]
	# only care about Tn5 in the middle
	df1 = df1[df1[2]>1]
	df1 = df1[df1[3]<150]
	df2 = df2[df2[2]>1]
	df2 = df2[df2[3]<150]
	R1_list = df1[0].tolist()
	R2_list = df2[0].tolist()
	return list(set(R1_list+R2_list))

def Tn5_percent_bam_fq(bam):
	label = bam.split("/")[-1]
	command0 = "bedtools bamtofastq -i {0} -fq {1}.fq".format(bam,label)
	command1="cutadapt --trimmed-only  -O 17 -b CTGTCTCTTATACACATCT -b AGATGTGTATAAGAGACAG -o {0}.Tn5.fq {0}.fq;rm {0}.fq".format(label)
	os.system(command0)
	os.system(command1)
	myDict = {}
	try:
		df = pd.read_csv("%s.Tn5.fq"%(label),sep="\t",header=None)
	except Exception as e:
		print (e)
		return myDict
	df = df.loc[list(range(0,df.shape[0],4))]
	
	for x in df[0]:
		myDict[x[1:]] = None
	return myDict


def read_pair_generator(bam):
	"""
	Generate read pairs in a BAM file or within a region string.
	Reads are added to read_dict until a pair is found.
	
	is chrM
	is chemric
	
	"""
	output = {}
	is_chrM = {}
	is_chimeric = {}
	total_reads = {}
	total_mapped_reads = {}
	unmapped = {}
	for read in bam.fetch(region=None):
		qname = read.query_name
		rname = read.reference_name
		total_reads[qname]=None

		if not "chr" in rname:
			print (qname,rname)
		if "chrM" == rname:
			is_chrM[qname]=None
		if read.has_tag('SA'):
			is_chimeric[qname]=None
		if read.is_unmapped:
			unmapped[qname]=None
			continue
		if not read.is_paired:
			continue
		if qname in unmapped:
			continue
		total_mapped_reads[qname]=None
	
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
	return output,is_chrM,is_chimeric,len(total_reads),len(total_mapped_reads)
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
	return False,0

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

def is_FF(x,y):
	if not x.is_reverse:
		if not y.is_reverse:
			return True
	return False

def is_RR(x,y):
	if x.is_reverse:
		if y.is_reverse:
			return True
	return False

def is_subset(x,y):
	if x.reference_start>=y.reference_start and x.reference_end <= y.reference_end:
		return True
	if y.reference_start>=x.reference_start and y.reference_end <= x.reference_end:
		return True
	return False

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
	bam = pysam.AlignmentFile(args.bam,"rb")
	df,is_chrM,is_chimeric,N_total,N_PE_total= read_pair_generator(bam)
	is_blacklist = get_reads_in_blacklist(args.bam,args.blacklist,args.output)
	TN5_list = Tn5_percent_bam_fq(args.bam)
	print ("%s mapping rate: %s"%(args.output,float(N_PE_total)/N_total))
	out = []
	for k in df:
		if df[k][0] == None:
			continue
		if df[k][1] == None:
			continue
		flag1,v = is_outie(df[k][0],df[k][1])
		flag2 = is_innie(df[k][0],df[k][1])
		flag3 = is_FF(df[k][0],df[k][1])
		flag4 = is_RR(df[k][0],df[k][1])
		flag5 = is_subset(df[k][0],df[k][1])
		out.append([k,flag1,flag2,flag3,flag4,flag5,k in is_chrM, k in is_chimeric, k in is_blacklist,k in TN5_list])
	df = pd.DataFrame(out)
	df.columns = ['read','is_outward','is_inward','is_FF','is_RR','is_subset','is_chrM','is_chimeric','is_blacklist','has_Tn5']
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








