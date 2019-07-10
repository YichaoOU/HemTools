#!/hpcf/apps/python/install/2.7.13/bin/python
from utils import *
import os
import argparse
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"

def arg_rna_seq(parser):
	cmd=parser.add_parser('rna_seq',help='RNA-seq pipeline',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	cmd.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='{{subcmd}}_'+username+"_"+str(datetime.date.today()))	
	cmd.add_argument('--debug',  help="Not for end-user.", action='store_true')
	cmd.add_argument('--short',  help="Not for end-user.", action='store_true')
	# cmd.add_argument('--tracks',  help="Upload bw files to protein paitn", action='store_true')
	# cmd.add_argument('--kallisto',  help="kallisto: quantifying abundances of transcripts from bulk RNA-Seq data.", action='store_true')
	
	group = cmd.add_mutually_exclusive_group(required=True)
	group.add_argument('-f',"--input",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID")
	group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')		
	

	genome=cmd.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="STAR index file", default=p_dir+'../hg19/hg19_star_253a_index/')
	genome.add_argument('-b','--Blacklist',  help="Blacklist file", default=p_dir+'../hg19/hg19.blacklist.bed')
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=p_dir+"../hg19/hg19.chrom.sizes")
	genome.add_argument('-e','--effectiveGenomeSize',  help="effectiveGenomeSize for bamCoverage", default="2451960000")


def run_rna_seq(args,rootLogger):
	# rootLogger.info("this is rna_seq")
	# rootLogger.info(str(args.subcmd).lower())
	if str(args.subcmd).lower() != "rna_seq":
		return 0
	if args.guess_input:
		flag,fname = prepare_paired_end_input()
		os.system("rm "+args.jid+".log")		
		sys.exit(1)	
	if not (os.path.isfile(args.input)):
		rootLogger.error(args.input+" not exists!")
		os.system("HemTools rna_seq -h")
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

		
	rna_seq = NGS_pipeline(args,rootLogger)
	rna_seq.parse_paired_fastq()
	rna_seq.dry_run()
	
	
	rna_seq.run_fastqc()
	
	if args.kallisto:
		rna_seq.run_kallisto()
		rna_seq.run_combine_kallisto()
		
	# rna_seq.run_samtools_markdup_rmdup()

	# run_bamCoverage
	# rna_seq.run_bamCoverage('${COL3}.markdup.bam','${COL3}.all.bw','all')
	# rna_seq.run_bamCoverage('${COL3}.rmdup.bam','${COL3}.rmdup.bw','rmdup')
	# rna_seq.run_bamCoverage('${COL3}.rmdup.uq.bam','${COL3}.rmdup.uq.bw','rmdup.uq')

	# if args.tracks:
		# rna_seq.run_STJtracks()

	rna_seq.run_output_organization()

	if args.debug:
		os.system("rm "+args.jid+"*")
		os.system("rm *bwDict")

