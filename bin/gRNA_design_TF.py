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
	requiredNamed = mainParser.add_argument_group('required named arguments')
	requiredNamed.add_argument('-TAD',"--TAD_file",  help="bed file, at least 4 columns",required=True)
	requiredNamed.add_argument('-peak',"--peak_file",  help="bed file, at least 4 columns",required=True)
	requiredNamed.add_argument('-motif',"--motif_file",  help="bed file, at 6 columns, containing strand",required=True)
	requiredNamed.add_argument('-gene',"--gene_file",  help="bed file, at least 4 columns",required=True)
	requiredNamed.add_argument('-off_target',"--Num_match_file",  help="tsv file, 2 columns, sgRNA seq and number of matches in the genome",required=True)
	requiredNamed.add_argument('-e',"--editable_base",  help="editable base",default="A")
	

	mainParser.add_argument('-l',"--flanking_length",help="number of bp flanking the motif bed file",default=25,type=int)	
	mainParser.add_argument("--PAM_seq",help="PAM seq",default="NGG",type=str)	
	mainParser.add_argument("--motif_position_anchor",help="which position to use as +1 position, default is for WGATAR, where the first A is used as +1 then T is -1",default=3,type=int)	

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update chrom size.", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="genome version: hs, mm", default=myData['hg19_fasta'],type=str)
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	if args.genome!="custom":
		args.genome_fasta = myData['%s_fasta'%(args.genome)]
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

	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























