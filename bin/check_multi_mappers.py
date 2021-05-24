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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="check number of multi-mapped reads in rRNA, HBG1/HBG2, and chrM, and number of reads in hemoglobin genes")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('--pipeline_type',  help="Not for end-user.", default=current_file_base_name)
	mainParser.add_argument('-f',"--bam_tsv",  help="tab delimited 2 columns (tsv file): Bam file, output prefix",required=True)


	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19", default='hg19',type=str)
	genome.add_argument('--rRNA_bed',  help="rRNA genes from RSEQC UCSC", default=myData['hg19_rRNA'])
	genome.add_argument('--HBG_bed',  help="HBG region, HBG1 -- HBG2", default=myData['hg19_HBG'])
	genome.add_argument('--hem_bed',  help="Hemoglobin genes", default=myData['hg19_hem'])
	genome.add_argument('-i','--index_file',  help="Kallisto index file", default=myData['hg19_kallisto_index'])
	genome.add_argument('--gene_info',  help="gene info t2g file for sleuth", default=myData['hg19_t2g'])


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

	##--------------- parameter replacement ------------
	
	args.rRNA_bed = myData['%s_rRNA'%(args.genome)]
	args.HBG_bed = myData['%s_HBG'%(args.genome)]
	args.hem_bed = myData['%s_hem'%(args.genome)]
	
	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()







































