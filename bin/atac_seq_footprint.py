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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="RGT_HINT atac-seq footprint with bias correction")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('--pipeline_type',  help=argparse.SUPPRESS, default=current_file_base_name)
	mainParser.add_argument('-f','--input',  help="3-col tsv, bam,bed,output-prefix", required=True)
	mainParser.add_argument('-t','--treatment',  help="default is the output-prefix in the first row. treatment output-prefix for differential footprint analysis, should match to names in the input file", default=None)
	mainParser.add_argument('-c','--control',  help="default is the second row. control output-prefix for differential footprint analysis", default=None)
	mainParser.add_argument('--softlinks',  help=argparse.SUPPRESS,default="")
	mainParser.add_argument('--treatment_bam',  help=argparse.SUPPRESS)
	mainParser.add_argument('--control_bam',  help=argparse.SUPPRESS)

	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def match_rgt_database_chromosome_names(f,rgt_chr_size):
	command = """awk -F "\t" '{print $1"\t0\t"$2}' %s > rgt.bed"""%(rgt_chr_size)
	os.system(command)
	command = "module load bedtools;bedtools intersect -a %s -b rgt.bed -u > %s.rgt.input.bed"%(f,f)
	os.system(command)
	return "%s.rgt.input.bed"%(f)
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

	#-------------- some helpers ----------------------
	df = pd.read_csv(args.input,sep="\t",header=None)
	if df.shape[0]>1:
		df.index = df[2]
		myDict = df[0].to_dict()
		if args.treatment == None:
			args.treatment = df[2].tolist()[0]
		if args.control == None:
			args.control = df[2].tolist()[1]
		args.treatment_bam = myDict[args.treatment]
		args.control_bam = myDict[args.control]


	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	if username != "yli11":	
		os.system("ln -s /home/yli11/rgtdata/ /home/%s/rgtdata"%(username))
		args.softlinks = "rm /home/%s/rgtdata"%(username)
	new_names = []
	for f in df[1].tolist():
		new_names.append(match_rgt_database_chromosome_names(f,"/home/yli11/rgtdata/{0}/chrom.sizes.{0}".format(args.genome)))
	df[1] = new_names
	df.to_csv("%s.input"%(args.jid),sep="\t",header=False,index=False)
	args.input = "%s.input"%(args.jid)
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

		
if __name__ == "__main__":
	main()







































