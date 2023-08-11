#!/home/yli11/.conda/envs/captureC/bin/python

import pandas as pd
import sys
import os
import argparse
import pysam
def cigar_tuple_to_df(read,gRNA1,gRNA2,flank = 2):
    out = [] # start, end, type, length
    deletion_length = 0
    insertion_length = 0
    start = read.reference_start
    for i in read.cigartuples:
        if i[0] == 0: # M
            tmp = [start,start+i[1],"M",i[1]]
            start += i[1]
        elif i[0] == 1: # I
            indel_length=i[1]
            indel_start = start
            indel_end = start 
            indel_type = "I"
            tmp = [indel_start,indel_end,indel_type,0]
        elif i[0] == 2:
            indel_length=i[1]
            indel_start = start
            start += i[1]
            indel_end = start 
            indel_type = "D"
            tmp = [indel_start,indel_end,indel_type,i[1]]
        elif i[0]==4:
            continue
        elif i[0]==5:
            continue
        else:
            print ("not considered",read.cigarstring,read.query_name)
        if tmp[0]-flank+1<=gRNA1<=tmp[1]+flank:
            tmp.append(True)
        elif tmp[0]-flank+1<=gRNA2<=tmp[1]+flank:
            tmp.append(True)
        else:
            tmp.append(False)
        out.append(tmp)
    df = pd.DataFrame(out)
    # start is 0-index, end is 1-index
    D = df[(df[2]=="D")&(df[4]==True)][3].sum()
    I = df[(df[2]=="I")&(df[4]==True)][3].sum()
    return df,D,I

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output_label", help="output_label, raw read stats, and summary stats, csv", required=True)

	mainParser.add_argument('-f',"--input",  help="bam file from minimap2",required=True)
	mainParser.add_argument("--left_primer_start",  help="left_primer_start",default=5244000,type=int)
	mainParser.add_argument("--left_primer_end",  help="left_primer_end",default=5246000,type=int)
	mainParser.add_argument("--right_primer_start",  help="right_primer_start",default=5259000,type=int)
	mainParser.add_argument("--right_primer_end",  help="right_primer_end",default=5259800,type=int)


	mainParser.add_argument("--gRNA1_cut_pos",  help="gRNA1_cut_pos",default=5249973,type=int)
	mainParser.add_argument("--gRNA2_cut_pos",  help="gRNA2_cut_pos",default=5254897,type=int)
	mainParser.add_argument("--gRNA_cut_flank",  help="gRNA_cut_flank",default=2,type=int)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()

	# r_start_range = [args.left_primer_start,args.left_primer_end]
	# r_end_range = [5259000,5259800]
	# flank = 6
	# g34_1_range = [5249973-flank,5249973+flank]
	# g34_2_range = [5254897-flank,5254897+flank]

	r_start_range = [args.left_primer_start,args.left_primer_end]
	r_end_range = [args.right_primer_start,args.right_primer_end]
	# """
	bam = pysam.AlignmentFile(args.input, "rb")

	out = []
	for r in bam.fetch():
		tmp = [r.query_name,r.reference_start+1,r.reference_end]
		_,D,I = cigar_tuple_to_df(r,args.gRNA1_cut_pos,args.gRNA2_cut_pos,flank = args.gRNA_cut_flank)
		out.append(tmp+[D,I])
			
	df = pd.DataFrame(out)	   	
	def is_valid(r):
		if r_start_range[0]<r[1]<r_start_range[1]:
			if r_end_range[0]<r[2]<r_end_range[1]:
				return True
		return False
	df['is_valid'] = df.apply(is_valid,axis=1)
	def is_edit(r):
		if sum([r[3],r[4]])>0:
			return True
		return False
	df['is_edit'] = df.apply(is_edit,axis=1)
	df.columns = ['read','start','end','Deletion','Insertion',"is_valid","is_edit"]
	df.to_csv(f"{args.output_label}.read_stats.csv",index=False)
	# exit()
	# """
	df = pd.read_csv(f"{args.output_label}.read_stats.csv")
	df.columns = ['read','start','end','Deletion','Insertion',"is_valid","is_edit"]
	df = df.sort_values(['is_valid','is_edit'],ascending=False)
	df = df.drop_duplicates("read")
	total_reads = df.shape[0]
	df2 = df[df.is_valid==True] # contain all valid reads
	N_valid = df2.shape[0]
	df3 = df2[df2.is_edit==True]
	N_edit = df3.shape[0]
	total_indel_frequency = N_edit/N_valid
	percent_valid_read = N_valid/total_reads
	# manually check insertion is all zero
	df4 = df2.groupby("Deletion").size().sort_values(ascending=False).reset_index()
	df4[1] = df4[0]/N_valid
	df4.to_csv(f"{args.output_label}.deletion_stats.csv",index=False)
	print (args.output_label,total_reads,N_valid,percent_valid_read,total_indel_frequency)
	# get_read_list
	# for i in df4.head(n=5).Deletion.tolist():
		# read_list = f"{args.output_label}D{i}.list"
		# try:
			# df[df.Deletion==i].sample(n=100)[['read']].to_csv(read_list,header=False,index=False)
		# except:
			# df[df.Deletion==i][['read']].to_csv(read_list,header=False,index=False)
		# command = f"module load samtools/1.15.1;samtools view -b -N {read_list} {args.input} > {args.output_label}D{i}.example.bam;samtools index {args.output_label}D{i}.example.bam"
		# os.system(command)

if __name__ == "__main__":
	main()


















