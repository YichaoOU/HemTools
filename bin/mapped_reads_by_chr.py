#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
import subprocess

"""
Every python wrapper is supposed to be similar, since they are using the same convention.

The only thing need to be changed is the guess_input function and the argparser function.

module load samtools/1.9

"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--bam_file",  help="a sorted bam with .bai index",required=True)

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. currently, only hg19 is available", default='hg19',type=str)
	genome.add_argument('--chrom_size',  help="This will be automatically changed with -g option", default=myData['hg19_main_chrom_size'])
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def check_chr(inFile,chr):
	out = subprocess.Popen("""samtools view -b {0} {1} | samtools flagstat - | grep mapped | head -n 1 | cut -d " " -f 1""".format(inFile,chr),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
	return out
	
def main():

	args = my_args()
	args.chrom_size = myData['%s_main_chrom_size'%(args.genome)]
	df = pd.read_csv(args.chrom_size,sep="\t",header=None)
	subprocess.call("samtools view -b -F 2048 -f 2 {0} > {0}.filtered.bam;samtools index {0}.filtered.bam".format(args.bam_file),shell=True)
	my_list = []
	for i in df[0]:
		my_list.append(check_chr("{0}.filtered.bam".format(args.bam_file),i))
	df[1] = [int(x) for x in my_list]
	print (df.head())
	print (df.head())
	df[2] = df[1]/df[1].sum()
	df.to_csv("%s.chr.mapping_reads.tsv"%(args.bam_file),sep="\t",header=False,index=False)




	
	
if __name__ == "__main__":
	main()







































