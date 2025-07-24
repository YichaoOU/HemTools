#!/usr/bin/env python
import sys
import os
import pandas as pd
import datetime
import getpass
import uuid
import argparse
from collections import Counter
import numpy as np

"""
module load bedtools
module load python/2.7.13
module load cas-offinder/2.4.1-rhel8  

OR

module load conda3/202011
source activate Cas_Offinder
module load bedtools

bsub -q priority -P Genomics -R 'rusage[mem=30000]' find_all_gRNA.py -f region.bed -e 30 -n 2

Code for intersect with exon bed
---------------
bedtools intersect -a candidate_gRNA.bed -b candidate.exon.bed -wa -wb > candidate_gRNA.exon.bed
df2 = pd.read_csv("candidate_gRNA.exon.bed",sep="\t",header=None)
df2 = df.merge(df2,left_on = df.columns[:6].tolist(),right_on = df2.columns[:6].tolist(),how="inner").drop(df2.columns[:6].tolist(),axis=1)
df2.columns = df.columns.tolist()+out.columns.tolist()
df2 = df2.drop(["start1","end1","start2","end2","seq1","seq2","check"],axis=1)
df2.head()
df2.to_csv("candidate_gRNA.bed.off_targets.info.CRISPRscore.csv",index=False)

output files
-----------
main: candidate_gRNA.bed.off_targets.info.csv and candidate_gRNA.bed

detailed off-targets: candidate_gRNA.bed.genome.sgRNA.bed

temporary  file: candidate_gRNA.bed.num_targets.tsv


"""

# Define a function to parse command-line arguments
def my_args():

	# Create an argument parser object
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	
	# Add mutually exclusive group for input options
	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-f','--bed_file',  help="input regions to look for gRNAs")
	group.add_argument('-fa','--fasta',  help="input fasta to look for gRNAs")
	
	# Add optional arguments
	mainParser.add_argument('-e','--extend',  help="extend search area to left and right", default=100,type=int)
	mainParser.add_argument('-l','--sgRNA_length',  help="sgRNA_length", default=20,type=int)
	mainParser.add_argument('-g','--genome_fa',  help="genome fasta", default="/home/yli11/Data/Human/hg19/fasta/hg19.fa")
	mainParser.add_argument('--GPU',  help="input C or G", default="C")
	mainParser.add_argument('--PAM',  help="PAM sequence", default="NGG")
	mainParser.add_argument("--include_PAM_mismatch",  help="include_PAM_mismatch, when doing genome-wide off-target search",action='store_true')
	
	mainParser.add_argument('-n','--mis_match',  help="number of mismatches, when doing genome-wide off-target search", default=0, type=int)
	mainParser.add_argument('-o','--output',  help="output bed file name", default="candidate_gRNA.bed")
	
	# Parse the arguments
	args = mainParser.parse_args()	
	return args
def shannon_index(sequence):
    # Count the frequency of each character in the sequence
    freq = Counter(sequence)
    # Total number of characters in the sequence
    total = len(sequence)
    # Calculate the Shannon index
    shannon = -sum((count / total) * np.log2(count / total) for count in freq.values())
    return shannon

def longest_homopolymer(spacer_sequence):
    max_length = 0
    current_length = 1
    
    for i in range(1, len(spacer_sequence)):
        if spacer_sequence[i] == spacer_sequence[i - 1]:
            current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_length = 1

    # Check if the last homopolymer is the longest
    max_length = max(max_length, current_length)

    return max_length

# Define a function to write to a file
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

# Define a function to extend bed coordinates
def extend_bed(args):
	# Read bed file into a DataFrame
	df = pd.read_csv(args.bed_file,sep="\t",header=None,comment="#")
	# Extend bed coordinates
	df[1] = df[1].astype(int)-args.extend
	df[2] = df[2].astype(int)+args.extend
	# Generate a unique output filename
	outfile = str(uuid.uuid4()).split("-")[-1]
	# Write extended bed coordinates to file
	df[[0,1,2]].to_csv(outfile,sep="\t",header=False,index=False)
	return outfile

# Define a function to extract fasta sequences
def get_fasta(genome_fa,extended_file):
	out = extended_file+".fa"
	# Generate command to extract fasta sequences
	command = "bedtools getfasta -fi %s -bed %s -fo %s"%(genome_fa,extended_file,out)
	# Execute command
	os.system(command)
	print (command)
	return out

# Define a function to run Cas-OFFinder
def run_casOFFinder(genome_fasta,PAM,your_seq_list,nMisMatch=0,GPU="G",include_PAM_mismatch=False):
	# Generate unique filenames
	cas_input = str(uuid.uuid4()).split("-")[-1]+".cas_input"
	cas_output = str(uuid.uuid4()).split("-")[-1]+".cas_output"
	# Generate search pattern
	pattern = "N"*len(your_seq_list[0])+PAM
	if include_PAM_mismatch:
		pattern = "N"*(len(your_seq_list[0])+len(PAM))
	# Configuration for Cas-OFFinder
	config = [genome_fasta,pattern]
	for i in your_seq_list:
		config.append(i+PAM+" %s"%(nMisMatch))
	# Write configuration to file
	write_file(cas_input,"\n".join(config))
	# Generate and execute Cas-OFFinder command
	command = "cas-offinder %s %s %s;head %s;rm %s"%(cas_input,GPU,cas_output,cas_input,cas_input)	
	os.system(command)
	print (command)
	return cas_output

# Define a function to adjust start position based on strand
def row_apply(x,n):
	if x[4] == "-":
		start = x[2]+n
	else:
		start = x[2]
	return start

# Define a function to calculate GC content
def get_GC(x):
	GC_count = 0
	for i in x:
		if i.upper() in ['G','C']:
			GC_count+=1
	return GC_count/float(len(x))

# Define a function to process Cas-OFFinder output to bed format
def cas_to_bed(x,PAM,output,sgRNA_length):
	print (x)
	# Read Cas-OFFinder output into a DataFrame
	df = pd.read_csv(x,sep="\t",header=None)
	# Adjust start position based on strand
	df['start'] = df.apply(lambda r:row_apply(r,len(PAM)),axis=1)
	df['end'] = df['start']+sgRNA_length
	df['target'] = [x.replace(PAM,"") for x in df[0].tolist()]
	df['seq'] = df[3].apply(lambda x:x.upper())
	# Calculate GC content
	df['gc'] = df['seq'].apply(get_GC)
	# Rename columns
	df['#chr'] = df[1]
	df['strand'] = df[4]
	df['N_mismatch_to_target'] = df[5]
	# Write output to bed file
	df[['#chr','start','end','seq','gc','strand','N_mismatch_to_target','target']].to_csv(output+".genome.sgRNA.bed",sep="\t",header=True,index=False)
	# Write target counts to file
	df['target'].value_counts().to_csv(output+".num_targets.tsv",sep="\t",header=True,index=True)

# Define a function to convert list of sequences to fasta format
def list_to_fasta(l):
	out = []
	for i in l:
		if len(i) != 23:
			print ("something is wrong")
		out.append(">%s"%(i[:20]))
		out.append("AAAA%sAAA"%(i))
	return "\n".join(out)

# Define a function to find off-target sites
def find_offtarget(locus_bed_file, gRNA_bed_file,genome_fasta):
	# Generate output filename
	outfile = str(uuid.uuid4()).split("-")[-1]
	columns = ['#chr','start','end','seq','gc','strand','N_mismatch_to_target','target']
	# Run bedtools intersect to find overlapping regions
	command = "bedtools intersect -a %s.genome.sgRNA.bed -b %s -u > %s"%(gRNA_bed_file,locus_bed_file,outfile)
	os.system(command)
	# Read intersected regions into DataFrame
	df = pd.read_csv(outfile,sep="\t",header=None)
	df.columns = columns
	print (df.shape)
	# Remove mis-matched sgRNA
	tmp = df[df['N_mismatch_to_target']!=0]
	df = df[df['N_mismatch_to_target']==0]
	print (df.shape)
	if tmp.shape[0] > 0:
		print ("mismatch in query bed:")
		print (tmp)
	# Read gRNA bed file into DataFrame
	df2 = pd.read_csv(gRNA_bed_file+".genome.sgRNA.bed",sep="\t",header=None)
	df2.columns = columns
	df2['name'] = df2['#chr']+":"+df2['start'].astype(str)+"-"+df2['end'].astype(str)+"("+df2['strand']+")"
	df['name'] = df['#chr']+":"+df['start'].astype(str)+"-"+df['end'].astype(str)+"("+df['strand']+")"
	df.index = df['target']
	# Group off-targets by target
	df3 = pd.DataFrame(df2.groupby('target')['name'].agg(', '.join))
	df['off_targets'] = df3['name']
	# Remove self-matches
	def remove_self_match(r):
		myList = r['off_targets'].split(", ")
		myList.remove(r['name'])
		return ",".join(myList)
	df['off_targets'] = df.apply(remove_self_match,axis=1)
	# Count number of off-targets
	def get_numOfftarget(r):
		if r['off_targets'] == "":
			return 0
		myList = r['off_targets'].split(",")
		return len(myList)
	df['numOffTargets'] = df.apply(get_numOfftarget,axis=1)
	df = df.drop(['off_targets'],axis=1) # in case output file is too big
	df.to_csv(gRNA_bed_file+".off_targets.info.csv",index=False)

	
	# Write results to file
	# df.to_csv(gRNA_bed_file+".off_targets.info.csv",index=False)
	
	df[['#chr','start','end','seq','gc','strand']].to_csv(gRNA_bed_file,index=False,header=False,sep="\t")
	
	
	# calculate N repeat mask
	command = "bedtools getfasta -fi %s -bed %s -s -fo %s.tsv -tab"%(genome_fasta,gRNA_bed_file,gRNA_bed_file)
	os.system(command)
	seq = pd.read_csv("%s.tsv"%(gRNA_bed_file),sep="\t",header=None,index_col=0)
	seq['N_repeatMask'] = [sum(1 for c in gRNA_seq if c.islower()) for gRNA_seq in seq[1]]
	# homopolyer
	df['homopolymer'] = df.seq.apply(lambda x:longest_homopolymer(x[:-3]))
	df['shannon_index'] = df.seq.apply(lambda x:shannon_index(x[:-3]))
	df['N_repeatMask'] = df['name'].map(seq.N_repeatMask.to_dict())
	def get_new_coordinates(chr, start, end, strand,u=0,d=3):
		if strand == '+':
			new_start = start-u
			new_end = end+d
		elif strand == '-':
			new_end = end+u
			new_start = start-d
		else:
			raise ValueError("Strand must be '+' or '-'.")

		return chr, new_start, new_end
	def get_crisprScore_inputs(r):
		# DeepSpCas9
		chr,start,end = get_new_coordinates(r['#chr'], r.start, r.end, r.strand,u=4,d=6)
		r['start1'] = start
		r['end1'] = end
		# CRISPRscan
		chr,start,end = get_new_coordinates(r['#chr'], r.start, r.end, r.strand,u=6,d=9)
		r['start2'] = start
		r['end2'] = end
		return r
	df = df.apply(get_crisprScore_inputs,axis=1)
	out="tmp.bed"
	df[['#chr','start1','end1','name','name','strand']].to_csv(out,sep="\t",header=False,index=False)
	command = "bedtools getfasta -fi %s -bed %s -s -fo %s.tsv -tab -name"%(genome_fasta,out,out)
	os.system(command)
	seq = pd.read_csv("%s.tsv"%(out),sep="\t",header=None,index_col=0)
	seq.index = [x.split("::")[0] for x in seq.index]
	df['seq1'] = df['name'].map(seq[1].to_dict()).str.upper()


	df[['#chr','start2','end2','name','name','strand']].to_csv(out,sep="\t",header=False,index=False)
	command = "bedtools getfasta -fi %s -bed %s -s -fo %s.tsv -tab -name"%(genome_fasta,out,out)
	os.system(command)
	seq = pd.read_csv("%s.tsv"%(out),sep="\t",header=None,index_col=0)
	seq.index = [x.split("::")[0] for x in seq.index]
	df['seq2'] = df['name'].map(seq[1].to_dict()).str.upper()
	
	
	
	# Write results to file
	df.to_csv(gRNA_bed_file+".off_targets.info.csv",index=False)
	os.system("rm %s"%(outfile))
	# add crisprscore
	command = f"CRISPRscore.R {gRNA_bed_file}.off_targets.info.csv"
	os.system(command)
	try:
		AzimuthScores = pd.read_csv("AzimuthScores.csv")
		df['AzimuthScores'] = AzimuthScores[AzimuthScores.columns[-1]].tolist()
		CRISPRaterScores = pd.read_csv("CRISPRaterScores.csv")
		df['CRISPRaterScores'] = CRISPRaterScores[CRISPRaterScores.columns[-1]].tolist()
		DeepHFScores_df = pd.read_csv("DeepHFScores_df.csv")
		df['DeepHFScores'] = DeepHFScores_df[DeepHFScores_df.columns[-1]].tolist()
		RuleSet1Scores_df = pd.read_csv("RuleSet1Scores_df.csv")
		df['RuleSet1Scores'] = RuleSet1Scores_df[RuleSet1Scores_df.columns[-1]].tolist()
		RuleSet3Scores_df = pd.read_csv("RuleSet3Scores_df.csv")
		df['RuleSet3Scores'] = RuleSet3Scores_df[RuleSet3Scores_df.columns[-1]].tolist()
		DeepSpCas9Scores_df = pd.read_csv("DeepSpCas9Scores_df.csv")
		df['DeepSpCas9Scores'] = DeepSpCas9Scores_df[DeepSpCas9Scores_df.columns[-1]].tolist()
		CRISPRscanScores_df = pd.read_csv("CRISPRscanScores_df.csv")
		df['CRISPRscanScores'] = CRISPRscanScores_df[CRISPRscanScores_df.columns[-1]].tolist()
		df = df.drop(["start1","end1","start2","end2","seq1","seq2"],axis=1)
		df.to_csv(gRNA_bed_file+".off_targets.info.csv",index=False)
	except:
		print ("CRISPRscore failed to run")
	

def main():

	# Parse command-line arguments
	args = my_args()

	# Pre-processing, use bed file or a list of sequences
	if not args.fasta:
		extended_file = extend_bed(args)
		print ("User input bed file, extracting a list of sequences")
		args.fasta = get_fasta(args.genome_fa,extended_file)
		print ("saved to %s"%(args.fasta))
	
	# Run 1, to find all gRNAs 
	print ("finding all gRNAs in your given file")
	# run_casOFFinder(genome_fasta,PAM,your_seq_list,nMisMatch=0,GPU="G",include_PAM_mismatch=False)
	cas_output = run_casOFFinder(args.fasta,args.PAM,["N"*args.sgRNA_length],0,args.GPU,False)
	
	
	# Run 1, parse cas-offinder output
	df = pd.read_csv(cas_output,sep="\t",header=None)
	print ("casoffinder finished, but sometimes, casoffinder output can be truncated, need to manually check",cas_output)
	df = df.dropna()
	df['sgRNA_length'] = [len(x) for x in df[3]]
	df = df[df.sgRNA_length==len(args.PAM)+args.sgRNA_length]
	df["gRNA_seq"] = [x[:-len(args.PAM)] for x in df[3].tolist()]
	df = df.drop_duplicates("gRNA_seq")
	candidate_gRNAs = df.gRNA_seq.tolist()
	print ("Total number of possible gRNA is: %s"%(len(candidate_gRNAs)))
	
	# Run 2 to get genomic coordinates
	if args.bed_file:
		cas_output = run_casOFFinder(args.genome_fa,args.PAM,candidate_gRNAs,args.mis_match,args.GPU,args.include_PAM_mismatch)
		cas_to_bed(cas_output,args.PAM,args.output,args.sgRNA_length)
		## Check if bedtools getfasta can get exact sequence - YES
		find_offtarget(extended_file, args.output,args.genome_fa)
		os.system("rm %s"%(args.fasta))
		os.system("rm %s"%(extended_file))
	else:
		cas_output = run_casOFFinder(args.genome_fa,args.PAM,candidate_gRNAs,args.mis_match,args.GPU,args.include_PAM_mismatch)
		cas_to_bed(cas_output,args.PAM,args.output,args.sgRNA_length)
	# os.system("rm %s"%(cas_output))
	
# Call the main function if the script is run directly
if __name__ == "__main__":
	main()