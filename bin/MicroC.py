#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
file_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
# print (file_dir)

pipeline_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='MicroC_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--fastq_tsv",  help="4 columns: R1, R2, label, bait.bed")
	mainParser.add_argument('-q',"--queue",  help="submit queue",default="standard")
	mainParser.add_argument('-m',"--memory",  help="request memory",default=100000, type=int)
	mainParser.add_argument("--FLASH_min_overlap",  help="FLASH_min_overlap",default=10, type=int)
	mainParser.add_argument("--FLASH_max_overlap",  help="FLASH_max_overlap",default=100, type=int)
	mainParser.add_argument("--username",  help="username",default=username)

	mainParser.add_argument("--src",  help="src of MicroC program",default="/home/yli11/Programs/Micro-Capture-C", type=str)



	
	
	# mainParser.add_argument("--single",  help="default is paired-end data, specify this parameter if you have single-end data",action='store_true')		
	# mainParser.add_argument("--csv",  help="convert tsv to csv when doing guess_input",action='store_true')		
	# mainParser.add_argument("--email",  help="send user the fastq.tsv file",action='store_true')		
	# mainParser.add_argument("--override_jid",  help="continue working on the same jid folder",action='store_true')		

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)


	genome.add_argument('--bowtie2_index',  help="fasta index", default=myData['hg19_bowtie2_index'])
	genome.add_argument('--genome_fasta',  help="fasta ", default=myData['hg19_fasta'])


	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])

	mainParser.add_argument('--interactive',  help="run pipeline interatively", action='store_true')

	##------- add parameters above ---------------------
	# args = mainParser.parse_args()	
	args,unknown = mainParser.parse_known_args()
	for i in range(0,len(unknown),2):
		mainParser.add_argument(unknown[i],default=unknown[i+1])
	args = mainParser.parse_args()
	return args


def main():
	# print (myPipelines)
	args = my_args()

	
	# print (args)
	if args.genome != "custom":
		args.chrom_size = myData['%s_chrom_size'%(args.genome)]
		if args.bowtie2_index == myData['hg19_bowtie2_index']:
			args.bowtie2_index = myData['%s_bowtie2_index'%(args.genome)]
		args.genome_fasta = myData['%s_fasta'%(args.genome)]
		# args.chrom_size = myData['%s_chrom_size'%(args.genome)]
	print (args)
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
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
		run_interative_jobs(pipeline_name,args)
		exit()
	# pipeline_name="MicroC_multi_bait"
	current_pipeline = myPipelines[pipeline_name]
	# print (current_pipeline)
	# exit()
	submit_pipeline_jobs(current_pipeline,args)

	
if __name__ == "__main__":
	main()

























