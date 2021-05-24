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

	mainParser.add_argument('-f',"--bed_file",  help="bed file, first 3 columns should be chr, start, end",required=True)
	mainParser.add_argument("-m","--motif_file",  help="meme format motif file",required=True)		
	mainParser.add_argument("--random_bed",  help=argparse.SUPPRESS)		

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="BWA index file", default=myData['hg19_fasta'])
	genome.add_argument('--chrom_size',  help="chrom_size", default=myData['hg19_chrom_size'])

	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	args.genome_fasta = myData['%s_fasta'%(args.genome)]
	args.chrom_size = myData['%s_chrom_size'%(args.genome)]
	
	

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
	
	## random bed files
	toBed4(args.bed_file,"%s/bed_file"%(args.jid))
	random_bed = [str(uuid.uuid4()).split("-")[-1] for x in range(10)]
	args.random_bed = "%s/random_bed.list"%(args.jid)
	write_file(args.random_bed,"\n".join(random_bed))

	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























