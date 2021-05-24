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

	mainParser.add_argument('-q',"--query_bed",  help="3 column bed file, additional columns are OK, but will be ignored",required=True)
	mainParser.add_argument("-exp","--deg_tsv",help="any number of columns, first column should be gene name, first row should be column names. should contain FDR and LFC.",required=True)	
	mainParser.add_argument("--query_motif",help="query_motif pwm file",required=True)	
	# /home/yli11/Tools/TF_target_finder/data/NFIX_mouse_known_motifs.meme

	mainParser.add_argument('-tss',"--tss_bed",help="4 column bed file, the 4th column should be gene name, should match to the gene name in DEG file (if supplied). Additional columns are OK, but will be ignored",default="/home/yli11/Data/Mouse/mm9/annotations/mm9.ensembl_v67.TSS.gene_name.bed")		
	mainParser.add_argument("-epi","--epi_bed",help="5 column bed file, the 4th column should be gene name, should match to the gene name in DEG file and TSS annotation(if supplied). The 5th column should be score (optional). Additional columns are OK, but will be ignored",default="/home/yli11/Tools/TF_target_finder/data/HPC7.mm9.captureC.bed")	
	
	
	mainParser.add_argument("--LFC_col_name",help="LFC_col_name",default="logFC")	
	mainParser.add_argument("--FDR_col_name",help="FDR_col_name",default="adj.P.Val")	
	mainParser.add_argument("--LFC_cutoff",help="LFC cutoff",default=1,type=float)	
	mainParser.add_argument("--FDR_cutoff",help="FDR cutoff",default=0.05,type=float)	
	
	mainParser.add_argument("-d1",help="extend query bed for intersection",default=0,type=int)	
	mainParser.add_argument("-d2",help="extending tss for intersection",default=5000,type=int)	
	mainParser.add_argument("-d3",help="extending epi for intersection",default=0,type=int)	
	mainParser.add_argument("-d4",help="for motif scanning: extend search on the flank sequences",default=100,type=int)	
	mainParser.add_argument("-d5",help="distance cutoff for peak overlap, used for co-binding test",default=500,type=int)	
	mainParser.add_argument("-d6",help="distance cutoff for motif overlap, used for co-binding test",default=100,type=int)	

	mainParser.add_argument("--motif_database",help="motif meme file",default="/home/yli11/Data/Motif_database/Mouse/mouse_TF.meme")	
	mainParser.add_argument('--motif_list',help="motif_list",default="/home/yli11/HemTools/share/misc/TF_target_finder/motif.list")	
	mainParser.add_argument('--peak_list',help="peak_list",default="/home/yli11/HemTools/share/misc/TF_target_finder/peak.list")	
	mainParser.add_argument('--assign_targets_addon_parameters',help="any addon parameters",default="")	
	mainParser.add_argument('--label',help="give a name for your TF (i.e., query)",default="target_finder")	
	

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
	
	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))

	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























