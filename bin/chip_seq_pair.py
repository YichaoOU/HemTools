#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


"""
Every python wrapper is supposed to be similar, since they are using the same convention.

The only thing need to be changed is the guess_input function and the argparser function.


"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('--debug',  help="Not for end-user.", action='store_true')
	mainParser.add_argument('--short',  help="Not for end-user.", action='store_true')
	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-f',"--fastq_tsv",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID")
	group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')		

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="BWA index file", default=myData['hg19_BWA_index'])
	genome.add_argument('-b','--black_list',  help="Blacklist file", default=myData['hg19_black_list'])
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])
	genome.add_argument('-e','--effectiveGenomeSize',  help="effectiveGenomeSize for bamCoverage", default=myPars['hg19_effectiveGenomeSize'])
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	
	##------- setup logger -----------------------------
	logger = setup_custom_logger(args.jid)
	
	##------- guess input ------------------------------
	if args.guess_input:
		logger.info("preparing input files")
		flag,fname = prepare_paired_end_input()
		os.system("rm "+args.jid+".log")		
		sys.exit(1)	
		
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logger.info ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logger.info ("The new job id is: "+args.jid)
	else:
		logger.info ("The job id is: "+args.jid)			
	
	##------- add functions below ----------------------
	#------------- check input 
	
	if not check_NGS_input(args):
		os.system("rm "+args.jid+".log")
		sys.exit(1)
	
	#-------------- run jobs 
	
	os.system("mkdir %s"%(args.jid))
	if args.short: ## for debug
		submit_pipeline_jobs(myPipelines[current_file_base_name+"_short"],args,logger)
	else:
		submit_pipeline_jobs(myPipelines[current_file_base_name],args,logger)
	
	
	#-------------- upload tracks 
	
	
	
	
	
	#-------------- generate html 
	
	
	
	
	
	#-------------- check job log files and organize output 
	
	
	
	
	#-------------- send email
	
	
	
	
	

	


	
	
	
	
if __name__ == "__main__":
	main()

























