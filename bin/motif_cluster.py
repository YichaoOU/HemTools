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

	mainParser.add_argument('-f',"--input_bed",  help="3 column bed file, additional columns are OK, but will be ignored",required=True)
	mainParser.add_argument("-m","--motif",help="motif database homer format",default="/home/yli11/Data/Motif_database/homer/combined.homer.motif")	
	mainParser.add_argument("--motif_cluster_score",help="motif_cluster_score",default=5)	
	mainParser.add_argument('-o',"--output",default="motif_cluster_output.bed")	
	mainParser.add_argument("--input_list",help="not for end user",default=None)	
	mainParser.add_argument("--motif_matching_score",help="motif_matching_score",default=7)	
	# /home/yli11/Tools/TF_target_finder/data/NFIX_mouse_known_motifs.meme
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, mm10, mm9, hg38", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="genome version: hs, mm", default=myData['hg19_fasta'],type=str)


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def split_input_bed(x,jid):
	os.system("split -l 200 {0} {1}/input.split.;cd {1};ls input.split.* > ../{1}.input".format(x,jid))

def main():

	args = my_args()
	args.genome_fasta = myData['%s_fasta'%(args.genome)]
	if not os.path.isfile(args.motif):
		print (args.motif,"not found")
		exit()
	if not os.path.isfile(args.input_bed):
		print (args.motif,"not found")
		exit()
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
	split_input_bed(args.input_bed,args.jid)
	args.input_list = "%s.input"%(args.jid)
	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























