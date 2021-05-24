#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


"""
Given motif.pwm and a user-bed file, perform motif scanning and generate bed file (bedjs) for each motif


"""

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--bed",  help="bed file",required=True)
	mainParser.add_argument('-m',"--motif",  help="motif",required=True)
	mainParser.add_argument('-c',"--cutoff",  default=0.0001, type=float)
	mainParser.add_argument('-o',"--output", default="output",help="output file name")
	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, mm10, mm9, hg38", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="genome version: hs, mm", default=myData['hg19_fasta'],type=str)


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	args.genome_fasta = myData['%s_fasta'%(args.genome)]
	print (args.output)
	## getfasta
	os.system("module load bedtools")
	os.system("bedtools getfasta -fi %s -bed %s -fo %s.fa"%(args.genome_fasta,args.bed,args.bed))
	
	## motif scanning
	os.system("module load meme")
	os.system("fimo --text --thresh %s --verbosity 1 --parse-genomic-coord %s %s.fa > %s.fimo"%(args.cutoff,args.motif,args.bed,args.bed))
	
	## fimo to bed
	df = pd.read_csv("%s.fimo"%(args.bed),sep="\t",comment="#",header=None)
	os.system("mkdir %s"%(args.output))
	for s,d in df.groupby(0):
		print ("Generating %s bed file"%(s))
		d[4] = s
		d[[1,2,3,4]].to_csv("%s/%s.bed"%(args.output,s),sep="\t",header=False,index=False)
		
if __name__ == "__main__":
	main()




