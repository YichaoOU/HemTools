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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="analysis of crispr gRNA deep sequencing data")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('--interative',  help="run pipeline interatively", action='store_true')
	mainParser.add_argument('-d',"--design_matrix",  help="(Required) tsv 3 columns: group 1 , group 2, comparison name. The second group is used as control.",required=False)
	mainParser.add_argument("-l","--gRNA_library", help="(Required) 3 columns csv, with header: id,seq,gene", required=False)
	mainParser.add_argument("-c","--control_gRNA_group", help="(Required) mageck format", required=False)
	mainParser.add_argument("--min_read_count", help="filter sgRNAs using read count, sgRNAs with less than the given value will be filtered out", default=10,type=int)
	mainParser.add_argument("-b",'--bed',  help="Genomic coordinates for gRNAs (Format: chr, start, end, name). If provided, raw counts, logFC, logFDR will be uploaded to protein paint for visualization.",default=None)
	mainParser.add_argument('--add_on_parameters',  help="",default="")
	mainParser.add_argument('--trim_5',  help="fix gRNA position to count",default=None)
	
	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-f',"--fastq_tsv",  help="tab delimited 3 columns (tsv file): Read 1 fastq, Sample ID, group ID")
	group.add_argument("--guess_input",  help="Let the program generate the fastq.tsv and design.tsv files for you.",action='store_true')			
	
	mainParser.add_argument("--fastq_files", help=argparse.SUPPRESS)
	mainParser.add_argument("--sample_ids", help=argparse.SUPPRESS)
	mainParser.add_argument("--bdg_to_bw_files", help=argparse.SUPPRESS)

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	# genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	# args.chrom_size = myData['%s_chrom_size'%(args.genome)]
	if args.guess_input:
		flag,fname = prepare_single_end_input_with_group_infer()
		sys.exit(1)	
	if args.trim_5:
		args.add_on_parameters += " --trim-5 %s"%(args.trim_5)
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			
		

	#-------------- run jobs ----------------------
	fq = pd.read_csv(args.fastq_tsv,sep="\t",header=None)
	args.fastq_files = " ".join(fq[0].tolist())
	args.sample_ids = ",".join(fq[1].tolist())
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	if args.interative:
		run_interative_jobs(myPipelines[pipeline_name],args)
	else:
		submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()







































