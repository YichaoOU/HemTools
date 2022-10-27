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

TODO, overwrite genome index
"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	

	mainParser.add_argument('-f',"--input_list",  help="TSV file, 3 columns, Rep1 bam , Rep2 bam, and output name",required=True)
	mainParser.add_argument("--macs2_addon_parameters", default="")
	mainParser.add_argument("--half_width", default=200,type=int,help="half.width: a numerical value to truncate the peaks to +- half_width")

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, mm10, mm9", default='hg19',type=str)
	genome.add_argument('--macs_genome',  help="genome version: hs, mm", default='hs',type=str)
	genome.add_argument('-b','--black_list',  help="Blacklist file", default=myData['hg19_black_list'])

	

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
def main():

	args = my_args()
	args.black_list = myData['%s_black_list'%(args.genome)]

	# check input
	df = pd.read_csv(args.input_list,sep="\t",header=None)
	if df.shape[1]!=3:
		logging.error ("The input list is not tsv or the number of column is not 3!")
		exit()
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

























