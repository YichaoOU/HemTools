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
	mainParser.add_argument('-f',"--bam_list",  help="tsv 2 columns, output_filename & input bam file(s). Note that multiple bam files can be merged, if multiple files are given, they should be separated by space",required=True)

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update chrom size.", default='hg19',type=str)
	genome.add_argument('-s','--genome_chrom_size',  help="chrome size", default=myData['hg19_homer_chrom_size'])
	genome.add_argument('--skip_chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])
	genome.add_argument('--chrom_size_bed',  help="for homer chrom error, not for end-user. chrome size bed file to filter out out-coordinate regions", default=myData['hg19_chrom_size_bed'])
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def find_other_chr(f):
    df = pd.read_csv(f,sep="\t",header=None)
    df = df[df[0].str.contains("_")]
    out = df[0].tolist()+['chrM']
    # print (out)
    return " ".join(out)

def main():

	args = my_args()
	if args.genome=="custom":
		args.genome_chrom_size = myData['%s_homer_chrom_size'%(args.genome)]
		args.skip_chrom_size = "chrM"
		args.chrom_size_bed = myData['%s_chrom_size_bed'%(args.genome)]
		args.genome = myData['%s_fasta'%(args.genome)]
	else:
		args.genome_chrom_size = myData['%s_homer_chrom_size'%(args.genome)]
		args.skip_chrom_size = myData['%s_chrom_size'%(args.genome)]
		args.skip_chrom_size = find_other_chr(args.skip_chrom_size)
		args.chrom_size_bed = myData['%s_chrom_size_bed'%(args.genome)]
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
	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























