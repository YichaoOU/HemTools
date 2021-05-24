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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="motif annotation")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()),type=str)	
	mainParser.add_argument('-f','--bed_file',  help="a bed file with chr, start, end as the first 3 columns, addtional columns will be ignored", required=True)

	mainParser.add_argument('--treatment_bam',  help=argparse.SUPPRESS)
	mainParser.add_argument('--control_bam',  help=argparse.SUPPRESS)
	mainParser.add_argument("-d1",help="extend query bed for intersection",default=0,type=int)	
	mainParser.add_argument("-d2",help="extend tss for intersection",default=2000,type=int)	
	mainParser.add_argument("-d3",help="extend epi for intersection",default=0,type=int)	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-m','--motif_list',  help="a list of motif location bed files", default=myData['hg19_motif_list'])
	genome.add_argument('-a','--gene_annotation',  help="gene annotation file", default=myData['hg19_gene_annotation'])

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	args.motif_list = myData['%s_motif_list'%(args.genome)]
	args.gene_annotation = myData['%s_gene_annotation'%(args.genome)]


	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		args.jid= args.jid.replace(".bed","")		
		logging.info ("The job id is: "+args.jid)		

	#-------------- some helpers ----------------------

	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)


if __name__ == "__main__":
	main()







































