#!/usr/bin/env python
import sys
import os
import argparse
import logging
import Colorer
import pandas as pd
import subprocess
import yaml
import datetime
import getpass
from utils import collision_boxplot

"""
main script to stitch  together share-seq analysis pipeline

"""
username = getpass.getuser()
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f1',"--sample_barcode",  help="input config file,tsv: label, sample_barcode, ATAC/RNA", required=True)	
	mainParser.add_argument('-f2',"--cell_barcode",  help="a list of barcode sequences", required=True)	
	mainParser.add_argument('-r1',  help="input undetermined R1 fastq.gz", required=True)	
	mainParser.add_argument('-r2',  help="input undetermined R2 fastq.gz", required=True)		
	# mainParser.add_argument('-r2',  help="input undetermined R2 fastq.gz", required=True)		
	mainParser.add_argument('-n',"--num_mismatch",  help="number of mismatch allowed", default=1,type=int)	
	mainParser.add_argument("--collision_threshold",  help="max mapping rate as collision", default=0.8,type=float)	
	mainParser.add_argument("--min_reads_per_cell",  help="minimal number of reads per cell", default=100,type=float)	
	mainParser.add_argument("--collision",  help="map to hybrid genome and calculate collision rate",action='store_true')
	mainParser.add_argument("--filter_polyT",  help="polyT reads may not be noise",action='store_true')

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version, must match key in genome config yaml file", default='hg38',type=str)
	genome.add_argument('--genome_config',  help="genome config file specifing: index file, black list, chrom size and effectiveGenomeSize", default='genome.yaml',type=str)


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args




def main():

	args = my_args()
	with open(args.genome_config, 'r') as f:
		genome = yaml.load(f,Loader=yaml.FullLoader)
	# genome = parse_yaml(args.genome_config)
	src="/home/yli11/Tools/SHARE_seq_pipeline"
	# print (genome)
	df = pd.read_csv(args.sample_barcode,sep="\t",header=None)

	# step 1: demultiplexing
	command = f"{src}/share_seq_step1_demultiplex.py -r1 {args.r1} -r2 {args.r2} -b {args.sample_barcode} -n {args.num_mismatch}"
	logging.info("Running sample demultiplexing...")
	logging.info(command)
	subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	# exit()
	# step 2: rename fastq, add cell barcode to read name, proper format for UMI-tools
	for label,_,data_type in df.values:
		
		command = f"{src}/share_seq_step2_rename_fastq.py -r1 {label}.R1.fastq.gz -r2 {label}.R2.fastq.gz  --sample_ID {label} --barcode_list {args.cell_barcode} --error {args.num_mismatch} --revcomp"
		logging.info(f"Reformatting fastq read name for {label} ...")
		logging.info(command)
		subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	
	# step 3: extract UMI and match polyT for RNA-seq
	for label,_,data_type in df.values:
		if str(data_type).upper() != "RNA":
			continue
		command = f"umi_tools extract --bc-pattern=NNNNNNNNNN --stdin {label}.matched.R2.fastq.gz --stdout {label}.matched.R2.extract --read2-in {label}.matched.R1.fastq.gz --read2-out {label}.matched.R1.extract"
		logging.info(f"UMI-tools extract UMI for {label} ...")
		logging.info(command)
		subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		if args.filter_polyT:
			command = f"cutadapt --overlap 6 -G ^TTTTTT --no-trim --untrimmed-output {label}.noPolyT.R1.fastq.gz --untrimmed-paired-output {label}.noPolyT.R2.fastq.gz -e 0.2 -o {label}.matched.R1.fastq.gz -p {label}.matched.R2.fastq.gz {label}.matched.R1.extract {label}.matched.R2.extract;rm {label}.matched.R1.extract {label}.matched.R2.extract"
			logging.info(f"cutadapt match polyT for {label} ...")
			logging.info(command)
			subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		else:
			command = f"mv {label}.matched.R2.extract {label}.matched.R2.fastq;gzip {label}.matched.R2.fastq;mv {label}.matched.R1.extract {label}.matched.R1.fastq;gzip {label}.matched.R1.fastq"
			logging.info(f"User choose not to filter reads based on polyT (this is default). Renaming fastq files...")
			logging.info(command)
			subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	# exit()	

	# step 4: if collision mode, map to hybrid genome
	if args.collision:
		for label,_,data_type in df.values:
			if str(data_type).upper() == "RNA":
				command = f"{src}/STAR_mapping.sh {genome['hybrid']['STAR']} {label}.matched.R1.fastq.gz {label}.matched.R2.fastq.gz {label} {genome['hybrid']['gtf']}"
				logging.info(f"STAR mapping for {label} ...")
				logging.info(command)
				subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			if str(data_type).upper() == "ATAC":
				command = f"{src}/BWA_mapping.sh {genome['hybrid']['BWA']} {label}.matched.R1.fastq.gz {label}.matched.R2.fastq.gz {label}"
				logging.info(f"BWA mapping for {label} ...")
				logging.info(command)
				subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			command = f"{src}/step4_calculate_collision_rate_hybrid.py --table {label}.total_number_reads.tsv --reads {label}.R1.bed --threshold {args.collision_threshold}"
			logging.info(f"step4_calculate_collision_rate_hybrid for {label} ...")
			logging.info(command)
			subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)			
			
			command = f"module load R/3.5.1;Rscript {src}/draw_collision_figure.R {label}.for_collision_plot.tsv {label}_collision.pdf {args.collision_threshold}"
			logging.info(f"draw_collision_figure for {label} ...")
			logging.info(command)
			subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)			
						
			
			collision_boxplot(f"{label}.for_collision_plot.tsv",label,cutoff=args.min_reads_per_cell,threshold=args.collision_threshold)
					
		exit()
		
	# step 5: using HemTools map the final fastq to the genome by BWA or STAR
	for label,_,data_type in df.values:
		if str(data_type).upper() == "RNA":
			command = f"{src}/STAR_mapping.sh {genome[args.genome]['STAR']} {label}.matched.R1.fastq.gz {label}.matched.R2.fastq.gz {label} {genome[args.genome]['gtf']} {genome[args.genome]['rseqc_bed']}"
			logging.info(f"STAR mapping for {label} ...")
			logging.info(command)
			subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			
			
		if str(data_type).upper() == "ATAC":
			command = f"{src}/BWA_mapping.sh {genome[args.genome]['BWA']} {label}.matched.R1.fastq.gz {label}.matched.R2.fastq.gz {label} {genome[args.genome]['rseqc_bed']} {args.genome}"
			logging.info(f"BWA mapping for {label} ...")
			logging.info(command)
			subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			

	
	
	# output Organization
	os.system(f"mkdir -p {args.jid}")
	for label,_,data_type in df.values:
		os.system(f"mkdir {args.jid}/{label};mv {label}* {args.jid}/{label}/")
		
if __name__ == "__main__":
	main()

























