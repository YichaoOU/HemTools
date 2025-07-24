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

	mainParser.add_argument('-r','--region_file',  help="gRNA_bed required",required=True)
	mainParser.add_argument('-f','--bam_list',  help="gRNA_bed required",required=True)
	mainParser.add_argument('--ref',  help="reference base",default="A",type=str)
	mainParser.add_argument('--alt',  help="alternative base",default="G",type=str)
	mainParser.add_argument('--center',  help="center",default=-10,type=int)
	mainParser.add_argument('--w_size',  help="w_size",default=10,type=int)
	mainParser.add_argument('--min_reads',  help="min_reads",default=50,type=int)
	mainParser.add_argument('--addon_parameters',  help="additional paramteeres, such as --min_paired_end_reads_overlap for crispresso",default="",type=str)
	# mainParser.add_argument("--info_tsv", help=argparse.SUPPRESS)
	mainParser.add_argument("--input_list", help=argparse.SUPPRESS)
	mainParser.add_argument('--queue',  help="which queue to use",default='standard')

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="genome fasta file", default=myData['hg19_fasta'])

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def create_info_tsv(region_file,jid):
	df = pd.read_csv(region_file,sep="\t",header=None)
	df = df[[3,3,4]].to_csv("%s/info.tsv"%(jid),sep="\t",header=False,index=False)
	

def main():

	args = my_args()
	args.genome_fasta = myData['%s_fasta'%(args.genome)]
	print (args.genome_fasta)
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
	create_info_tsv(args.region_file,args.jid)
	submit_pipeline_jobs(myPipelines["crispressoWGS_BE"],args)


	
if __name__ == "__main__":
	main()

























