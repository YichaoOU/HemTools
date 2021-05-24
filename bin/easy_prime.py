#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


"""
Every python wrapper is supposed to be similar, since they are using the same convention.

The only thing need to be changed is the guess_input function and the argparser function.


"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--input_list",  help="a list of variants 5 columns chr, pos, name, ref, alt",required=True)
	mainParser.add_argument('--PAM_seq', help="specify the PAM sequence, e.g., NGG.",default="NGG")
	mainParser.add_argument('-e','--extend',  help="Define a region to look for gRNAs, extend search area to left and right", default=200,type=int)
	mainParser.add_argument('-l','--sgRNA_length',  help="sgRNA_length", default=20)
	mainParser.add_argument('-o',"--output",  help="output file name",default=username+"_"+str(datetime.date.today()))
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. currently, only hg19 is available", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="genome version: hs, mm", default=myData['hg19_fasta'],type=str)	
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


	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	

	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines["easy_prime_alpha"],args)
	
	
	
if __name__ == "__main__":
	main()







































