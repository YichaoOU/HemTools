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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="General variant calling method using samtools mpileup, useful for ChIP-seq or ATAC-seq to find allele-specific binding or chromatin accessibility.")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('--pipeline_type',  help="Not for end-user.", default=current_file_base_name)
	mainParser.add_argument('-d',"--depth_filter", help="filter variants by raw read depth (this depth contains unfiltered reads)", default=5,type=int)
	mainParser.add_argument('-f',"--bam_list",  help="tab delimited 2 columns (tsv file): path_to_bam_file, sample ID",required=True)
	mainParser.add_argument("--mpileup_addon_parameters",  help="if you have a specific region to search for, you can do -l path_to_bed",default="")
	mainParser.add_argument("--help_dir",  help="not for end-user",default=myPars['helper_scripts'])

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19. Only working for hg19", default='hg19',type=str)
	genome.add_argument('--samtools_fa_index',  help="samtools fa index", default=myData['hg19_samtools_index'],type=str)

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
			
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			
	
	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























