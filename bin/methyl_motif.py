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

	mainParser.add_argument('-f',"--bed_file",  help="TSV file, make sure the first 3 columns are chr, start, end",required=True)
	mainParser.add_argument('-o',"--output_prefix",  help="Output file name (prefix-)", required=True)
	mainParser.add_argument("--methyl_alphabet",  default=myPars['methyl_alphabet'])
	mainParser.add_argument("--cellLine",help="available: hudep1, hudep2",required=True)
	mainParser.add_argument("--methyl_cutoff",help="available cutoffs: 0.6, 0.7, 0.8, 0.9",default="0.6")

	mainParser.add_argument('--helper_dir',  default=myPars['helper_dir'])
	# mainParser.add_argument('--short',  help="Not for end-user.", action='store_true')
	# mainParser.add_argument('--pipeline_type',  help="Not for end-user.", default=current_file_base_name)
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19", default='hg19',type=str)
	genome.add_argument('--genome_fa',  help="genome fasta", default=myData['hg19_fasta'])
	genome.add_argument('--known_motif',  help="known motifs", default=myData['hg19_motif'])
	genome.add_argument('--typeE_graph',  help="graph file for mEpigram", default=myData['typeE_graph'])
	genome.add_argument('--typeEF_graph',  help="graph file for mEpigram", default=myData['typeEF_graph'])
	genome.add_argument('--mepigram_dir',  help="executables for mEpigram", default=myPars['mepigram_dir'])
	genome.add_argument('--methy_genome_typeE',  help="known motifs", default=myData['hg19_hudep1_0.6_genome_TypeE'])
	genome.add_argument('--background_typeE_tsv',  help="known motifs", default=myData['hg19_hudep1_0.6_background_typeE'])
	genome.add_argument('--methy_genome_typeEF',  help="known motifs", default=myData['hg19_hudep1_0.6_genome_TypeEF'])
	genome.add_argument('--background_typeEF_tsv',  help="known motifs", default=myData['hg19_hudep1_0.6_background_typeEF'])
	

	
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
	
	##------- add functions below ----------------------
	#------------- check input ----------------------
	if not isfile(args.bed_file):
		logging.error ("%s not found"%args.bed_file)
		sys.exit(1)
	#-------------- run jobs ----------------------
	
	cellLine = str(args.cellLine).lower()
	args.methy_genome_typeE = myData["hg19_%s_0.6_genome_TypeE"%(cellLine)]
	args.background_typeE_tsv = myData["hg19_%s_0.6_background_typeE"%(cellLine)]
	args.methy_genome_typeEF = myData["hg19_%s_0.6_genome_TypeEF"%(cellLine)]
	args.background_typeEF_tsv = myData["hg19_%s_0.6_background_typeEF"%(cellLine)]
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























