#!/hpcf/apps/python/install/2.7.13/bin/python
from utils import *
import os
import argparse
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"

def arg_atac_seq(parser):
	cmd=parser.add_parser('atac_seq',help='ATAC-seq pipeline',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	cmd.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='{{subcmd}}_'+username+"_"+str(datetime.date.today()))	
	cmd.add_argument('--short',  help="Force to use the short queue. (only if R1+R2 fastq.gz size <=250M)", action='store_true')	
	cmd.add_argument('--debug',  help="Not for end-user.", action='store_true')

	group = cmd.add_mutually_exclusive_group(required=True)
	group.add_argument('-f',"--input",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID")
	group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')		
		
	

	# group = cmd.add_mutually_exclusive_group(required=True)
	# input=group.add_argument_group(title='Input files')
	# input.add_argument('-f',"--input",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID")
	# group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')	

	
	# input=cmd.add_argument_group(title='Input files')
	# input.add_argument('-f',"--input",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID", required=True)
	# input.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')
	genome=cmd.add_argument_group(title='Genome Info')
	genome.add_argument('-i','--index_file',  help="BWA index file", default=p_dir+'../hg19/bwa_16a_index/hg19.fa')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm10, mm9.", default='hg19',type=str)
	genome.add_argument('-b','--Blacklist',  help="Blacklist file", default=p_dir+'../hg19/Hg19_Blacklist.bed')
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=p_dir+"../hg19/hg19.chrom.sizes")
	genome.add_argument('-e','--effectiveGenomeSize',  help="effectiveGenomeSize for bamCoverage", default="2451960000")

def run_atac_seq(args,rootLogger):
	# rootLogger.info("this is atac_seq")
	# rootLogger.info(str(args.subcmd).lower())
	if str(args.subcmd).lower() != "atac_seq":
		return 0
	if args.guess_input:
		flag,fname = prepare_paired_end_input()
		os.system("rm "+args.jid+".log")		
		sys.exit(1)	
	if not (os.path.isfile(args.input)):
		rootLogger.error(args.input+" not exists!")
		os.system("HemTools atac_seq -h")
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

		
	atac_seq = NGS_pipeline(args,rootLogger)
	
	
	atac_seq.parse_paired_fastq()
	atac_seq.dry_run()

	atac_seq.run_fastqc()
	atac_seq.run_skewer()
	atac_seq.run_BWA()
	
	atac_seq.run_samtools_markdup_rmdup()

	
	# run_bamCoverage
	atac_seq.run_bamCoverage('${COL3}.markdup.bam','${COL3}.all.bw','all')
	atac_seq.run_bamCoverage('${COL3}.rmdup.bam','${COL3}.rmdup.bw','rmdup')
	atac_seq.run_bamCoverage('${COL3}.rmdup.uq.bam','${COL3}.rmdup.uq.bw','rmdup.uq')

	# lib complexity 
	atac_seq.run_lib_complexity()

	atac_seq.run_macs2_narrowPeak()

	atac_seq.run_STJtracks()

	atac_seq.run_output_organization()

	if args.debug:
		os.system("rm "+args.jid+"*")
		os.system("rm *bwDict")

