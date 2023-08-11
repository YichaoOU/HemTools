#!/usr/bin/env python

import pandas as pd
import sys
import os
import argparse
from datetime import datetime

from Levenshtein import distance as edit_distance
from Bio import SeqUtils


"""
-i Input, chr, start, end, gene, exon number, seq. Note this seq,start, end are all extended by 20bp




"""

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output", help="output file",required=True)

	mainParser.add_argument('-i',"--input",  help="exon bed file",required=True)
	mainParser.add_argument("--sample",  help="random sampling input file to set different seed gRNA",type=int,default=10)
	mainParser.add_argument("--init_gRNA_per_gene",  help="",type=int,default=5)
	mainParser.add_argument('-e',"--edit_distance_cutoff",  help="",type=int,default=7)
	mainParser.add_argument('-n','--min_N_gRNA',  help="Minimal number of gRNAs in the set",type=int,default=5000)
	mainParser.add_argument('-p',"--position_distance_cutoff",  help="we check gRNA start position diff, so the actual distance should be minus gRNA length",type=int,default=50)
	mainParser.add_argument('-r',"--repeat_mask_threshold",  help="",type=int,default=10)
	mainParser.add_argument("--firstG",  help="Require the first letter to be G for gRNA sequence",action='store_true')
	mainParser.add_argument("--no_firstG",  help="Require the first letter to be G for gRNA sequence",action='store_true')
	mainParser.add_argument('-c',"--cut_pos",  help="gRNA cut position",type=int,default=-3)
	mainParser.add_argument("--PAM",  help="gRNA cut position",type=str,default="NGG")
	mainParser.add_argument('-l',"--gRNA_length",  help="gRNA length",type=int,default=20)
	mainParser.add_argument("--flank_length",  help="fixed",type=int,default=20)
	mainParser.add_argument('-v',"--verbosity",  help="print more info for debug",type=int,default=0)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
def find_gRNA(chr,start,end,exon_number,gene_name,target_fa,gRNA_dict,number_gene_used,seq="NNNNNNNNNNNNNNNNNNNN",PAM="NGG",cut_pos=-3,position_distance_cutoff=30,init_gRNA_per_gene=5,edit_distance_cutoff=7,repeat_mask_threshold=10,flank_length=20,verbosity=10,**kwargs):
	"""Given exon sequence, gRNA pattern, search params, find all gRNAs

	Input
	-----

	exon info:, chr,start,end

	target_fa: <string>, exon sequence, ACGTacgt, lower case are repeat-masks. We assume the input sequence is the forward sequence.

	flank_length: we assume the input exon sequence is extended +/- flank_length, because there could be a gRNA partially overlaps with exon but cuts at the exon, this is a valid gRNA. So to calculate gRNA position, we will do start/end +/- flank_length.

	gRNA_dict: <dict>, gRNA_seq:[chr,start,end,gene_name,gRNA_seq,strand,exon_number]

	number_gene_used: to ensure number of gRNAs per gene requirements

	gRNA pattern: seq, PAM, cut_pos

	search params: 

	1. position_distance_cutoff: minimal distance between any two gRNAs, make sure gRNAs do not overlap, two gRNAs to be at least 30bp away

	2. init_gRNA_per_gene: number of gRNAs per gene

	3. edit_distance_cutoff: minimal edit distance between any two gRNAs

	4. repeat_mask_threshold: maximal repeat region overlaps

	Output
	------

	gRNA_dict: final output

	number_gene_used: intermediate output

	"""
	if number_gene_used[gene_name]>=init_gRNA_per_gene:
		# print (gene_name,"has more than",init_gRNA_per_gene,"gRNAs")
		return gRNA_dict,number_gene_used
	upper_case_seq = target_fa.upper()
	if verbosity>0:
		print (gene_name,"F",target_fa)
	# find gRNA in forward strand
	fwd_search = SeqUtils.nt_search(upper_case_seq, seq+PAM)
	if len(fwd_search) > 1:
		for s in fwd_search[1:]: # s is 0-index position
			#---Filter flank_length, cutting position has to be in the exon region
			if not cut_in_exon(len(target_fa),s,len(seq),cut_pos,flank_length):
				if verbosity>10:
					gRNA_seq = target_fa[s:(s+len(seq))]
					print (s,gRNA_seq," not in exon")
				continue
			#---Filter repeat_mask_cutoff
			gRNA_seq = target_fa[s:(s+len(seq))]
			gRNA_seq_repeat_mask = sum(1 for c in gRNA_seq if c.islower())
			# print ("forward",gRNA_seq,gRNA_seq_repeat_mask)
			if gRNA_seq_repeat_mask>=repeat_mask_threshold:
				if verbosity>10:
					print ("repeat mask failed",gRNA_seq_repeat_mask)
				continue
			gRNA_seq = gRNA_seq.upper()
			gRNA_start,gRNA_end = get_gRNA_position(start,end,s,len(seq))
			current_gRNA_info = [chr,gRNA_start,gRNA_end,gene_name,gRNA_seq,"+",exon_number]
			if verbosity>1:
				print (current_gRNA_info)
			select=True
			for g in gRNA_dict:
				#---Filter distance_cutoff
				if edit_distance(g,gRNA_seq) <=edit_distance_cutoff:
					if verbosity>10:
						print (g,gRNA_seq,"edit distance fail")
					select=False
					break
				#---Filter position_distance_cutoff
				if position_distance(gRNA_dict[g],current_gRNA_info)<=position_distance_cutoff:
					if verbosity>10:
						print (g,gRNA_seq,"pos distance fail")
					select=False
					break
			if select:
				gRNA_dict[gRNA_seq] = current_gRNA_info
				number_gene_used[gene_name]+=1
				if number_gene_used[gene_name]>=init_gRNA_per_gene:
					# print ("FWD",gene_name,"has more than",init_gRNA_per_gene,"gRNAs")
					return gRNA_dict,number_gene_used
	# find gRNA in reverse strand
	rev_seq = revcomp(upper_case_seq)			
	rev_seq_soft_mask = revcomp(target_fa)			
	rev_search = SeqUtils.nt_search(rev_seq, seq+PAM)
	if verbosity>0:
		print (gene_name,"R",rev_seq_soft_mask)
	if len(rev_search) > 1:
		for s in rev_search[1:]:
			pos  = len(target_fa)-s-len(seq)
			#---Filter flank_length, cutting position has to be in the exon region
			if not cut_in_exon(len(target_fa),s,len(seq),cut_pos,flank_length):
				if verbosity>10:
					gRNA_seq = rev_seq_soft_mask[s:(s+len(seq+PAM))]

					print (s,pos,gRNA_seq," rev not in exon")
				continue
			
			gRNA_seq = rev_seq_soft_mask[s:(s+len(seq))]
			#---Filter repeat_mask_cutoff
			gRNA_seq_repeat_mask = sum(1 for c in gRNA_seq if c.islower())
			# print ("rev",gRNA_seq,gRNA_seq_repeat_mask)
			if gRNA_seq_repeat_mask>=repeat_mask_threshold:
				if verbosity>10:
					print ("repeat mask failed",gRNA_seq_repeat_mask)
				continue
			gRNA_seq = gRNA_seq.upper()
			gRNA_start,gRNA_end = get_gRNA_position(start,end,pos,len(seq))
			current_gRNA_info = [chr,gRNA_start,gRNA_end,gene_name,gRNA_seq,"-",exon_number]
			if verbosity>1:
				print (current_gRNA_info)
			select=True
			for g in gRNA_dict:
				#---Filter distance_cutoff
				if edit_distance(g,gRNA_seq) <=edit_distance_cutoff:
					if verbosity>10:
						print (g,gRNA_seq,"edit distance fail")
					select=False
					break
				#---Filter position_distance_cutoff
				if position_distance(gRNA_dict[g],current_gRNA_info)<=position_distance_cutoff:
					if verbosity>10:
						print (g,gRNA_seq,"pos distance fail")
					select=False
					break
			if select:
				gRNA_dict[gRNA_seq] = current_gRNA_info
				number_gene_used[gene_name]+=1
				if number_gene_used[gene_name]>=init_gRNA_per_gene:
					# print ("REV",gene_name,"has more than",init_gRNA_per_gene,"gRNAs")
					return gRNA_dict,number_gene_used

	return gRNA_dict,number_gene_used

def cut_in_exon(target_seq_length,s,gRNA_length,cut_pos,flank_length):
	left_boundary = flank_length-gRNA_length-cut_pos
	right_boundary = target_seq_length-flank_length-gRNA_length-cut_pos
	return left_boundary<=s<=right_boundary


def get_gRNA_position(start,end,s,gRNA_length):
	"""return bed format position, the ccds database follows this format

	start 0-index

	end 1-index

	make sure "s" is adjusted by strand

	"""
	return start+s,start+s+gRNA_length


def position_distance(A,B):
	"""get two gRNA distance, assuming same length

	"""
	if A[0] == B[0]:
		return abs(A[1]-B[1])
	else:
		return 99999
def revcomp(seq):
	try: ## python2
		tab = string.maketrans(b"ACTGactg", b"TGACtgac")
	except:  ## python3
		tab = bytes.maketrans(b"ACTGactg", b"TGACtgac")
	return seq.translate(tab)[::-1]

def main():

	args = my_args()
	parameters = vars(args)
	# print (parameters)
	df = pd.read_csv(args.input,sep="\t",header=None)
	# df = df.sample(n=args.sample)
	df.columns = ['chr','start','end','gene','exon_number',"sequence"]
	number_gene_used=dict.fromkeys(df.gene.unique(),0)
	count = 0
	gRNA_dict={}
	while len(gRNA_dict) <args.min_N_gRNA:
		for i,r in df.iterrows():
			count+=1
			if len(gRNA_dict)>=args.min_N_gRNA:
				break
			if count %1000 == 0:
				now = datetime.now()
				current_time = now.strftime("%H:%M:%S")
				print("Current Time =", current_time,len(gRNA_dict),file=sys.stderr)
			# gRNA_dict,number_gene_used = find_gRNA(r[4],gRNA_dict,number_gene_used,r[3],seq="NNNNNNNNNNNNNNNNNNNN",PAM="NGG",position_distance=30,init_gRNA_per_gene=args.init_gRNA_per_gene,distance_cutoff=args.distance_cutoff)
			if args.firstG:
				gRNA_dict,number_gene_used = find_gRNA(r.chr,r.start,r.end,r.exon_number,r.gene,r.sequence,
													gRNA_dict,number_gene_used,
													seq="G"+"N"*(args.gRNA_length-1),**parameters)
			elif args.no_firstG:
				gRNA_dict,number_gene_used = find_gRNA(r.chr,r.start,r.end,r.exon_number,r.gene,r.sequence,
													gRNA_dict,number_gene_used,
													seq="H"+"N"*(args.gRNA_length-1),**parameters)
			else:
				gRNA_dict,number_gene_used = find_gRNA(r.chr,r.start,r.end,r.exon_number,r.gene,r.sequence,
													gRNA_dict,number_gene_used,
													seq="N"*args.gRNA_length,**parameters)
		parameters['edit_distance_cutoff'] -=1
		print ("updating edit_distance_cutoff to",parameters['edit_distance_cutoff'])
	# g = pd.DataFrame.from_dict(gRNA_dict,orient="index").reset_index()
	g = pd.DataFrame.from_dict(gRNA_dict,orient="index")
	g.columns = ['chr','start','end','gene','gRNA','strand','exon_number']
	g.to_csv(args.output,header=True,index=False)
	print (g)
	command = "cas_offinder.py -g hg19 --add_PAM --PAM_seq NGG -f %s -n 0 -j %s_casOffinder"%(args.output,args.output)
	# os.system(command)

if __name__ == "__main__":
	main()


















