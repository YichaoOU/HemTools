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

	SE = mainParser.add_mutually_exclusive_group(required=False)
	SE.add_argument('-r1',help="only use R1 read for analysis",action='store_true')
	SE.add_argument('-r2',help="only use R2 read for analysis",action='store_true')


	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-f',"--input_list",  help="tsv 5 columns, R1.fastq, R2.fastq, amplicon_seq, gRNA_seq, output_name")
	mainParser.add_argument('-q',  help="read quality",default=0,type=int)
	mainParser.add_argument('--tsv',  help="not for end user",default="")
	mainParser.add_argument('-s',  help="base quality",default=0,type=int)
	mainParser.add_argument('--custom_mutation',  help="quantify freq for a specific mutation",default=None,type=str)
	mainParser.add_argument('-a',  help="Amplicon sequence",default=None,type=str)
	mainParser.add_argument('-gRNA',  help="gRNA",default=None,type=str)
	mainParser.add_argument('-m', '--min_overlap', help="min_overlap for read merging",default=10,type=int)
	mainParser.add_argument('--ref',  help="reference base",default="A",type=str)
	mainParser.add_argument('--alt',  help="alternative base",default="G",type=str)
	mainParser.add_argument('--base_editor_commands',  help="alternative base",default="--quantification_window_size 10 --quantification_window_center -10 --base_editor_output --keep_intermediate --dump",type=str)
	mainParser.add_argument('--cas9',  help="not running in base editor mode",action='store_true')
	# mainParser.add_argument('--SNP',  help="3-col tsv file, gRNA seq, position, SNP",default="",type=str)
	mainParser.add_argument('--queue',  help="which queue to use",default='standard')
	mainParser.add_argument('--interactive',  help="run pipeline interatively", action='store_true')

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
		out.append([r[1][1],r[1][2],r[1][3],fq1,fq2,define_fastq_label(fq1)+"_"+r[1][1]])
	args.input_list = args.jid+".input"
	pd.DataFrame(out).to_csv(args.input_list,sep="\t",header=False,index=False)

def add_gRNA_amp_seq(jid,file,gRNA,amplicon_seq):
	df = pd.read_csv(file,sep="\t",header=None)
	sample_name_col = df.columns[-1]
	other_cols = df.columns[:-1].tolist()
	df['gRNA'] = gRNA
	df['amplicon_seq'] = amplicon_seq
	out_file = jid+".gRNA.Amp.tsv"
	print (other_cols)
	print (['amplicon_seq','gRNA',sample_name_col])
	df[other_cols+['amplicon_seq','gRNA',sample_name_col]].to_csv(out_file,index=False,header=False,sep="\t")
	return out_file

def main():

	args = my_args()
	args.genome_fasta = myData['%s_fasta'%(args.genome)]
	args.index_file = myData['%s_BWA_index'%(args.genome)]
	
	if args.cas9:
		args.base_editor_commands = "--keep_intermediate --dump"
	if args.r1:
		args.jid = args.jid + "_R1_only"
	if args.r2:
		args.jid = args.jid + "_R2_only"
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
		if args.a and args.gRNA:
			args.input_list = add_gRNA_amp_seq(args.jid,args.input_list,args.gRNA,args.a)
	if args.gRNA_and_primers:
		prepare_input(args)
		pipeline_name = current_file_base_name+"_PCR"
		# submit_pipeline_jobs(myPipelines[pipeline_name],args)		
	if args.gRNA_and_primers_BWA:
		prepare_input(args)
		pipeline_name = current_file_base_name+"_BWA_PCR"
		# submit_pipeline_jobs(myPipelines[pipeline_name],args)		
	if args.r1:
		pipeline_name += "_R1"
	if args.r2:
		pipeline_name += "_R2"
	args.tsv = args.input_list
	if args.custom_mutation:
		args.custom_mutation = os.path.abspath(args.custom_mutation)
		args.custom_mutation = "module load python/3.7.0;crispresso_custom_edit_freq.py %s"%(args.custom_mutation)
		# pipeline_name = current_file_base_name +"_custom_mutation"
	if args.interactive:
		run_interative_jobs(myPipelines[pipeline_name],args)
		exit()

	submit_pipeline_jobs(myPipelines[pipeline_name],args)
	
if __name__ == "__main__":
	main()

























