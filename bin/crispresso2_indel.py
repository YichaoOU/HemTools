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

	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-f',"--input_list",  help="tsv 5 columns, R1.fastq, R2.fastq, amplicon_seq, gRNA_seq, output_name")
	mainParser.add_argument('-q',  help="read quality",default=0,type=int)
	mainParser.add_argument('-s',  help="base quality",default=0,type=int)
	mainParser.add_argument('--queue',  help="which queue to use",default='standard')
	group.add_argument("--gRNA_and_primers",  help="tsv 4 columns, unique ID that matches to fastq file name, gRNA seq, Forward Primer, Reverse Primer")		
	group.add_argument("--gRNA_and_primers_BWA",  help="tsv 4 columns, unique ID that matches to fastq file name, gRNA seq, Forward Primer, Reverse Primer")		

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="genome fasta file", default=myData['hg19_fasta'])
	genome.add_argument('--index_file',  help="BWA index file", default=myData['hg19_BWA_index'])

	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args



def prepare_input(args):
	try:
		df = pd.read_csv(args.gRNA_and_primers,sep="\t",header=None)
	except Exception as e:
		print (e)
		df = pd.read_csv(args.gRNA_and_primers_BWA,sep="\t",header=None)
	# print (df.head())
	out = []
	for r in df.iterrows():
		print (r[1][0])
		fq1 = glob.glob("*%s*R1*"%(r[1][0]))[0]
		fq2 = glob.glob("*%s*R2*"%(r[1][0]))[0]
		out.append([r[1][1],r[1][2],r[1][3],fq1,fq2,define_fastq_label(fq1)])
	args.input_list = args.jid+".input"
	pd.DataFrame(out).to_csv(args.input_list,sep="\t",header=False,index=False)

def main():

	args = my_args()
	args.genome_fasta = myData['%s_fasta'%(args.genome)]
	args.index_file = myData['%s_BWA_index'%(args.genome)]

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
	if args.input_list:
		pipeline_name = current_file_base_name
		submit_pipeline_jobs(myPipelines[pipeline_name],args)
	if args.gRNA_and_primers:
		prepare_input(args)
		pipeline_name = current_file_base_name+"_PCR"
		submit_pipeline_jobs(myPipelines[pipeline_name],args)		
	if args.gRNA_and_primers_BWA:
		prepare_input(args)
		pipeline_name = current_file_base_name+"_BWA_PCR"
		submit_pipeline_jobs(myPipelines[pipeline_name],args)		

	
if __name__ == "__main__":
	main()

























