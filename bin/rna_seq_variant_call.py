#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


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
	mainParser.add_argument('--pipeline_type',  help="Not for end-user.", default=current_file_base_name)
	mainParser.add_argument('-d',"--depth_filter", help="filter variants by read depth", default=10,type=int)
	mainParser.add_argument("-WT", help="specify a WT name to compare all samples to this WT sample", default=None)
	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-f',"--fastq_tsv",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID")
	group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')		
	# group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')		

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19. Only working for hg19", default='hg19',type=str)
	genome.add_argument('--STAR_index',  help="genome version: hg19. Only working for hg19", default='/research/dept/hem/common/sequencing/chenggrp/pipelines/hg19/hg19_star_253a_index/',type=str)

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	
	##------- guess input ------------------------------
	if args.guess_input:
		logging.info("preparing input files")
		## CHANGE THE FUNCTION HERE FOR DIFFERENT WRAPPER
		flag,fname = prepare_paired_end_input() 
		sys.exit(1)	
		
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			
	
	##------- add functions below ----------------------
	#------------- check input ----------------------
	## CHANGE THE FUNCTION HERE FOR DIFFERENT WRAPPER
	if not check_NGS_input(args):
		sys.exit(1)
	
	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	if args.WT:
		submit_pipeline_jobs(myPipelines[pipeline_name+"_compare"],args)
	else:
		submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























