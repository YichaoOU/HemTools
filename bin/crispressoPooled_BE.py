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


	mainParser.add_argument('-a','--amplicon_bed',  help="amplicon_bed required",required=True)
	mainParser.add_argument('-gRNA','--gRNA_bed',  help="gRNA_bed required",required=True)
	mainParser.add_argument('-f','--fastq_tsv',  help="gRNA_bed required",required=True)
	mainParser.add_argument('--ref',  help="reference base",default="A",type=str)
	mainParser.add_argument('--alt',  help="alternative base",default="G",type=str)
	mainParser.add_argument('--cas9',  help="not running in base editor mode",action='store_true')
	mainParser.add_argument('--SNP',  help="3-col tsv file, gRNA seq, position, SNP",default="",type=str)
	mainParser.add_argument('--addon_parameters',  help="additional paramteeres, such as --min_paired_end_reads_overlap for crispresso",default="",type=str)
	# mainParser.add_argument("--info_tsv", help=argparse.SUPPRESS)
	mainParser.add_argument("--input_list", help=argparse.SUPPRESS)
	mainParser.add_argument('--queue',  help="which queue to use",default='standard')

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="genome fasta file", default=myData['hg19_fasta'])

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def prepare_input(amp_bed,gRNA_bed,fasta,jid):
	df = pd.read_csv(amp_bed,sep="\t",header=None,comment="#")
	df2 = pd.read_csv(gRNA_bed,sep="\t",header=None,comment="#")

	# get gRNA sequence
	out_fa = "gRNA.fa"
	command = "module load  bedtools/2.25.0;bedtools getfasta -fi {0} -bed {1} -fo {2} -s -name -tab".format(fasta,gRNA_bed,out_fa)
	os.system(command)
	# exit()
	df3 = pd.read_csv(out_fa,sep="\t",header=None,index_col=0)
	df3.index = [x.split("::")[0] for x in df3.index]
	# print (df3.head())
	os.system("rm %s"%(out_fa))
	df2.index = df2[3].tolist()

	df[5] = df[3].map(df2[5].to_dict())# key step to make sure amplicon is the same strand as gRNA
	# print (df)
	is_NaN = df.isnull()
	row_has_NaN = is_NaN.any(axis=1)
	rows_with_NaN = df[row_has_NaN]
	if rows_with_NaN.shape[0]>0:
		print ("The following Amplicon id are removed")
		print ("\n".join(rows_with_NaN[3].tolist()))
	df = df.dropna()
	out_bed = str(uuid.uuid4()).split("-")[-1]
	
	df.to_csv("%s.bed"%(out_bed),sep="\t",header=False,index=False)
	
	# get gRNA sequence
	out_fa = "%s.fa"%(out_bed)
	command = "module load  bedtools/2.25.0;bedtools getfasta -fi {0} -bed {1}.bed -fo {1}.fa -s -name -tab".format(fasta,out_bed,out_bed)
	os.system(command)
	
	df4 = pd.read_csv(out_fa,sep="\t",index_col=0,header=None)
	df4.index = [x.split("::")[0] for x in df4.index]
	df4[2] = df3[1]
	df4[1] = df4[1].str.upper()
	df4[2] = df4[2].str.upper()
	# df4[3] = "NA"
	# df4[4] = "NA"
	# print (df4.head())
	# exit()
	df4.to_csv("%s_info.tsv"%(jid),sep="\t",header=False)
	os.system("rm %s"%(out_fa))
	os.system("rm %s.bed"%(out_bed))
	


def main():

	args = my_args()
	args.genome_fasta = myData['%s_fasta'%(args.genome)]

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
	df = pd.read_csv(args.fastq_tsv,sep="\t",header=None)
	df=df[[0,1,2]]
	df[3] = "%s_info.tsv"%(args.jid)
	df.to_csv("%s.input"%(args.jid),sep="\t",header=False,index=False)
	args.input_list = "%s.input"%(args.jid)
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	if args.SNP != "":
		os.system("cp %s %s/"%(args.SNP,args.jid))	
	prepare_input(args.amplicon_bed,args.gRNA_bed,args.genome_fasta,args.jid)	
	# exit()
	if args.cas9:
		submit_pipeline_jobs(myPipelines["crispressoPooled_cas9"],args)
		exit()
	submit_pipeline_jobs(myPipelines["crispressoPooled_BE"],args)


	
if __name__ == "__main__":
	main()

























