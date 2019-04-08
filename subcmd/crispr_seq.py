#!/hpcf/apps/python/install/2.7.13/bin/python
from utils import *
import os
import argparse
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"

def arg_crispr_seq(parser):
	cmd=parser.add_parser('crispr_seq',help='Genome-wide CRISPR Screening pipeline',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	cmd.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='{{subcmd}}_'+username+"_"+str(datetime.date.today()))	
	cmd.add_argument('--short',  help="Force to use the short queue.", action='store_true')	
	cmd.add_argument('--debug',  help="Not for end-user.", action='store_true')	

	input=cmd.add_argument_group(title='Input files')

	# input.add_argument('--CRISPhieRmix',  help="run CRISPhieRmix in addition to Mageck MLE and RRA.", action='store_true')	
	input.add_argument('--control_gRNAs',  help="a list of control gRNAs. If provided, normalization will be performed based on these controls, instead of median normalization.")	
	
	input.add_argument('-d', "--design_matrix", help="tab delimited 3 columns (tsv file): treatment sample ID, control sample ID, peakcall ID", required=True)
	input.add_argument("--gRNA_library", help="mageck format", required=True)

	genome=cmd.add_argument_group(title='Genome Info')
	genome.add_argument('--bed',  help="Genomic coordinates for gRNAs (Format: chr, start, end, name). If provided, raw counts, logFC, logFDR will be uploaded to protein paint for visualization.")
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38", default='hg19',type=str)

def run_crispr_seq(args,rootLogger):
	# rootLogger.info("this is crispr_seq")
	# rootLogger.info(str(args.subcmd).lower())
	if str(args.subcmd).lower() != "crispr_seq":
		return 0		
	if not os.path.isfile(args.design_matrix):
		rootLogger.error("Input files do not exist!")
		os.system("HemTools crispr_seq -h")
		# rootLogger.close()
		os.system("rm "+args.jid+".log")
		sys.exit(1)
	if os.path.isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		rootLogger.info ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		rootLogger.info ("The new job id is: "+args.jid)
	else:
		rootLogger.info ("The job id is: "+args.jid)			
		
		
	crispr_seq = NGS_pipeline(args,rootLogger)
	
	crispr_seq.parse_treatment_control()
	crispr_seq.dry_run()

	crispr_seq.run_mageck_count()
	# crispr_seq.run_DESEQ2()
	# if args.CRISPhieRmix:
	# 		crispr_seq.run_CRISPhieRmix()
	crispr_seq.run_mageck_RRA()
	crispr_seq.run_mageck_MLE()

	# DESEQ (TODO), RRA
	# crispr_seq.combined_sgRNA_level_results()

	# MLE, RRA, and/or CRISPhieRmix (TODO)
	# crispr_seq.combined_gene_level_results()

	if args.bed:
		crispr_seq.run_STJtracks()

	crispr_seq.run_output_organization(report_flag=False)
	if args.debug:
		os.system("rm "+args.jid+"*")
		os.system("rm *bwDict")















