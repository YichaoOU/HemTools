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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="plot correlation for all bw files in the current dir")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--bw_files",  help="input file or use all bw files in the current dir", default="None")
	mainParser.add_argument('-b',"--bin_size", default=10000)
	mainParser.add_argument("--bed_file", default="")
	mainParser.add_argument('-r',"--region", default="None",help="Could be chr11:5267561-5277281, HBG region")
	mainParser.add_argument('-o',"--output", default="plotCorrelation")
	mainParser.add_argument("--addon_parameter", default="")
	# mainParser.add_argument("--whole_genome",action='store_true')
	


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	if args.region != "None":
		args.addon_parameter += " -r %s"%(args.region)

		
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			


	#-------------- run jobs ----------------------
	if args.bw_files == "None":
		files = glob.glob("*.bw")
		if len(files) < 2:
			os.system("%s -h"%(sys.argv[0]))
			print ("Less than 2 bw files. Program exit!")
			exit()
		args.bw_files = " ".join(files)
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	submit_pipeline_jobs(myPipelines["bw_corr"],args)

	
if __name__ == "__main__":
	main()







































