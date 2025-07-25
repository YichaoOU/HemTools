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
	mainParser.add_argument("--bamCoverage_addon",  help="for PE data, you add --center to get sharper peaks", default="")
	mainParser.add_argument("--MNase",  help="bw for MNase",action='store_true')		
	mainParser.add_argument('file', type=str, nargs='+')
	mainParser.add_argument("--no_filter",  help="no_filter for input bam",action='store_true')
	mainParser.add_argument('--input', help=argparse.SUPPRESS)
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-e','--effectiveGenomeSize',  help="effectiveGenomeSize for bamCoverage", default=myPars['hg19_effectiveGenomeSize'])

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


	
def main():

	args = my_args()
	args.effectiveGenomeSize = myPars['%s_effectiveGenomeSize'%(args.genome)]
	
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)	
	args.input = args.jid+".input"
	write_file(args.input,"\n".join(args.file))
	
	##------- add functions below ----------------------
	
	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	if args.no_filter:
		pipeline_name+="_no_filter"
	if args.MNase:
		pipeline_name="bam_MNase_coverage"
	submit_pipeline_jobs(myPipelines[pipeline_name],args)
	# bam_to_bw_no_filter
	
if __name__ == "__main__":
	main()

























