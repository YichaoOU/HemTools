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

	mainParser.add_argument('-f',"--input_bed",  help="bed file 4 column",required=True)
	mainParser.add_argument('-l',"--bait_length",  help="bait_length",default=120)
	mainParser.add_argument("--src",  help="bait_length",default="/home/yli11/Programs/BaitsTools/bin/baitstools")

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10, custom. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="genome fasta file", default=myData['hg19_fasta'])


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def split_bed(df,bait_length=120):
	out = []
	step=50
	for i,r in df.iterrows():
		chr = r[0]
		start = r[1]
		end = r[2]
		count = 1
		for j in range(start-step,end+step,step):
			new_start = j
			new_end = j+bait_length
			new_name = "%s_%s"%(r[3],count)
			count+=1
			out.append([chr,new_start,new_end,new_name])
	return pd.DataFrame(out)

def main():

	args = my_args()
	if not args.genome == "custom":
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
	
	os.system("mkdir %s"%(args.jid))	
	# args.jid="bait_design_yli11_2022-03-08_f9406a95c814"
	# read bed file
	df = pd.read_csv(args.input_bed,sep="\t",header=None)
	df2 = split_bed(df,bait_length=args.bait_length)
	
	# get fasta
	out_fasta = "%s/bait_design.fa"%(args.jid)
	out_tsv = "%s/bait_design.tsv"%(args.jid)
	out_bed = "%s/bait_design.bed"%(args.jid)
	df2.to_csv(out_bed,sep="\t",header=False,index=False)
	command = "module load bedtools;bedtools getfasta -fi %s -fo %s -bed %s -name"%(args.genome_fasta,out_fasta,out_bed)
	command2 = "module load bedtools;bedtools getfasta -fi %s -fo %s -bed %s -name -tab"%(args.genome_fasta,out_tsv,out_bed)
	os.system(command)
	os.system(command2)
	my_fasta = pd.read_csv(out_tsv,sep="\t",header=None,index_col=0)
	# print (my_fasta)
	
	# run blat
	out_psl = "%s/bait_design.psl"%(args.jid)
	command = "module load blat;blat %s %s %s"%(args.genome_fasta,out_fasta,out_psl)
	os.system(command)
	
	
	# run QC
	
	command = "module load conda3/202105;source activate /home/yli11/.conda/envs/gem;%s checkbaits -i %s -w"%(args.src,out_fasta)
	os.system(command)
	
	# merge table
	qc_out = "out-filtered-params.txt"
	tmp = "out-filtered-baits.fa"
	os.system("rm %s"%(tmp))
	psl = pd.read_csv(out_psl,skiprows=5,sep="\t",header=None).groupby(9).size()
	# print (psl)
	qc = pd.read_csv(qc_out,sep="\t",index_col=0)
	df2.index = df2[3].tolist()
	
	df2 = pd.concat([df2,qc],axis=1)
	# print (df2)
	df2['#Matches'] = df2[3].map(psl)
	# print (df2)
	df2['seq'] = df2[3].map(my_fasta[1])
	df2 = df2.drop([3],axis=1)
	os.system("mv %s %s"%(qc_out,args.jid))
	df2.to_csv("%s/bait_design.final.csv"%(args.jid))
	# print (df2)


if __name__ == "__main__":
	main()

























