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

	mainParser.add_argument('-f',"--fastq_tsv",  help="TSV file, 3 columns, peak, bam, output, need absolute path to file",required=True)
	mainParser.add_argument('-d',"--peakcall_tsv",  help="TSV file, 3 columns, peak, bam, output, need absolute path to file",required=True)
	mainParser.add_argument("--scale_multiplier",default=10000)
	mainParser.add_argument("--Ecoli_index_file",default="/home/yli11/Data/E_coli/MG1655.fa",help="Yeast: /home/yli11/Data/E_coli/Yeast/sacCer3.fa")
	# mainParser.add_argument("--only_cut_sites_bw", action='store_true')
	# mainParser.add_argument("--Liu_Nan_pipeline_path_atactk", help="not for end-user", default="/home/yli11/Programs/cut_run_pipeline_Nan_Liu/git/atactk/scripts")
	# mainParser.add_argument("--Liu_Nan_pipeline_path_root", help="not for end-user", default="/home/yli11/Programs/cut_run_pipeline_Nan_Liu")
	mainParser.add_argument('--MACS2_genome',  help=argparse.SUPPRESS)

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, mm10, mm9", default='hg19',type=str)
	# genome.add_argument('--genome_fasta',  help="genome version: hs, mm", default=myData['hg19_fasta'],type=str)
	genome.add_argument('-b','--black_list',  help="Blacklist file", default=myData['hg19_black_list'])
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])
	genome.add_argument('-i','--index_file',  help="chrome size", default=myData['hg19_BWA_index'])
	genome.add_argument('--gene_body',  help="chrome size", default=myData['hg19_gene_body'])

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	if "hg" in args.genome:
		args.MACS2_genome = "hs"
	else:
		args.MACS2_genome = "mm"
	# args.genome_fasta = myData['%s_fasta'%(args.genome)]
	args.black_list = myData['%s_black_list'%(args.genome)]
	args.chrom_size = myData['%s_chrom_size'%(args.genome)]
	args.index_file = myData['%s_BWA_index'%(args.genome)]
	args.gene_body = myData['%s_gene_body'%(args.genome)]

		
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
	
	# dos2unix(args.motif_list)
	# dos2unix(args.input_tsv)

	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))

	pipeline_name = current_file_base_name

	submit_pipeline_jobs(myPipelines[pipeline_name],args)
		

	
if __name__ == "__main__":
	main()

























