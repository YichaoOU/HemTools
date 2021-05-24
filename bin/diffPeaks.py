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
	requiredNamed.add_argument('-f',"--input_tsv",  help="4 column tsv, bam file, peak file, sample name, sample group",required=True)
	requiredNamed.add_argument("-d","--design_matrix",help="3 column tsv for design matrix",required=True)
	requiredNamed.add_argument("--merge_distance",help="Maximum distance between features allowed for features to be merged. Default is 0. That is, overlapping and/or book-ended features are merged.",default="0",type=str)

	mainParser.add_argument("--guess_input",  help="Let the program generate the input files for you, won't be correct, but should be helpful",action='store_true')		
	mainParser.add_argument("--MAnorm_PE_flag",help="whether input is paired-end data",action='store_true')	
	mainParser.add_argument("--continue_homer_diff",help="Not for end-user. If homer tag is available, just run homer diff",action='store_true')	
	# mainParser.add_argument('-o',"--output",default="motif_cluster_output.bed")	
	# mainParser.add_argument("--input_list",help="not for end user",default=None)	
	# mainParser.add_argument("--motif_matching_score",help="motif_matching_score",default=7)	
	# /home/yli11/Tools/TF_target_finder/data/NFIX_mouse_known_motifs.meme
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update chrom size.", default='hg19',type=str)
	genome.add_argument('-s','--genome_chrom_size',  help="chrome size", default=myData['hg19_homer_chrom_size'])
	genome.add_argument('--skip_chrom_size',  help="for homer chrom error, not for end-user. chrome size", default=myData['hg19_chrom_size'])
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def create_soft_links(f,jid):
	df = pd.read_csv(f,sep="\t",header=None)
	for bam,peak,name,group in df.values:
		# print (bam,peak,name,group)
		tmp=bam+".bai"
		if not os.path.isfile(tmp):
			print ("Can't find the .bai file for ",tmp)
			# print (os.path.islink(tmp))
			exit()
		if not name.startswith(group):
			print (name,"not start with",group)
			print ("Please update input file. Exit...")
			exit()
	for bam,peak,name,group in df.values:		
		os.system("cd %s;ln -s ../%s %s.bam"%(jid,bam,name))
		os.system("cd %s;ln -s ../%s.bai %s.bam.bai"%(jid,bam,name))
		os.system("cd %s;ln -s ../%s %s.bed"%(jid,peak,name))
def find_other_chr(f):
    df = pd.read_csv(f,sep="\t",header=None)
    df = df[df[0].str.contains("_")]
    out = df[0].tolist()+['chrM']
    # print (out)
    return " ".join(out)
def main():

	args = my_args()
	args.genome_chrom_size = myData['%s_homer_chrom_size'%(args.genome)]
	args.skip_chrom_size = myData['%s_chrom_size'%(args.genome)]
	args.skip_chrom_size = find_other_chr(args.skip_chrom_size)
	## guess input
	if args.guess_input:
		print ("not implemented yet")
		exit()
	
	
	if not os.path.isfile(args.input_tsv):
		print (args.input_tsv,"not found")
		exit()
	if not os.path.isfile(args.design_matrix):
		print (args.design_matrix,"not found")
		exit()
	if args.continue_homer_diff:
		create_soft_links(args.input_tsv,args.jid)
		submit_pipeline_jobs(myPipelines["continue_homer_diff"],args)
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
	if args.MAnorm_PE_flag:
		args.MAnorm_PE_flag = " --pe "
	else:
		args.MAnorm_PE_flag = ""
	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	create_soft_links(args.input_tsv,args.jid)
	pipeline_name = current_file_base_name
	# exit()
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























