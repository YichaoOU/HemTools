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

better to use it for one TF or a group of related TFs

"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--fasta",  help="input query fasta",required=True)
	mainParser.add_argument('-m',"--motif_file",  help="meme file",default="/home/yli11/Data/Motif_database/Human/human.meme")
	# mainParser.add_argument('-o',"--output",  help="output csv",required=True)
	mainParser.add_argument('-p',"--fimo_cutoff",  default=0.0001)
	# mainParser.add_argument("--fimo_addon",  default="")
	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()

	#------- check if jid exist  ----------------------
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


	# fimo
	command = "module load meme/4.11.2;fimo --verbosity 1 --text --thresh  {0} {1} {2} > {3}/motif_finding_result.tsv".format(args.fimo_cutoff,args.motif_file,args.fasta,args.jid)
	logging.info (command)
	os.system(command)
	
	df = pd.read_csv("%s/motif_finding_result.tsv"%(args.jid),sep="\t")
	df = df.sort_values("p-value")
	df.to_csv("%s/motif_finding_result.tsv"%(args.jid),sep="\t",index=False)
	
	

if __name__ == "__main__":
	main()

























