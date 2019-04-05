#!/hpcf/apps/python/install/2.7.13/bin/python
from __future__ import print_function,division
import sys
import logging
import argparse
import os
import subprocess 
import re
import getpass
import datetime
import uuid
'''
HemTools dir structure
-bin/
	HemTools
	exec
-subcmd/
	*.py
-hg19/
-hg38/
-genomes
	
'''

# ---------------- import subcmd libraries -------------------
# p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
# username = getpass.getuser()
sys.path.append(os.path.abspath("../subcmd/"))
from cut_run import *
from chip_seq_pair import *
from chip_seq_single import *
from atac_seq import *
from report_bug import *
# from hichip import *
# from rna_seq import *
# from read_align import *
# from bam_to_bw import *
# from STJtracks import *
# from volcano_plot import *
# from diffpeaks import *
# from crispr_seq import *
# from grna_heatmap import *
# from methylmotifs import *
# from chromhmm import *
# from csaw import *
# from bed_heatmap import *
# from demultiplex import *


# main_parser = argparse.ArgumentParser(description="HemTools: performs NGS pipelines and other common analyses. Contact: Yichao.Li@stjude.org or Yong.Cheng@stjude.org",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# main_parser.add_argument('-v', '--version',action='version',version='%(prog)s 1.0')
# # main_parser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='{{subcmd}}_'+username+"_"+str(datetime.date.today()))	
# # main_parser.add_argument('-x','--dry_run',  help=" 1 or 0. 1: dry run, check file names", default=0,type=int)
# # main_parser.add_argument('--short',  help="1 or 0. 1: Force to use the short queue. (only if R1+R2 fastq.gz size <=250M)", default=0,type=int)
# subparser=main_parser.add_subparsers(help='Available APIs in HemTools',dest='subcmd')


# cmd=subparser.add_parser('atac_seq',help='ATAC-seq pipeline',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# cmd.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='{{subcmd}}_'+username+"_"+str(datetime.date.today()))	
# cmd.add_argument('--short',  help="Force to use the short queue. (only if R1+R2 fastq.gz size <=250M)", action='store_true')	
# cmd.add_argument('--debug',  help="Not for end-user.", action='store_true')

# group = cmd.add_mutually_exclusive_group(required=True)
# group.add_argument('-f',"--input",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID")
# group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')		
	


# # group = cmd.add_mutually_exclusive_group(required=True)
# # input=group.add_argument_group(title='Input files')
# # input.add_argument('-f',"--input",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID")
# # group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')	


# # input=cmd.add_argument_group(title='Input files')
# # input.add_argument('-f',"--input",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID", required=True)
# # input.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')
# genome=cmd.add_argument_group(title='Genome Info')
# genome.add_argument('-i','--index_file',  help="BWA index file", default=p_dir+'../hg19/bwa_16a_index/hg19.fa')
# genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm10, mm9.", default='hg19',type=str)
# genome.add_argument('-b','--Blacklist',  help="Blacklist file", default=p_dir+'../hg19/Hg19_Blacklist.bed')
# genome.add_argument('-s','--chrom_size',  help="chrome size", default=p_dir+"../hg19/hg19.chrom.sizes")
# genome.add_argument('-e','--effectiveGenomeSize',  help="effectiveGenomeSize for bamCoverage", default="2451960000")
# adaptor=cmd.add_argument_group(title='Adaptor Info')
# adaptor.add_argument('-x', '--adaptor_x', help="Adapter sequence 5'end",type=str,default="CTGTCTCTTATACACATCT")
# adaptor.add_argument('-y', '--adaptor_y', help="Adapter sequence 3'end",type=str,default="CTGTCTCTTATACACATCT")




def HemTools_parser():
	

	main_parser = argparse.ArgumentParser(description="HemTools: performs NGS pipelines and other common analyses. Contact: Yichao.Li@stjude.org or Yong.Cheng@stjude.org",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	main_parser.add_argument('-v', '--version',action='version',version='%(prog)s 1.0')
	# main_parser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='{{subcmd}}_'+username+"_"+str(datetime.date.today()))	
	# main_parser.add_argument('-x','--dry_run',  help=" 1 or 0. 1: dry run, check file names", default=0,type=int)
	# main_parser.add_argument('--short',  help="1 or 0. 1: Force to use the short queue. (only if R1+R2 fastq.gz size <=250M)", default=0,type=int)
	subparser=main_parser.add_subparsers(help='Available APIs in HemTools',dest='subcmd')

	arg_cut_run(subparser)
	arg_chip_seq_pair(subparser)
	arg_chip_seq_single(subparser)
	arg_atac_seq(subparser)
	arg_report_bug(subparser)
	# arg_hichip(subparser)
	# arg_rna_seq(subparser)
	# arg_read_align(subparser)
	# arg_bam_to_bw(subparser)
	# arg_STJtracks(subparser)
	# arg_volcano_plot(subparser)
	# arg_diffpeaks(subparser)
	# arg_crispr_seq(subparser)
	# arg_grna_heatmap(subparser)
	# arg_methylmotifs(subparser)
	# arg_chromhmm(subparser)
	# arg_csaw(subparser)
	# arg_bed_heatmap(subparser)
	# arg_demultiplex(subparser)


	return main_parser

main_parser = HemTools_parser()




