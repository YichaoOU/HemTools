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
	mainParser.add_argument('-f',"--input",  help="one motif sequence",required=True)
	mainParser.add_argument("--check",  help="run bedtools to check (only for custom genome)",default="")
	mainParser.add_argument('-l',"--motif_length",  help="motif_length")
	mainParser.add_argument('-n',"--num_mismatches",  help="Number of allowed mis-matches in the gRNA, excluding PAM sequence",default=0)

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. currently, only hg19 is available", default='hg19',type=str)
	genome.add_argument('--chr_fa',  help="This will be automatically changed with -g option", default=myData['hg19_chr_fa'])
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def to_casOffinder_input(args):


	out = []
	if args.genome == "custom":
		out.append(args.chr_fa)
	else:
		out.append(myData['%s_chr_fa'%(args.genome)])
	out.append("".join(["N"]*len(args.input)))
	args.motif_length = len(args.input)
	out.append(args.input+" %s"%(args.num_mismatches))

	write_file("%s/input.list"%(args.jid),"\n".join(out))
	
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
	
	## additional commands
	to_casOffinder_input(args)
	if args.genome == "custom":
		args.check = "bedtools getfasta -fi %s -bed matches.bed.bed -fo test.fa -s -name"%(args.chr_fa)
		

	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)
	
	
	
if __name__ == "__main__":
	main()







































