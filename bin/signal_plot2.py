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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="signal plot 2")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('--current_dir',  help="plot all bw files and all bed files",action='store_true' )
	mainParser.add_argument("-u",  help="upstream flanking length",default=5000,type=int)
	mainParser.add_argument("-d",  help="downstream flanking length",default=5000,type=int)	
	mainParser.add_argument('--bw_list',  help="bw_file_list",default="None")
	mainParser.add_argument('--bed_list',  help="bed_list",default="None")
	

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


	if args.current_dir:
		bw_list = glob.glob("*.bw")
		args.bw_list = args.jid+".input"
		write_file(args.bw_list,"\n".join(bw_list))
		bed_list = glob.glob("*.bed")+glob.glob("*Peak")
		args.bed_list = " ".join(bed_list)
	else:
		args.bed_list = " ".join(read_file_to_list(args.bed_list))
	

	#-------------- run jobs ----------------------

	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	

	submit_pipeline_jobs(myPipelines[current_file_base_name],args)

	
if __name__ == "__main__":
	main()







































