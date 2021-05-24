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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="perform chromatin state discovery using chromHMM v1.18, bin size is fixed to be 200bp.")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('--pipeline_type',  help="Not for end-user.", default=current_file_base_name)
	
	input=mainParser.add_argument_group(title='Input Files')

	input.add_argument('-se',"--SE_fastq_list",  help="A tsv file containing 2 columns, R1.fastq.gz & UID")
	input.add_argument('-tf',"--TF_fastq_list",  help="A tsv file containing 2 columns, R1.fastq.gz & UID")
	input.add_argument('-his',"--His_fastq_list",  help="A tsv file containing 2 columns, R1.fastq.gz & UID")
	input.add_argument('-d_tf',"--design_matrix_TF",  help="Similar to peakcall.tsv, this is a tsv file containing 3 columns: treatment_UID & control_UID & label. Label has to be meaningful labels, such as H3K4me3. Case insensitive.")
	input.add_argument('-d_his',"--design_matrix_His",  help="Similar to peakcall.tsv, this is a tsv file containing 3 columns: treatment_UID & control_UID & label. Label has to be meaningful labels, such as H3K4me3. Case insensitive.")
	input.add_argument('-d1',"--design_matrix_1",  help="Similar to peakcall.tsv, this is a tsv file containing 3 columns: treatment_UID & control_UID & label. Label has to be meaningful labels, such as H3K4me3. Case insensitive.")
	input.add_argument('-d2',"--design_matrix_2",  help="A tsv file contatinig 2 columns: UID & label. ")
	input.add_argument("--LearnModel_addon",  help="chromHMM learmodel additional parameters e.g. -u coord dir",default="")
	input.add_argument('-pe',"--PE_fastq_list",  help="A tsv file containing 3 columns, R1.fastq.gz & R2.fastq.gz & UID")
	input.add_argument('-c',"--cell_line",  help="input cell line, just a name, not important",default="myCellLine")
	input.add_argument("--from_binBam",  help="Resume analysis from chromHMM binBam step", action='store_true')
	input.add_argument('-m',"--memory",  help="memory requested (MB), if you have 16+ samples, for example, 8 markers and 2 replicates per marker, use 200G, which is -m 200000",default=200000)
	input.add_argument('-bin',"--chromHMM_jar",  help="chromHMM bin location",default=myPars['chromHMM_jar'])
	input.add_argument("--known_association",  help="chromHMM bin location",default=myData['known_association'])
	input.add_argument("--chromatin_state_info",  help="chromHMM bin location",default=myData['chromatin_state_info'])
	input.add_argument('-n',"--number_states",  help="Number of chromHMM states to learn. Remember, chromHMM uses binarized signals. If you have N markers, then possibly you could explain up to 2^N states. In practice, you should run this program several times, each with different number of states.",default=10)
	input.add_argument("--d1_bin_bam_addon",  help="This is an addon parameter for binarized bam with design_matrix_1 as input",default="")
	input.add_argument("--d2_bin_bam_addon",  help="This is an addon parameter for binarized bam with design_matrix_2 as input",default="")
	input.add_argument("--adjust_TF_pvalue",  help="Most TFs, except for CTCF, tend to have much lower number of 1s",default=0.0005,type=float)
	input.add_argument("--adjust_histone_pvalue",  help="Some histone marks can have much higher number of 1s after binarizeBam, increase the p-value cutoff can descrease the number of 1s",default=0.00001,type=float)
	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-i','--index_file',  help="BWA index file", default=myData['hg19_BWA_index'])
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])
	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	if args.from_binBam:
		return args
	if not (args.SE_fastq_list or args.PE_fastq_list):
		mainParser.error('No input fastq files')	
	if not (args.design_matrix_1 or args.design_matrix_2):
		mainParser.error('No design matrix input')	
	
	return args
	
def to_design_matrix(args):
	if args.design_matrix_1:
		logging.info("parsing %s"%(args.design_matrix_1))
		df = pd.read_csv(args.design_matrix_1,sep="\t",header=None,dtype=str)
		df['cell'] = args.cell_line
		df[0] = df[0].apply(lambda x:x+".bam")
		df[1] = df[1].apply(lambda x:x+".bam")
		df[['cell',2,0,1]].to_csv("%s/design_matrix_1"%(args.jid),index=False,header=None,sep="\t")
	if args.design_matrix_2:
		logging.info("parsing %s"%(args.design_matrix_2))
		df = pd.read_csv(args.design_matrix_2,sep="\t",header=None,dtype=str)
		df['cell'] = args.cell_line
		df[0] = df[0].apply(lambda x:x+".bam")
		df[['cell',1,0]].to_csv("%s/design_matrix_2"%(args.jid),index=False,header=None,sep="\t")
	if args.design_matrix_TF:
		logging.info("parsing %s"%(args.design_matrix_TF))
		df = pd.read_csv(args.design_matrix_TF,sep="\t",header=None,dtype=str)
		df['cell'] = args.cell_line
		df[0] = df[0].apply(lambda x:x+".bam")
		df[1] = df[1].apply(lambda x:x+".bam")
		df[['cell',2,0,1]].to_csv("%s/design_matrix_TF"%(args.jid),index=False,header=None,sep="\t")
	if args.design_matrix_His:
		logging.info("parsing %s"%(args.design_matrix_His))
		df = pd.read_csv(args.design_matrix_His,sep="\t",header=None,dtype=str)
		df['cell'] = args.cell_line
		df[0] = df[0].apply(lambda x:x+".bam")
		df[1] = df[1].apply(lambda x:x+".bam")
		df[['cell',2,0,1]].to_csv("%s/design_matrix_His"%(args.jid),index=False,header=None,sep="\t")

def main():

	args = my_args()
	args.index_file = myData['%s_BWA_index'%(args.genome)]
	args.chrom_size = myData['%s_chrom_size'%(args.genome)]	
	if args.from_binBam:
		logging.info ("The job id is: "+args.jid)	
		logging.info ("Resuming analysis from binBam...")	
		pipeline_name = current_file_base_name+"_from_binBam"
		submit_pipeline_jobs(myPipelines[pipeline_name],args)
		exit()
			

		
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)	

	##------- check inputs exist  ----------------------
	logging.info("checking input files...")
	input_error = False
	if args.SE_fastq_list:
		logging.info("parsing %s"%(args.SE_fastq_list))
		dos2unix(args.SE_fastq_list)
		with open(args.SE_fastq_list) as f:
			for line in f:
				if len(line) < 2:
					continue
				line = line.strip().split()
				if not isfile(line[0]):
					logging.error("%s not found"%(line[0]))
					input_error=True
	if args.PE_fastq_list:
		logging.info("parsing %s"%(args.PE_fastq_list))
		dos2unix(args.PE_fastq_list)
		with open(args.PE_fastq_list) as f:
			for line in f:
				if len(line) < 2:
					continue			
				line = line.strip().split()
				if not isfile(line[0]):
					logging.error("%s not found"%(line[0]))
					input_error=True
				if not isfile(line[1]):
					logging.error("%s not found"%(line[1]))
					input_error=True

	if input_error:
		logging.error("Please check your input. See above message.")
		logging.error("Program exiting...")
		sys.exit(1)
	else:
		logging.info("All input files are found. Submitting jobs...")
				
			

	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	
	## additional commands
	to_design_matrix(args)
	

	pipeline_name = current_file_base_name
	# submit_pipeline_jobs(myPipelines[pipeline_name],args)
	submit_pipeline_jobs(myPipelines["chromHMM_TF"],args)
	
if __name__ == "__main__":
	main()







































