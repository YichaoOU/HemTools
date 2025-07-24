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
	group.add_argument('-u',"--user_lsf",  help="user defined lsf file")
	
	# mainParser.add_argument("--single",  help="Let the program generate the input files for you.",action='store_true')
	mainParser.add_argument('-f',"--input",  help="tab delimited any number of columns (tsv file), the last column is output prefix. For example, a paired-end fastq input could be: Read 1 fastq, Read 2 fastq, sample ID")
	mainParser.add_argument('-q',"--queue",  help="submit queue",default="standard")
	mainParser.add_argument('-d',"--design_tsv",  help="for pairwise comparison, eg, diff analysis",default="")
	mainParser.add_argument('-m',"--memory",  help="request memory",default=20000, type=int)
	# mainParser.add_argument("--ncores",  help="request CPU",default=2, type=int)
	mainParser.add_argument("--FLASH_min_overlap",  help="FLASH_min_overlap",default=10, type=int)
	mainParser.add_argument("--username",  help="username",default=username)
	mainParser.add_argument("--addon_parameters",  help="addon_parameters any pipeline",default="")


	mainParser.add_argument('-f2',"--input2",  help="for jobs with dependencies. tab delimited any number of columns (tsv file), the last column is output prefix. For example, a paired-end fastq input could be: Read 1 fastq, Read 2 fastq, sample ID")
	
	
	mainParser.add_argument("--single",  help="default is paired-end data, specify this parameter if you have single-end data",action='store_true')		
	mainParser.add_argument("--general",  help="general file list generator",action='store_true')		
	mainParser.add_argument("--csv",  help="convert tsv to csv when doing guess_input",action='store_true')		
	mainParser.add_argument("--email",  help="send user the fastq.tsv file",action='store_true')		
	mainParser.add_argument("--override_jid",  help="continue working on the same jid folder",action='store_true')		

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="BWA index file", default=myData['hg19_BWA_index'])
	genome.add_argument('--BSgenome',  help="R BS genome 2bit file", default=myData['hg38_BSgenome'])
	genome.add_argument('--repBase_index',  help="repBase_index", default=myData['hg38_repBase_index'])
	genome.add_argument('--main_chrom_size',  help="main_chrom_size", default=myData['hg38_main_chrom_size'])
	genome.add_argument('--main_genome_fasta',  help="main_genome_fasta", default=myData['hg38_main_genome_fasta'])
	genome.add_argument('--bowtie2_index',  help="bowtie2_index", default=myData['hg19_bowtie2_index'])
	genome.add_argument('--faidx',  help="fasta index", default=myData['mm9_faidx'])
	genome.add_argument('--chromap_index',  help="fasta index", default=myData['mm9_faidx'])
	genome.add_argument('--fasta',  help="fasta ", default=myData['mm9_fasta'])
	genome.add_argument('--STAR_index',  help="STAR_index ", default=myData['hg19_STAR_index'])
	genome.add_argument('--excl',  help="excl ", default=myData['hg38_excl'])
	genome.add_argument('--delly_map',  help="delly map ", default=myData['hg19_delly_map'])
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

def get_value(Dict,myKey):
	try:
		return Dict[myKey]
	except:
		return ""

def general_file_list(file_pattern,replace_name):
	files = glob.glob("*%s"%(file_pattern))
	names = [f.replace(replace_name,"") for f in files]
	df = pd.DataFrame()
	df[0] = files
	df[1] = names
	df.to_csv("input.tsv",sep="\t",header=False,index=False)


def main():

	args = my_args()
	if args.list_pipelines:
		print ("All available pipelines are shown below:")
		available_pipes = list(set([x.lower() for x in myPipelines]))
		for k in available_pipes:
			print (k)
		print ("----------------------------------------")
		sys.exit(1)	
	if not args.genome == "custom":
		# try:
			# args.index_file = myData['%s_BWA_index'%(args.genome)]
			# args.fasta = myData['%s_fasta'%(args.genome)]	
			# args.faidx = myData['%s_faidx'%(args.genome)]	
			# args.excl = myData['%s_excl'%(args.genome)]	
		# except:
			# pass
		# args.chrom_size = myData['%s_chrom_size'%(args.genome)]	
		
		args.chromap_index = get_value(myData,'%s_chromap_index'%(args.genome))
		args.fasta = get_value(myData,'%s_fasta'%(args.genome))
		args.STAR_index = get_value(myData,'%s_STAR_index'%(args.genome))
		args.faidx = get_value(myData,'%s_faidx'%(args.genome))
		args.excl = get_value(myData,'%s_excl'%(args.genome))
		args.chrom_size = get_value(myData,'%s_chrom_size'%(args.genome))
		args.main_chrom_size = get_value(myData,'%s_main_chrom_size'%(args.genome))
		args.main_genome_fasta = get_value(myData,'%s_main_genome_fasta'%(args.genome))
		args.index_file = get_value(myData,'%s_BWA_index'%(args.genome))
		args.black_list = get_value(myData,'%s_black_list'%(args.genome))
		args.bowtie2_index = get_value(myData,'%s_bowtie2_index'%(args.genome))
		# args.black_list = myData['%s_black_list'%(args.genome)]	
		# args.effectiveGenomeSize = myData['%s_effectiveGenomeSize'%(args.genome)]	
	##------- guess input ------------------------------
	if args.guess_input:
		logging.info("preparing input files")
		# run_lsf.py --guess_input --general --file_pattern bam --replace_name ".markdup.bam"
		if args.general:
			general_file_list(args.file_pattern,args.replace_name)
			sys.exit(1)
		if args.single:
			flag,fname = prepare_single_end_input() 
		else:
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
	if isdir(args.jid) and not args.override_jid:
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			

	#-------------- run jobs ----------------------
	
	os.system("mkdir -p %s"%(args.jid))
	os.system("mkdir -p %s/log_files"%(args.jid))
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

























