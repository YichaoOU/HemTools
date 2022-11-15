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

	mainParser.add_argument('-f',"--bam_tsv",  help="TSV file, 3 columns, bam file, sample name, group name",required=True)
	mainParser.add_argument('-d',"--design_matrix",  help="TSV file, 3 columns, group ID, group ID, output_prefix",required=True)
	mainParser.add_argument("--cores",  help="Number of CPUs",default=10,type=int)
	mainParser.add_argument("--src",  help="DEX src",default="/home/yli11/Programs/DEXSeq/inst/python_scripts",type=str)
	mainParser.add_argument("--count_cutoff",  help="filter exons by sum read count, more samples should increase this cutoff",default=10,type=int)
	mainParser.add_argument("--design_tsv",  help=argparse.SUPPRESS)


	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10", default='hg19',type=str)
	genome.add_argument('-gff',  help="DEXseq gff file", default=myData['hg19_DEXseq_gff'])

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def make_design_tsv(input_tsv,design_matrix,jid):
	df = pd.read_csv(input_tsv,sep="\t",header=None)
	for i in df[0].tolist():
		if not os.path.isfile(i):
			logging.error ("File not exist: %s"%(i))
			exit()
	for i in df[0].tolist():
		i = i+".bai"
		if not os.path.isfile(i):
			logging.error ("File not exist: %s"%(i))
			exit()
	group_dict ={}
	for i,r in df.iterrows():
		if r[2] in group_dict:
			group_dict[r[2]].append("%s.out"%(r[1]))
		else:
			group_dict[r[2]] = ["%s.out"%(r[1])]
	df2 = pd.read_csv(design_matrix,sep="\t",header=None)
	n = df2.shape[0]
	df2 = df2.drop_duplicates(2)
	if df2.shape[0] != n:
		logging.error ("Design Matrix contains non-unique output names!")
		exit()
	out = []
	for i,r in df2.iterrows():
		c1 = group_dict[r[0]]+group_dict[r[1]]
		c2 = [r[0]]*len(group_dict[r[0]])+[r[1]]*len(group_dict[r[1]])
		c3 = r[2]
		c1 = ",".join(c1)
		c2 = ",".join(c2)
		out.append([c1,c2,c3])
	df = pd.DataFrame(out)
	outfile="%s.design_tsv.input"%(jid)
	df.to_csv(outfile,sep="\t",header=False,index=False)
	return outfile
	
def main():

	args = my_args()
	args.gff = myData['%s_DEXseq_gff'%(args.genome)]
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			
	
	##------- add functions below ----------------------
	args.design_tsv = make_design_tsv(args.bam_tsv,args.design_matrix,args.jid)
	#-------------- run jobs ----------------------

	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























