#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
"""
designed for 20copy project, mid point of start, end is used.

"""

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

	mainParser.add_argument('-bed',  help="a bed file",required=True)
	mainParser.add_argument('-fa',"--fasta",  help="a fasta file",required=True)
	mainParser.add_argument('-o','--output',  help="output vcf file name",required=True)

	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, mm10, mm9, hg38", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="genome version: hs, mm", default=myData['hg19_fasta'],type=str)


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def get_insertion(r,seq,seq_rev):
	if r[5]=="-":
		# print ("rev")
		return r[4]+seq_rev
	else:
		# print ("pos")
		return r[4]+seq

def main():

	args = my_args()
	args.genome_fasta = myData['%s_fasta'%(args.genome)]

	def read_fasta(f):
		lines = open(f).readlines()
		return lines[1].strip().upper()
		


	seq = read_fasta(args.fasta)
	seq_rev = revcomp(seq)

	# print (seq,seq_rev)
	# get midpoint bed and base
	df = pd.read_csv(args.bed,sep="\t",header=None)
	df['mid'] = (df[1]+df[2])/2
	df.mid = df.mid.astype(int)
	df[1] = df.mid
	df[2] = df.mid+1
	df[3] = df[0]+"_"+df[1].astype(str)+"_"+df[2].astype(str)
	df.index = df[3].tolist()
	df[[0,1,2,3,4,5]].to_csv("tmp.bed",sep="\t",header=False,index=False)
	command = "module load bedtools/2.25.0;bedtools getfasta -fi %s -bed tmp.bed -fo tmp.tsv -name -tab"%(args.genome_fasta)
	# print (command)
	os.system(command)
	df2 = pd.read_csv("tmp.tsv",sep="\t",index_col=0,header=None)
	# print (df2)
	df[4] = df2[1].apply(lambda x:x.upper())
	
	# print (df.head())
	df[6] = df.apply(lambda r:get_insertion(r,seq,seq_rev),axis=1)
	# print (df.head())
	
	vcf_header="##fileformat=VCFv4.2\n"
	vcf_col_names = "#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	%s\n"%(args.bed.replace(".bed",""))
	vcf_header +=  vcf_col_names
	
	f = open(args.output,'wb')
	f.write(vcf_header)
	f.close()
	f = open(args.output,'a')
	df = df.sort_values([0,1])
	df['chr'] = df[0]
	df['pos'] = df[2]
	df['ID'] = df[3]
	df['REF'] = df[4]
	df['ALT'] = df[6]
	df['QUAL'] = "."
	df['FILTER'] =  "."
	df['INFO'] =  "."
	df['FORMAT'] =  "GT"
	df['last'] = "1|1"
	columns = ['chr','pos','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT','last']
	df[columns].to_csv(f,header=False,index=False,sep="\t")
	f.close()	

	
if __name__ == "__main__":
	main()































