#!/usr/bin/env python
import os
import sys
import argparse
# sys.path.append('/home/dshresth/.conda/envs/umitools/bin/')
import pandas as pd
from loguru import logger
from datetime import datetime
import getpass


#umi_tools extract --extract-method=regex --bc-pattern=".+(?P<umi_1>G.{6}$)" --bc-pattern2=".+(?P<umi_2>T.{6}$)" --stdin=../trimmed_CTCF_DMSO_R1.fastq.gz --read2-in=../trimmed_CTCF_DMSO_R2.fastq.gz --stdout=processed_CTCF_DMSO_R1.fastq.gz --read2-out=processed_CTCF_DMSO_R2.fastq.gz --log=processed_DMSO.log
#umi_tools dedup --input-bam processed_CTCF_DMSO.bam --output-bam processed_CTCF_DMSO.dedup.bam --method=cluster --log=DMSO_deduplication.log

path = '/home/yli11/HemTools/share/script/proseq/'

@logger.catch
def get_bwa_genome_index(x):
	if x == 'hg19':
		return '2864785220', '/home/yli11/Data/Human/hg19/index/bwa_16a_index/hg19.fa', '/research_jude/rgs01_jude/dept/HEM/common/sequencing/chenggrp/pipelines/hg19/hg19.chrom.sizes'
	elif x == 'hg38':
		return '2913022398', '/research_jude/rgs01_jude/dept/HEM/common/sequencing/chenggrp/pipelines/hg38/bwa_16a_index/hg38.fa', '/research_jude/rgs01_jude/dept/HEM/common/sequencing/chenggrp/pipelines/hg38/hg38.chrom.sizes'
	elif x == 'mm10':
		return '2652783500', '/research_jude/rgs01_jude/dept/HEM/common/sequencing/chenggrp/pipelines/mm10/bwa_16a_index/mm10.fa', '/research_jude/rgs01_jude/dept/HEM/common/sequencing/chenggrp/pipelines/mm10/mm10.chrom.sizes'


@logger.catch
def run_proseq(input_file, output_folder, jid, cpu, genome_index,genome_size,read1_adapter, read2_adapter, read1_pattern, read2_pattern, umi_pattern, min_length ):
	bwa_cmd = open(path + 'proseq.lsf','r').read()

	flength = str(pd.read_csv(input_file, sep='\t', header=None).shape[0])
	
	bwa_cmd = bwa_cmd.replace('jid',jid).replace('cpu',cpu).replace('input_file',input_file).replace('genome_index',genome_index).replace('nfiles', flength).replace('read1_adapter', read1_adapter).replace('read2_adapter', read2_adapter).replace('umi_pattern', umi_pattern).replace('read1_pattern', read1_pattern).replace('read2_pattern', read2_pattern).replace('min_length',min_length).replace('genome_size',genome_size)

	with open(f'{jid}_run_proseq.lsf','w') as bwa:
		bwa.write(bwa_cmd)

	os.system(f'bsub < {jid}_run_proseq.lsf')
		
	return f'{jid}_proseq[1-{flength}]'
	
@logger.catch
def split_bam_bw(input_file, cpu, genome_index, genome_size_file, genome_size, proseq_jid):
	file_length = str(pd.read_csv(input_file, sep='\t', header=None).shape[0])
	fw_split = open(path + 'fw_split.lsf','r').read()
	rev_split = open(path + 'rev_split.lsf').read()

	fw_split_cmd = fw_split.replace('cpu',cpu).replace('input_file',input_file).replace('genome_size',genome_size).replace('nfiles', file_length).replace('proseq_jid', proseq_jid)
	rev_split_cmd = rev_split.replace('cpu',cpu).replace('input_file',input_file).replace('genome_size_file',genome_size_file).replace('nfiles', file_length).replace('genome_size', genome_size).replace('proseq_jid', proseq_jid)


	with open(f'fw_proseq_split.lsf','w') as fw:
		fw.write(fw_split_cmd)

	with open(f'rev_proseq_split.lsf','w') as rev:
		rev.write(rev_split_cmd)

	os.system(f'bsub < fw_proseq_split.lsf')
	os.system(f'bsub < rev_proseq_split.lsf')

	return [f'fw_split[1-{file_length}]', f'rev_split[1-{file_length}]']


def arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_file', default=None, help='tab separated file with fastq file and name')
	#parser.add_argument('m', '--mode', default='auto-detect', choices=['auto-detect', 'paired', 'single'], helpize='paired end or single end sequencing')
	parser.add_argument('-j', '--job_name', default ='proseq_result', help = 'this will be used to create output directory')
	parser.add_argument('-g','--genome', default = 'hg19', choices = ['hg38','hg19','mm10','custom'], help = 'different genome versions available. Default = hg19. incase of custom genome provide index path in --genome_index')
	parser.add_argument('--genome_index', default = None, help = 'genome index for custom genome file')
	parser.add_argument('-s', '--genome_size_file', default = None, help ='genome size file for custom genome')
	parser.add_argument('-a1','--read1_adapter', default = 'TGGAATTCTCGGGTGCCAAGG', help = 'adapter sequence for read1')
	parser.add_argument('-a2','--read2_adapter', default = 'GATCGTCGGACTGTAGAACTCT', help = 'adapter sequence for read2')
	parser.add_argument('-l', '--min_length', default = '17', help = 'minimum length after trimming adapters. Default value is set to 17')
	parser.add_argument('--umi_pattern', default = 'regex', choices = ['regex','string'], help = 'default value is regex for umi extraction')
	parser.add_argument('-u1','--read1_umi', default = ".+(?P<umi_1>G.{6}$)" , help = 'umi regex pattern for read1, this is for the umi at 3 prime end')
	parser.add_argument('-u2','--read2_umi', default = ".+(?P<umi_2>T.{6}$)", help = 'umi regex pattern for read2, this is for the umi at 3 prime end')
	parser.add_argument('-n','--cpu', default = '10', help = 'number of processors, default = 10')
	
	return parser

def main():
	
	username = getpass.getuser()
	email = f'{username}@stjude.org'
	parser = arguments()
	args = parser.parse_args()
	
	output_folder = os.path.abspath(args.job_name + '_' + datetime.now().strftime('%m_%d_%Y'))
	subdirectories = ['fastqc','adapter_umi_processed','bam','bw','split_bam_bw','logs']
	
	if args.input_file == None:
		logger.error('input file not provided. Exiting....')
		parser.print_help()
		sys.exit(1)

	if not os.path.exists(output_folder):
		for subdir in subdirectories:
			os.makedirs(os.path.join(output_folder, subdir), exist_ok = True)
	else:
		output_folder = os.path.abspath(args.job_name + '_' + datetime.now().strftime('%m_%d_%Y_%H%M%S'))
		for subdir in subdirectories:
			os.makedirs(os.path.join(output_folder, subdir), exist_ok = True)
		
	logger.add(f"{output_folder}/{args.job_name}.log", rotation='10 MB',mode='w')
	logger.level("WARNING", color="<bold><red>")
	
	logger.info(f"retrieving {args.genome} genome index and genome size\n")
			
	if args.genome != 'custom':
		genome_size, genome_index, genome_size_file = get_bwa_genome_index(args.genome)
	else:
		genome_size_file = args.genome_size_file
		genome_size = str(sum(pd.read_csv(genome_size_file, sep='\t', header=None).iloc[:,1]))
		genome_index = os.path.abspath(args.genome_index)
		
	logger.info(f'Parameters Used:\n\nrun_proseq.py --input_file {args.input_file} --job_name {args.job_name} --genome {args.genome} --cpu {args.cpu} --genome_index {genome_index} --genome_size_file {genome_size_file} --genome_size {genome_size} --read1_adapter {args.read1_adapter} --read2_adapter {args.read2_adapter} --read1_umi {args.read1_umi} --read2_umi {args.read1_umi}\n\n')
	
	logger.info(f'\n\n Submitting jobs for: \n\nRunning cutadapt------> Umi extraction -------> BWA mapping ---------> splitting bam files\n\n')
	proseq_jid = run_proseq(args.input_file, output_folder, args.job_name, args.cpu, genome_index, genome_size, args.read1_adapter, args.read2_adapter, args.read1_umi, args.read2_umi, args.umi_pattern, args.min_length)
	
	#jobs.append(proseq_jid)

	split_proseq_jid = split_bam_bw(args.input_file, args.cpu, genome_index, genome_size_file, genome_size, proseq_jid)

	email_job = open(path+'mv_files.sh','r').read().replace('output_folder',output_folder)

	with open(f'{output_folder}/logs/mv_files.sh','w') as f:
		f.write(email_job)

	#logger.info(f'\n\nbsub -P proseq -J {args.job_name}_email -w "ended({split_proseq_jid[0]}) && ended({split_proseq_jid[1]})" -oo {output_folder}/logs/email.out -eo {output_folder}logs/email.err -R "rusage[mem=5000]" -N -u {email} /home/dshresth/scripts/proseq/mv_files.sh\n\n')

	os.system(f'bsub -P proseq -J {args.job_name}_email -w "ended({split_proseq_jid[0]}) && ended({split_proseq_jid[1]})" -oo {output_folder}/logs/email.out -eo {output_folder}/logs/email.err -R "rusage[mem=5000]" -N -u {email} {output_folder}/logs/mv_files.sh')

	
	

main()
	
				
