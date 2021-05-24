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
	mainParser.add_argument("--label",  help="required if --vcf_file is used", default="label")

	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('--vcf_file',  help="a single vcf file containing all the mutation to be added to the fasta")
	group.add_argument("--mutation_list",  help="a list of mutations, each mutation makes a new genome")	


	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options. input of hg19custom will replace anything that is supplied by user and use the default if not supplied", default='hg19',type=str)
	genome.add_argument('-b','--black_list',  help="Blacklist file", default=None)
	genome.add_argument('-fa','--genome_fa',  help="genome fasta file", default=None)
		



	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args



def main():

	args = my_args()
	
	if "custom" in args.genome:
		genome = args.genome.replace("custom","")
		default_black_list = myData['%s_black_list'%(genome)]
		default_genome_fasta = myData['%s_fasta'%(genome)]
		if args.black_list == None:
			args.black_list = default_black_list
		if args.genome_fa == None:
			args.genome_fa = default_genome_fasta
	else:
		args.black_list = myData['%s_black_list'%(args.genome)]
		args.genome_fa = myData['%s_fasta'%(args.genome)]		


	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			
	
	##------- add functions below ----------------------
	
	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))

	if args.mutation_list:
	
		submit_pipeline_jobs(myPipelines["new_genome"],args)
	if args.vcf_file:
		submit_pipeline_jobs(myPipelines["new_genome_multiple"],args)

	
if __name__ == "__main__":
	main()

























