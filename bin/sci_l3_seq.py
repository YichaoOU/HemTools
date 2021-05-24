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

	mainParser.add_argument('-f',"--input_list",  help="3 column bed file, additional columns are OK, but will be ignored",required=True)
	mainParser.add_argument('-b1',"--barcode_1_list",help="list of barcode 1 sequences",required=True)	
	mainParser.add_argument('-b2',"--barcode_2_list",help="list of barcode 2 sequences",required=True)	
	mainParser.add_argument('-b3',"--barcode_3_list",help="list of barcode 3 sequences",required=True)	
	
	mainParser.add_argument("--RT_PRIMER",help="RT_PRIMER seq",default="GGGATGCAGCTCGCTCCTG")	
	mainParser.add_argument("--TN5_fwd",help="TN5_fwd seq",default="AGATGTGTATAAGAGACAG")	
	mainParser.add_argument("--TN5_rev",help="TN5_rev seq",default="CTGTCTCTTATACACATCT")	


	mainParser.add_argument("--UMI_length",help="UMI_length",default=4, type=int)	
	mainParser.add_argument("--bc3_length",help="barcode 3 length",default=6, type=int)	
	mainParser.add_argument("--sp2_length",help="spacer 2 length",default=19, type=int)	
	mainParser.add_argument("--bc2_length",help="barcode 2 length",default=7, type=int)	
	mainParser.add_argument("--sp1_length",help="spacer 1 seq length",default=6, type=int)	
	mainParser.add_argument("--bc1_length",help="barcode 1 length",default=8, type=int)	


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

	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























