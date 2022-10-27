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

TODO, overwrite genome index
"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	

	mainParser.add_argument('-f',"--fastq_tsv",  help="TSV file, 4 columns, read 1, read 2, UID, group ID",required=True)
	mainParser.add_argument('-d',"--design_matrix",  help="TSV file, 3 columns, group ID, group ID, output_prefix",required=True)
	mainParser.add_argument("--strandness",  help="fr: first read forward or rf: first read reverse",default=None)

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10", default='hg19',type=str)
	genome.add_argument('--nfcore_genome',  help="genome version: hg19, hg38, mm9, mm10", default='hg38',type=str)
	genome.add_argument('-i','--index_file',  help="Kallisto index file", default=myData['hg19_kallisto_index'])
	genome.add_argument('--gene_info',  help="gene info t2g file for sleuth", default=myData['hg19_t2g'])

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def to_nfcore_sample_csv(fastq_tsv,strandness,jid):
	df = pd.read_csv(fastq_tsv,sep="\t",header=None)
	df['sample'] = df[2]
	df['fastq_1'] = df[0]
	df['fastq_2'] = df[1]
	if strandness == "fr":
		strand = "forward"
	elif strandness == "rf":
		strand = "reverse"
	else:
		strand = "unstranded"
	df['strandedness'] = strand
	df[['sample','fastq_1','fastq_2','strandedness']].to_csv("%s.sample.csv"%(jid),index=False)

def reformat_design_tsv(fastq_tsv,design_tsv):
	df = pd.read_csv(fastq_tsv,sep="\t",header=None)
	df2 = pd.read_csv(design_tsv,sep="\t",header=None)
	# print (df)
	# print (df2)
	out = []
	for i,r in df2.iterrows():
		g1 = r[0]
		g2 = r[1]
		name = r[2]
		# print (df[df[3]==g1][2])
		g1_samples = df[df[3]==g1][2].tolist()
		g2_samples = df[df[3]==g2][2].tolist()
		col4 = ",".join(g1_samples+g2_samples)
		col5 = "-x %s -y %s"%(g1_samples[0],g1_samples[1])
		col6 = "-x %s -y %s"%(g2_samples[0],g2_samples[1])
		out.append([g1,g2,name,col4,col5,col6])
	df = pd.DataFrame(out)
	df.to_csv(design_tsv,sep="\t",header=False,index=False)

def main():

	args = my_args()
	if args.strandness == "fr":
		args.strandness = "--fr-stranded"
	elif args.strandness == "rf":
		args.strandness = "--rf-stranded"
	
	else:
		args.strandness = ""

		
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			
	
	##------- add functions below ----------------------
	#------------- check input ----------------------
	if not isfile(args.fastq_tsv):
		logging.error ("%s not found"%args.fastq_tsv)
		sys.exit(1)
	if not isfile(args.design_matrix):
		logging.error ("%s not found"%args.design_matrix)
		sys.exit(1)
	#-------------- run jobs ----------------------
	to_nfcore_sample_csv(args.fastq_tsv,args.strandness,args.jid)
	if not args.genome == "custom":
		args.index_file = myData['%s_kallisto_index'%(args.genome)]
		args.gene_info = myData['%s_t2g'%(args.genome)]
		# args.nfcore_genome = args.genome
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	reformat_design_tsv(args.fastq_tsv,args.design_matrix)
	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























