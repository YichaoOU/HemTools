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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="starr-seq pipeline")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--fastq_tsv",  help="paired-end fastq tsv", required=True)
	mainParser.add_argument("-d","--design_matrix",help="3 column tsv for design matrix",required=True)
	mainParser.add_argument('-bs',"--bin_size",  help="bin_size", default=500,type=int)
	mainParser.add_argument('-ss',"--step_size",  help="step_size", default=100,type=int)
	mainParser.add_argument('-c',"--FDR_cutoff",  help="FDR_cutoff", default=0.05,type=float)
	mainParser.add_argument('-min',"--min_frag",  help="min_frag size", default=200,type=int)
	mainParser.add_argument('-max',"--max_frag",  help="max_frag size", default=1000,type=int)
	mainParser.add_argument('-q',"--MAPQ",  help="MAPQ cutoff", default=40,type=int)
	mainParser.add_argument('-a',"--addon_parameters",  help="other parameters to add to starrPeaker", default="",type=str)


	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="BWA index file", default=myData['hg19_BWA_index'])

	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_starr_chrom_size'])
	genome.add_argument('-b','--blacklist',  help="blacklist size", default=myData['hg19_black_list'])
	genome.add_argument('--gc_cov',  help="gc_cov", default=myData['hg19_gc_cov'])
	genome.add_argument('--map_cov',  help="map_cov", default=myData['hg19_map_cov'])
	genome.add_argument('--conv_cov',  help="conv_cov", default=myData['hg19_conv_cov'])


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	if args.genome != "custom":
		args.chrom_size = myData['%s_starr_chrom_size'%(args.genome)]
		args.index_file = myData['%s_BWA_index'%(args.genome)]
		args.gc_cov = myData['%s_gc_cov'%(args.genome)]
		args.map_cov = myData['%s_map_cov'%(args.genome)]
		args.conv_cov = myData['%s_conv_cov'%(args.genome)]
		args.blacklist = myData['%s_black_list'%(args.genome)]

		
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))

	#-------------- run jobs ----------------------



	submit_pipeline_jobs(myPipelines[current_file_base_name],args)

	
if __name__ == "__main__":
	main()







































