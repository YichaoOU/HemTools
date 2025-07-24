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
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='Methyl_seq_'+username+"_"+str(datetime.date.today()))	

	mainParser.add_argument('-f',"--input",  help="fastq.tsv",required=True)
	mainParser.add_argument('-a',"--amplicon_seq",  help="amplicon_seq fasta file",required=True)
	mainParser.add_argument("--read_length",  help="read_length",type=int,required=True)
	mainParser.add_argument("--genomic_chr",  help="genomic_chr",type=str,required=True)
	mainParser.add_argument("--genomic_start",  help="genomic_start",type=int,required=True)
	mainParser.add_argument("--guide_seq",  help="distal HBG use AAATTAGTTAAAGGGAAGA",type=str,default="")
	mainParser.add_argument("--trim",  help="CTGTCTCTTATACACATCT",type=str,default="")
	
	mainParser.add_argument("--max_overlap",  help=argparse.SUPPRESS,type=int)
	mainParser.add_argument("--min_overlap",  help=argparse.SUPPRESS,type=int)
	mainParser.add_argument("--R1",  help="use R1",action='store_true')

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="BWA index file", default=myData['hg19_BWA_index'])
	genome.add_argument('-b','--black_list',  help="Blacklist file", default=myData['hg19_black_list'])
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])
	genome.add_argument('-e','--effectiveGenomeSize',  help="effectiveGenomeSize for bamCoverage", default=myPars['hg19_effectiveGenomeSize'])
	mainParser.add_argument('--interactive',  help="run pipeline interatively", action='store_true')

	# mainParser.add_argument('--softlinks',  help=argparse.SUPPRESS,default="")
	# mainParser.add_argument('--treatment_bam',  help=argparse.SUPPRESS)
	# mainParser.add_argument('--port',  help=argparse.SUPPRESS)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	# get fasta
	def read_fasta(f):
		my_dict = {}
		for r in SeqIO.parse(f, "fasta"):
			return str(r.seq).upper()
	fasta = read_fasta(args.amplicon_seq)
	args.amplicon_seq = fasta
	if args.guide_seq=="":
		args.guide_seq = fasta[20:-20]
	if args.trim!="": #not working as expected
		# args.trim = "--trim_sequences %s"%(args.trim)
		args.trim = '--trim_sequences --trimmomatic_options_string "ILLUMINACLIP:/hpcf/apps/trimmomatic/install/0.36/adapters/NexteraPE-PE.fa:0:90:10:0:true"'
	overlap_length = 2*args.read_length-len(fasta)
	args.max_overlap = overlap_length+10
	args.min_overlap = overlap_length-10
	
	
	
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
	if args.R1:
		# pipeline_name = pipeline_name+"_R1"
		current_pipeline = myPipelines[pipeline_name+"_R1"]
	else:
		current_pipeline = myPipelines[pipeline_name]
	submit_pipeline_jobs(current_pipeline,args)
	
	



	
	
	
	
	
	
	
	



if __name__ == "__main__":
	main()


















