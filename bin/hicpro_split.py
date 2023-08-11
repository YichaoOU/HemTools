#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
import multiprocessing 
import time 
   
  

"""
Every python wrapper is supposed to be similar, since they are using the same convention.

The only thing need to be changed is the guess_input function and the argparser function.

look for ## CHANGE THE FUNCTION HERE FOR DIFFERENT WRAPPER

variable inherents from utils:
myData
myPars
myPipelines
"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	
	# mainParser.add_argument('--split_fastq',  help="only run hicpro", action='store_true')
	mainParser.add_argument('--input_list',  help=argparse.SUPPRESS) # hicpro input data
	mainParser.add_argument('--queue',  default="priority")
	mainParser.add_argument('--bowtie2_k',  default="1", help="only used if --keep_up.")
	mainParser.add_argument('--bin_size',  default="10000 20000 40000 50000 100000", help="hicpro matrix bin size, e.g., 1000 2000 3000 4000 5000 10000 20000 40000 100000 150000")
	mainParser.add_argument('--hicpro_config',  default=myData['hicpro_config2'])
	mainParser.add_argument('--hichipper_config',  default=myData['hichipper_config'])
	mainParser.add_argument('--MAPS_config',  default=myData['MAPS_config'])
	mainParser.add_argument('-a','--anchor',  default="None", help="anchor list to search for interactions, if given, MAPS will be run as well")
	# mainParser.add_argument('--cutsite',  default="GATC", help="Mbol cut site")
	## fastq files must end with _R1.fastq.gz
	mainParser.add_argument('-r1', help="fastq R1", required=True)
	mainParser.add_argument('-r2', help="fastq R2", required=True)
	mainParser.add_argument('-s',"--sample_id", help="sample ID", required=True)
	mainParser.add_argument('-t',"--target_bed", help="for captureC, no more abs path required, user no more need to match the digested enzyme bed file, all automated now", default=None)
	mainParser.add_argument('--interactive',  help="run pipeline interatively", action='store_true')
	mainParser.add_argument('--rerun',  help="rerun", action='store_true')
	mainParser.add_argument('--debug',  help="debug", action='store_true')
	mainParser.add_argument('--keep_dup',  help="use this option to keep dup and keep multi-mapped reads", action='store_true')

	# group = mainParser.add_mutually_exclusive_group(required=True)
	# group.add_argument('-f',"--fastq_tsv",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID")
	# group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')		

	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="bowtie2 index file", default=myData['hg19_bowtie2_index'])
	# genome.add_argument('--bwa_index',  help="bwa index file", default=myData['hg19_BWA_index'])
	genome.add_argument('--chrom_size',  help="chrome size", default=myData['hg19_main_chrom_size'])
	# genome.add_argument('--genomic_feat_filepath',  help="MAPS genomic_feat_filepath", default=myData['hg19_genomic_feat_filepath'])
	genome.add_argument('-e','--digested_enzyme',  help="digested_fragments hg19_MboI", default="MboI")
	genome.add_argument('--chr_count',  help="chr_count", default=myPars['hg19_chr_count'])
	genome.add_argument('--digested_fragments',  help=argparse.SUPPRESS)
	genome.add_argument('--juicer_genome_size',  help=argparse.SUPPRESS)
	genome.add_argument('--ref_genome', help="in case input is hg19_20copy, but you still want to use hg19 in other programs OR -g custom, use ref_genome to locate the correct index file prefix")

	# bowtie2_index={{bowtie2_index}}
	# genome_build={{genome}}
	# cutsite={{cutsite}}
	# ncore=4
	# outdir={{jid}}	
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args




def get_hicpro_config(args):
	content = "".join(open(args.hicpro_config).readlines())
	content = multireplace(content, vars(args))
	write_file("%s/hicpro.config.txt"%(args.jid),content)

def split_fastq(outdir,input_fastq,id,read_number="R1"):
	number_reads = 100000000 ## 100M
	# subprocess.call("split_reads.py -n %s -r %s/split_reads/%s/ %s"%(number_reads,outdir,id,input_fastq),shell=True)
	# subprocess.call("module load pigz;pigz %s/split_reads/%s/*.fastq"%(outdir,id),shell=True)

	subprocess.call("mkdir -p %s/split_reads"%(outdir),shell=True)
	subprocess.call("mkdir -p %s/split_reads/%s"%(outdir,id),shell=True)
	subprocess.call("module load gcc/9.1.0; splitFastq -n %s -i %s -o %s/split_reads/%s/%s_%s"%(number_reads,input_fastq,outdir,id,id,read_number),shell=True)


def split_fastq_p(myList):
	outdir,input_fastq,id,read_number=myList
	print (outdir,input_fastq,id,read_number)
	number_reads = 100000000 ## 100M
	# subprocess.call("split_reads.py -n %s -r %s/split_reads/%s/ %s"%(number_reads,outdir,id,input_fastq),shell=True)
	# subprocess.call("module load pigz;pigz %s/split_reads/%s/*.fastq"%(outdir,id),shell=True)

	subprocess.call("mkdir -p %s/split_reads"%(outdir),shell=True)
	subprocess.call("mkdir -p %s/split_reads/%s"%(outdir,id),shell=True)
	subprocess.call("module load gcc/9.1.0; splitFastq -n %s -i %s -o %s/split_reads/%s/%s_%s"%(number_reads,input_fastq,outdir,id,id,read_number),shell=True)

def preprocess_target_bed(user_t,digestion_bed,sample):
	command = "module load bedtools;bedtools intersect -a %s -b %s -u > %s.target.bed"%(digestion_bed,user_t,sample)
	os.system(command)
	return os.path.abspath("%s.target.bed"%(sample))

def main():

	args = my_args()
	print (vars(args))
	if args.genome != "custom":
		args.juicer_genome_size = myData['%s_main_chrom_size'%(args.genome)]	
		if args.genome == "hg38":
			args.juicer_genome_size = "hg38"
		if args.genome == "mm9":
			args.juicer_genome_size = "mm9"
		args.digested_fragments = myData['%s_%s'%(args.genome,args.digested_enzyme)]
		args.index_file = myData['%s_bowtie2_index'%(args.genome)]
		args.index_file = "/".join(args.index_file.split("/")[:-1]) 
		# args.bwa_index = myData['%s_BWA_index'%(args.genome)]
		args.chrom_size = myData['%s_main_chrom_size'%(args.genome)]
		# args.genomic_feat_filepath = myData['%s_genomic_feat_filepath'%(args.genome)]
		args.chr_count = myPars['%s_chr_count'%(args.genome)]
		if args.genome == "hg19_20copy":
			args.ref_genome = "hg19_20copy"
		elif "hg19_" in args.genome:
			args.ref_genome = "hg19"
		else:
			args.ref_genome = args.genome
	else:
		args.juicer_genome_size = args.chrom_size
		args.digested_fragments = args.digested_enzyme
		# args.genome = args.ref_genome # seems not used?
	if "hybrid" in args.genome:
		args.ref_genome = args.genome
		
	if args.debug:
		submit_pipeline_jobs(myPipelines["hicpro_split_debug"],args)
		sys.exit()
	if args.rerun:
		submit_pipeline_jobs(myPipelines["hicpro_split_rerun"],args)
		sys.exit()
	if args.keep_dup:
		args.hicpro_config = myData['hicpro_config_keep_dup']
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			
	
	##------- add functions below ----------------------
	os.system("mkdir -p %s"%(args.jid))
	os.system("mkdir -p %s/log_files"%(args.jid))
	
	## split fastq files
	## gzip fastq files
	# logging.info ("Spliting Reads: %s"%(args.r1))	
	# split_fastq(args.jid,args.r1,args.sample_id,"R1")
	# logging.info ("Spliting Reads: %s"%(args.r2))	
	# split_fastq(args.jid,args.r2,args.sample_id,"R2")

	inputs = [[args.jid,args.r1,args.sample_id,"R1"],[args.jid,args.r2,args.sample_id,"R2"]]
	pool = multiprocessing.Pool(processes=2) 
	outputs = pool.map(split_fastq_p, inputs) 
	
	
	## prepare hicpro config
	get_hicpro_config(args)	
	# "%s/hicpro.config.txt"%(args.jid),
	## generate input file list
	logging.info ("Preparing HiC-Pro input")
	command = "module load hic-pro/2.11.1;cd %s; HiC-Pro -c hicpro.config.txt -i split_reads -o hicpro_results -p"%(args.jid)
	subprocess.call(command,shell=True)
		
	# exit()
	args.input_list = "%s/hicpro_results/inputfiles_hicpro.txt"%(args.jid)
	
	
	#-------------- run jobs ----------------------
	

	pipeline_name = current_file_base_name

	if args.interactive:
		run_interative_jobs(myPipelines[pipeline_name],args)
		exit()
	if args.target_bed:
		args.target_bed = preprocess_target_bed(args.target_bed,args.digested_fragments,args.sample_id)
		# print (args.target_bed)
		submit_pipeline_jobs(myPipelines["hicpro_captureC"],args)
		exit()

	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























