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

	mainParser.add_argument('-f',"--input_list",  help="tsv 4 columns, bam 1, bam 2, peak 1, peak 2. Relative or Absolute path.",required=True)

	mainParser.add_argument('--bw',  help="input is bw, not bam", action='store_true')
	mainParser.add_argument('--intersect',  help="input is bw, not bam", action='store_true')
	mainParser.add_argument("--featureCount_addon_parameters",  help="if paired data add -p option",default="")
	mainParser.add_argument("--highlight",  help="highlight bed file",default="")
	mainParser.add_argument('-i','--interactive',  help="run pipeline interatively", action='store_true')



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
	if args.bw:
		pipeline_name = current_file_base_name + "_bw"
	if args.intersect:
		pipeline_name = pipeline_name+"_intersection"
	if args.interactive:
		run_interative_jobs(myPipelines[current_file_base_name],args)
		exit()
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























