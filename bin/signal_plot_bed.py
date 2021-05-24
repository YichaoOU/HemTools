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
	# mainParser.add_argument('--current_dir',  help="plot all bw files and all bed files",action='store_true' )
	mainParser.add_argument("-u",  help="upstream flanking length",default=5000,type=int)
	mainParser.add_argument("-d",  help="downstream flanking length",default=5000,type=int)	
	mainParser.add_argument("-s",  help="bin size",default=50,type=int)	
	mainParser.add_argument("--computeMatrix_addon_parameters",  help="add user-defined parameters to computeMatrix",default="")
	mainParser.add_argument("-c","--colors",help="colors, seperated by comma, hex color is OK",default="red,green,blue,yellow,grey,purple,darkgreen,darkred,pink,orange")
	mainParser.add_argument('--bw_files',  help="bw_file_list",required=True,nargs='+')
	mainParser.add_argument('-f','--bed',  help="one bed file",required=True)
	mainParser.add_argument('--plotProfile_addon_parameters',  help="plotProfile_addon_parameters",default="")
	# mainParser.add_argument('--yMax',  help="yMax",default="")
	

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
	args.bw_files = " ".join(args.bw_files)

	submit_pipeline_jobs(myPipelines["signal_plot_bed"],args)

	
if __name__ == "__main__":
	main()







































