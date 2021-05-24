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
	mainParser.add_argument("-o","--output_label",  help="output_label", required=True)
	mainParser.add_argument("-fa","--ref_fa",  help="reference fa", default=None)
	mainParser.add_argument("-fq","--fastq_file",  help="MinION fastq file", required=True)
	mainParser.add_argument("--ngmlr_addon_parameters",  help="MinION fastq file", default=None)
	mainParser.add_argument("--wtdbg2_addon_parameters",  help="MinION fastq file", default=None)
	mainParser.add_argument("--wtpoa_cns_addon_parameters",  help="MinION fastq file", default=None)
	mainParser.add_argument("-m","--mem",  help="required mem in MB", default=15000)
	mainParser.add_argument("-k","--kmer",  help="kmer size", default=13)


	mainParser.add_argument('-s','--genome_size',  help="Approximate genome size (k/m/g suffix allowed)", default=0)
	



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
	
	##------- add functions below ----------------------
	
	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))


	submit_pipeline_jobs(myPipelines["minion_lance"],args)

if __name__ == "__main__":
	main()

























