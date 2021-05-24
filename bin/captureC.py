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
	group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')			
	group.add_argument('-f',"--fastq_tsv",  help="3 columns")
	mainParser.add_argument('-t',"--target",  help="9 columns")
	mainParser.add_argument('-c',"--cut_site",  help=argparse.SUPPRESS)
	mainParser.add_argument('-l',"--exclusion_length",  help="exclusion_length",default=1000,type=int)
	
	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="BWA index file", default=myData['hg19_bowtie_CapC_index'])
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])
	# genome.add_argument('-d','--dpnII_coordinates',  help="Blacklist file", default=myData['hg19_dpnII_coordinates'])
	genome.add_argument('-fa','--genome_fa',  help="Blacklist file", default=myData['hg19_fasta'])
	genome.add_argument('-e','--digested_enzyme',  help="digested_fragments hg19_MboI", default="MboI")
	genome.add_argument('--digested_fragments',  help=argparse.SUPPRESS)
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

enzyme_cut = {}
enzyme_cut['MboI'] = "GATC"
enzyme_cut['DpnI'] = "GATC"
enzyme_cut['DpnII'] = "GATC"
enzyme_cut['NlaIII'] = "CATG"

def preprocess_target_bed(user_t,digestion_bed,jid,exclusion_length):
	output = "%s/%s.target.bed"%(jid,jid)
	command = "module load bedtools;bedtools intersect -a %s -b %s -u > %s"%(digestion_bed,user_t,output)
	os.system(command)
	df = pd.read_csv(output,sep="\t",header=None)
	df['name'] = ["C%s"%(x) for x in df.index]
	df['chr'] = [x.replace("chr","") for x in df[0]]
	df['e_start'] = df[1]-1000
	df['e_end'] = df[2]+1000
	df['flag'] = 1
	df['SNP']="A"
	df[['name','chr',1,2,'chr','e_start','e_end','flag','SNP']].to_csv(output,sep="\t",header=False,index=False)
	return os.path.abspath(output)
# args.target_bed = preprocess_target_bed(args.target_bed,args.digested_fragments,args.sample_id)
def main():

	args = my_args()
	args.digested_fragments = myData['%s_%s'%(args.genome,args.digested_enzyme)]
	args.cut_site = enzyme_cut[args.digested_enzyme]
	args.chrom_size = myData['%s_chrom_size'%(args.genome)]
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
	args.target = preprocess_target_bed(args.target,args.digested_fragments,args.jid,args.exclusion_length)
	logging.info("Using %s"%(args.target))
	pipeline_name = current_file_base_name.lower()
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























