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
	mainParser.add_argument('-f',"--bed_file",  help="input bed file for featureCount",required=True)
	mainParser.add_argument('-o',"--output",  help="output file name",default="featureCount")
	
	mainParser.add_argument("--bam_file_list",  help="HemTools blood collection",default=myData['blood_ATAC_bam'])
	mainParser.add_argument("--bw_list",  help="HemTools blood collection",default=myData['blood_ATAC_bw'])

	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument("--on_bw",  help="extract values based on bw files", action='store_true')
	group.add_argument("--on_bam",  help="extract values based on bam files", action='store_true')	


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def to_bed4(args):
	
	command = """awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$1":"$2"-"$3}' %s > %s/my.input"""%(args.bed_file,args.jid)
	os.system(command)

def main():

	args = my_args()
	args.bam_file_list = " ".join(read_file_to_list(args.bam_file_list))
	
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
	to_bed4(args)
	if args.on_bam:
		submit_pipeline_jobs(myPipelines["blood_ATAC"],args)
	if args.on_bw:
		submit_pipeline_jobs(myPipelines["blood_ATAC_bw"],args)

	
if __name__ == "__main__":
	main()

























