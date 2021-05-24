#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
file_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
# print (file_dir)

"""
run a custom lsf script

make sure my_args() contains all your parameters

"""
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='Pipeline-type_'+username+"_"+str(datetime.date.today()))	
	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-p','--pipeline_name',  help="which pipeline to run, e.g., atac_seq")
	group.add_argument("--list_pipelines",  help="list all available pipelines",action='store_true')		
	group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')
	group.add_argument('-lsf',"--user_lsf",  help="user defined lsf file")
	
	
	mainParser.add_argument('-f',"--input",  help="tab delimited any number of columns (tsv file), the last column is output prefix. For example, a paired-end fastq input could be: Read 1 fastq, Read 2 fastq, sample ID")
	mainParser.add_argument('-q',"--queue",  help="submit queue",default="standard")
	mainParser.add_argument('-mem',"--memory",  help="request memory",default=20000, type=int)


	mainParser.add_argument('-f2',"--input2",  help="for jobs with dependencies. tab delimited any number of columns (tsv file), the last column is output prefix. For example, a paired-end fastq input could be: Read 1 fastq, Read 2 fastq, sample ID")
	
	
	# mainParser.add_argument("--single",  help="default is paired-end data, specify this parameter if you have single-end data",action='store_true')		
	mainParser.add_argument("--csv",  help="convert tsv to csv when doing guess_input",action='store_true')		
	mainParser.add_argument("--email",  help="send user the fastq.tsv file",action='store_true')		

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="BWA index file", default=myData['hg19_BWA_index'])
	genome.add_argument('-b','--black_list',  help="Blacklist file", default=myData['hg19_black_list'])
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])
	genome.add_argument('-e','--effectiveGenomeSize',  help="effectiveGenomeSize for bamCoverage", default=myPars['hg19_effectiveGenomeSize'])
	mainParser.add_argument('--interactive',  help="run pipeline interatively", action='store_true')

	##------- add parameters above ---------------------
	# args = mainParser.parse_args()	
	args,unknown = mainParser.parse_known_args()
	for i in range(0,len(unknown),2):
		mainParser.add_argument(unknown[i],default=unknown[i+1])
	args = mainParser.parse_args()
	return args


def main():

	args = my_args()
	if args.list_pipelines:
		print ("All available pipelines are shown below:")
		available_pipes = list(set([x.lower() for x in myPipelines]))
		for k in available_pipes:
			print (k)
		print ("----------------------------------------")
		sys.exit(1)	
	args.index_file = myData['%s_BWA_index'%(args.genome)]
	args.chrom_size = myData['%s_chrom_size'%(args.genome)]	
	# args.black_list = myData['%s_blacklist'%(args.genome)]	
	# args.effectiveGenomeSize = myData['%s_effectiveGenomeSize'%(args.genome)]	
	##------- guess input ------------------------------
	if args.guess_input:
		logging.info("preparing input files")
		## CHANGE THE FUNCTION HERE FOR DIFFERENT WRAPPER
		flag,fname = prepare_paired_end_input() 
		if args.csv:
			df = pd.read_csv(fname,sep="\t",header=None)
			## just for Shengdar's target seq, need abs path
			abs_path = os.getcwd()
			df[0] = abs_path+"/"+df[0]
			df[1] = abs_path+"/"+df[1]
			os.system("rm %s"%(fname))
			fname = fname.replace(".tsv",".csv")
			df.to_csv(fname,index=False,header=False)
		if args.email:
			os.system("""%ssend_email_v1.py -a %s -m "See attached file" -j %s --common"""%(file_dir,fname,args.jid))
		sys.exit(1)	
		
	##------- find which pipeline to use  ----------------------

	
	if args.pipeline_name == None:
		pipeline_name = ".".join(str(args.user_lsf).split("/")[-1].split(".")[:-1])
		current_pipeline = args.user_lsf
	else:
		pipeline_name = str(args.pipeline_name).lower()
		if not pipeline_name in myPipelines:
			logging.error("%s not found."%(pipeline_name))
			sys.exit(1)
		current_pipeline = myPipelines[pipeline_name]
	##------- check if jid exist  ----------------------
	args.jid = args.jid.replace("Pipeline-type",pipeline_name)
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
	if args.interactive:
		run_interative_jobs(current_pipeline,args)
		exit()

	
	if args.csv:
		df = pd.read_csv(args.input,header=None)
		fname = args.input.replace(".csv",".input")
		args.input = fname
		df.to_csv(fname,index=False,header=False,sep="\t")		
	submit_pipeline_jobs(current_pipeline,args)

	
if __name__ == "__main__":
	main()

























