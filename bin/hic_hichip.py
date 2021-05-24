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
	
	mainParser.add_argument('--hicpro',  help="only run hicpro", action='store_true')
	mainParser.add_argument('--hicpro_input',  help=argparse.SUPPRESS)
	mainParser.add_argument('--hicpro_config',  default=myData['hicpro_config'])
	mainParser.add_argument('--hichipper_config',  default=myData['hichipper_config'])
	mainParser.add_argument('--MAPS_config',  default=myData['MAPS_config'])
	mainParser.add_argument('-a','--anchor',  default="None", help="anchor list to search for interactions, if given, MAPS will be run as well")

	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-f',"--fastq_tsv",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Read 2 fastq, sample ID")
	group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')		

	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="bowtie2 index file", default=myData['hg19_bowtie2_index'])
	genome.add_argument('--bwa_index',  help="bwa index file", default=myData['hg19_BWA_index'])
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_main_chrom_size'])
	genome.add_argument('--genomic_feat_filepath',  help="MAPS genomic_feat_filepath", default=myData['hg19_genomic_feat_filepath'])
	genome.add_argument('-e','--digested_enzyme',  help="digested_fragments hg19_MboI", default="MboI")
	genome.add_argument('--chr_count',  help="chr_count", default=myPars['hg19_chr_count'])
	genome.add_argument('--digested_fragments',  help=argparse.SUPPRESS)
	
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def run_trimgalore(fq1,fq2,output_name):
	command_list = []
	command1 = "trim_galore --paired %s %s --basename %s -j 10 -q 10 --fastqc"%(fq1,fq2,output_name)
	command2 = "rm %s"%(fq1)
	command3 = "rm %s"%(fq2)
	command4 = "mv %s_R1_val_1.fq.gz %s"%(output_name,fq1)
	command5 = "mv %s_R2_val_2.fq.gz %s"%(output_name,fq2)
	command_list.append(command1)
	command_list.append(command2)
	command_list.append(command3)
	command_list.append(command4)
	command_list.append(command5)
	return "\n".join(command_list)
	

def make_hicpro_input(fastq_tsv,jid):
	
	
	df = pd.read_csv(fastq_tsv,sep="\t",header=None)
	for s,d in df.groupby(2):
		os.system("mkdir -p %s/%s"%(jid,s))
		os.system("mkdir -p %s/%s/fastq"%(jid,s))
		os.system("mkdir -p %s/%s/fastq/%s"%(jid,s,s))
		output_command = []
		trim_script_name = "%s/%s/fastq/%s/run_trim_galore.sh"%(jid,s,s)
		d.index = [str(i) for i in range(d.shape[0])]
		count = 1
		for i in d.index:
			os.system("ln -s %s %s/%s/fastq/%s/%s_rep%s_R1.fastq.gz"%(os.path.abspath(d.at[i,0]),jid,s,s,s,count))
			os.system("ln -s %s %s/%s/fastq/%s/%s_rep%s_R2.fastq.gz"%(os.path.abspath(d.at[i,1]),jid,s,s,s,count))
			## trimgalore script
			output_command.append(run_trimgalore("%s_rep%s_R1.fastq.gz"%(s,count),"%s_rep%s_R2.fastq.gz"%(s,count),"%s_rep%s"%(s,count)))
			count += 1
		write_file(trim_script_name,"\n".join(output_command))	
		dos2unix(trim_script_name)
def get_hicpro_config(args):
	content = "".join(open(args.hicpro_config).readlines())
	content = multireplace(content, vars(args))
	write_file("%s/hicpro.config.txt"%(args.jid),content)

def get_hichipper_config(args):
	content = "".join(open(args.hichipper_config).readlines())
	content = multireplace(content, vars(args))
	write_file("%s/hichipper.yaml"%(args.jid),content)
	
def get_MAPS_config(args):
	anchor_dir = os.path.abspath("/".join(args.anchor.split("/")[:-1]))
	args.anchor = anchor_dir+"/"+args.anchor.split("/")[-1]
	print ("anchor file abs path: %s"%(args.anchor))
	df = pd.read_csv(args.fastq_tsv,sep="\t",header=None)
	content = "".join(open(args.MAPS_config).readlines())
	for n in df[2].tolist():
		myDict = vars(args)
		myDict['unique_id'] = n+"_rep1"
		myDict['MAPS_fastq_dir']=os.path.abspath("%s/%s/fastq/%s"%(args.jid,n,n))
		myDict['MAPS_out_dir']=os.path.abspath("%s/%s"%(args.jid,n))
		outContent = multireplace(content, myDict)
		write_file("%s/%s/MAPS.sh"%(args.jid,n),outContent)
	
	
def main():

	args = my_args()
	args.digested_fragments = myData['%s_%s'%(args.genome,args.digested_enzyme)]
	args.index_file = myData['%s_bowtie2_index'%(args.genome)]
	args.index_file = "/".join(args.index_file.split("/")[:-1]) 
	args.bwa_index = myData['%s_BWA_index'%(args.genome)]
	args.chrom_size = myData['%s_main_chrom_size'%(args.genome)]
	args.genomic_feat_filepath = myData['%s_genomic_feat_filepath'%(args.genome)]
	args.chr_count = myPars['%s_chr_count'%(args.genome)]
	
	##------- guess input ------------------------------
	if args.guess_input:
		logging.info("preparing input files")
		## CHANGE THE FUNCTION HERE FOR DIFFERENT WRAPPER
		flag,fname = prepare_paired_end_input() 
		sys.exit(1)		
	
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
	make_hicpro_input(args.fastq_tsv,args.jid)
	args.hicpro_input = "%s.hicpro_input"%(args.jid)
	os.system("cut -f 3 %s > %s"%(args.fastq_tsv,args.hicpro_input))
	get_hicpro_config(args)
	if args.hicpro:
		submit_pipeline_jobs(myPipelines["hicpro"],args)
	else:
		get_hichipper_config(args)
		if args.anchor != "None":
			get_MAPS_config(args)
			submit_pipeline_jobs(myPipelines["hichip_MAPS"],args)
		else:
			submit_pipeline_jobs(myPipelines["hichip"],args)

	
if __name__ == "__main__":
	main()

























