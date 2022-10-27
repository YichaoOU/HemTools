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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="RGT_HINT atac-seq footprint with bias correction")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f','--fastq_tsv',  help="3-col tsv, R1, R2, sample_ID", required=True)
	mainParser.add_argument('-p','--peak_bed',  help="narrowpeak file", required=True)
	mainParser.add_argument('-IntType',  help="#Interaction type - 1: peak to peak (CTCF) 2: peak to non peak 3: peak to all (default, h3k27ac) 4: all to all 5: everything from 1 to 4.", default=3)
	mainParser.add_argument('-BINSIZE',  help="# Size of the bins, in bases, for detecting the interactions.", default=2500)
	mainParser.add_argument('-mapq_cutoff',  help="mapq_cutoff", default=0)
	mainParser.add_argument('-LowDistThr',  help="Lower distance threshold of interaction between two segments", default=10000)
	mainParser.add_argument('-UppDistThr',  help="Upper distance threshold of interaction between two segments", default=2000000)
	mainParser.add_argument('-UseP2PBackgrnd',  help="# Applicable only for peak to all output interactions - values: 0 / 1 \n# if 1, uses only peak to peak loops for background modeling - corresponds to FitHiChIP(S) \n# if 0, uses both peak to peak and peak to nonpeak loops for background modeling - corresponds to FitHiChIP(L)", default=0)
	mainParser.add_argument('-BiasType',  help="# parameter signifying the type of bias vector - values: 1 / 2 # 1: coverage bias regression 2: ICE bias regression", default=1)
	mainParser.add_argument('-MergeInt',  help="# following parameter, if 1, means that merge filtering (corresponding to either FitHiChIP(L+M) or FitHiChIP(S+M))\n# depending on the background model, would be employed. Otherwise (if 0), no merge filtering is employed. ", default=1)
	mainParser.add_argument('-QVALUE',  help="FDR (q-value) threshold for loop significance", default=0.05)
	# args.softlinks = "rm /home/%s/rgtdata"%(username)
	mainParser.add_argument('--username',  help=argparse.SUPPRESS,default=username)
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('--bwa_index',  help="bwa index file", default=myData['hg19_BWA_index'])
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	args.bwa_index = myData['%s_BWA_index'%(args.genome)]
	args.chrom_size = myData['%s_chrom_size'%(args.genome)]
	args.peak_bed = os.path.abspath(args.peak_bed)
		
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)		


	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = "hichip_mnase"
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

		
if __name__ == "__main__":
	main()







































