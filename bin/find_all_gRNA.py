#!/usr/bin/env python
import sys
import os
import pandas as pd
import datetime
import getpass
import uuid
import argparse

"""
module load bedtools
module load python/2.7.13
module load cas-offinder
bsub -q priority -P Genomics -R 'rusage[mem=30000]' find_all_gRNA.py -f region.bed -e 30 -n 2
"""

def my_args():

	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f','--bed_file',  help="input regions to look for gRNAs", required=True)
	mainParser.add_argument('-e','--extend',  help="extend search area to left and right", default=100,type=int)
	mainParser.add_argument('-l','--sgRNA_length',  help="sgRNA_length", default=20)
	mainParser.add_argument('-g','--genome_fa',  help="genome fasta", default="/home/yli11/Data/Human/hg19/fasta/hg19.fa")
	mainParser.add_argument('--chr_dir',  help="dir to individual chromosome files, seems to be faster than a single big one", default=None)
	mainParser.add_argument('--PAM',  help="PAM sequence", default="NGG")
	mainParser.add_argument('-n','--mis_match',  help="number of mismatches", default=0, type=int)
	mainParser.add_argument('-o','--output',  help="output bed file name", default="candidate_gRNA.bed")
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()
def extend_bed(args):
	df = pd.read_csv(args.bed_file,sep="\t",header=None)
	df[1] = df[1].astype(int)-args.extend
	df[2] = df[2].astype(int)+args.extend
	outfile = str(uuid.uuid4()).split("-")[-1]
	df[[0,1,2]].to_csv(outfile,sep="\t",header=False,index=False)
	return outfile
	
def get_fasta(genome_fa,extended_file):
	out = extended_file+".fa"
	command = "bedtools getfasta -fi %s -bed %s -fo %s"%(genome_fa,extended_file,out)
	os.system(command)
	print (command)
	return out
	
def run_casOFFinder(genome_fasta,PAM,your_seq_list,nMisMatch=0,chr_dir=None):
	cas_input = str(uuid.uuid4()).split("-")[-1]
	cas_output = str(uuid.uuid4()).split("-")[-1]
	pattern = "N"*len(your_seq_list[0])+PAM
	if chr_dir:
		genome_fasta = chr_dir
	# print (chr_dir)
	# print (genome_fasta)
	config = [genome_fasta,pattern]
	for i in your_seq_list:
		config.append(i+PAM+" %s"%(nMisMatch))
	write_file(cas_input,"\n".join(config))
	# command = "cas-offinder %s C %s;rm %s"%(cas_input,cas_output,cas_input)	
	command = "cas-offinder %s G %s;rm %s"%(cas_input,cas_output,cas_input)	
	# command = "cas-offinder %s G %s"%(cas_input,cas_output)	
	# command = "cas-offinder %s C %s"%(cas_input,cas_output)	
	os.system(command)
	print (command)
	# exit()
	return cas_output
def row_apply(x,n):
	if x[4] == "-":
		start = x[2]+n
	else:
		start = x[2]
	return start
	
def get_GC(x):
	GC_count = 0
	for i in x:
		if i.upper() in ['G','C']:
			GC_count+=1
	return GC_count/float(len(x))

def cas_to_bed(x,PAM,output,sgRNA_length):
	df = pd.read_csv(x,sep="\t",header=None)
	df['start'] = df.apply(lambda r:row_apply(r,len(PAM)),axis=1)
	df['end'] = df['start']+sgRNA_length
	df['target'] = [x.replace(PAM,"") for x in df[0].tolist()]
	df['seq'] = df[3].apply(lambda x:x.upper())
	# print (df.head())
	## get GC%
	df['gc'] = df['seq'].apply(get_GC)
	# all mapped sgRNAs
	df['#chr'] = df[1]
	df['strand'] = df[4]
	df['N_mismatch_to_target'] = df[5]
	df[['#chr','start','end','seq','gc','strand','N_mismatch_to_target','target']].to_csv(output+".genome.sgRNA.bed",sep="\t",header=True,index=False)

	
def find_offtarget(locus_bed_file, gRNA_bed_file):
	outfile = str(uuid.uuid4()).split("-")[-1]
	columns = ['#chr','start','end','seq','gc','strand','N_mismatch_to_target','target']
	command = "bedtools intersect -a %s.genome.sgRNA.bed -b %s -u > %s"%(gRNA_bed_file,locus_bed_file,outfile)
	os.system(command)
	df = pd.read_csv(outfile,sep="\t",header=None)
	df.columns = columns
	print (df.shape)
	tmp = df[df['N_mismatch_to_target']!=0] # remove mis-matched sgRNA
	df = df[df['N_mismatch_to_target']==0] # remove mis-matched sgRNA
	print (df.shape)
	if tmp.shape[0] > 0:
		print ("mismatch in query bed:")
		print (tmp)
	df2 = pd.read_csv(gRNA_bed_file+".genome.sgRNA.bed",sep="\t",header=None)
	df2.columns = columns
	df2['name'] = df2['#chr']+":"+df2['start'].astype(str)+"-"+df2['end'].astype(str)+"("+df2['strand']+")"
	df['name'] = df['#chr']+":"+df['start'].astype(str)+"-"+df['end'].astype(str)+"("+df['strand']+")" # should be unique
	df.index = df['target'] ## number of off-target in terms of the target sgRNA sequence
	df3 = pd.DataFrame(df2.groupby('target')['name'].agg(', '.join))
	df['off_targets'] = df3['name']
	def remove_self_match(r):
		myList = r['off_targets'].split(", ")
		myList.remove(r['name'])
		return ",".join(myList)
		# return len(myList)

	df['off_targets'] = df.apply(remove_self_match,axis=1)

	def get_numOfftarget(r):
		if r['off_targets'] == "":
			return 0
		myList = r['off_targets'].split(",")
		return len(myList)
	df['numOffTargets'] = df.apply(get_numOfftarget,axis=1)
	df = df.drop(['off_targets'],axis=1) # in case output file is too big
	
	df.to_csv(gRNA_bed_file+".off_targets.info.csv",index=False)
	df[['#chr','start','end','seq','gc','strand']].to_csv(gRNA_bed_file,index=False,header=False,sep="\t")
	os.system("rm %s"%(outfile))

def main():

	args = my_args()
	# find_offtarget("a746985b8f5d", args.output)
	# exit()
	extended_file = extend_bed(args)
	extended_fa = get_fasta(args.genome_fa,extended_file)
	# run 1 
	cas_output = run_casOFFinder(extended_fa,args.PAM,["N"*args.sgRNA_length])
	# get sequneces
	df = pd.read_csv(cas_output,sep="\t",header=None)
	df = df.dropna()
	candidate_gRNAs = [x[:-len(args.PAM)] for x in df[3].tolist()]
	print ("Total number of possible gRNA is: %s"%(len(candidate_gRNAs)))
	os.system("rm %s"%(cas_output))
	# run 2 to get genomic coordinates
	cas_output = run_casOFFinder(args.genome_fa,args.PAM,candidate_gRNAs,args.mis_match,args.chr_dir)
	cas_to_bed(cas_output,args.PAM,args.output,args.sgRNA_length)
	## check if bedtools getfasta can get exact sequence - YES
	find_offtarget(extended_file, args.output)
	os.system("rm %s"%(extended_fa))
	os.system("rm %s"%(extended_file))
	os.system("rm %s"%(cas_output))
	
	
if __name__ == "__main__":
	main()


















































