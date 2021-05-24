#!/home/yli11/.conda/envs/py2/bin/python
from joblib import Parallel, delayed
import argparse
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from data import *
# import datetime
# import re
# import pandas as pd

def samtools_merge(input_list,out):
	command = "samtools merge -f %s %s; samtools index %s"%(out," ".join(input_list),out)
	print (command)
	os.system(command)


def depth_norm_bw(bam,effective_genome,output):
	command1 = f"bamCoverage -p 8 -b {bam} -o {output}.pos.bw --filterRNAstrand reverse --normalizeUsing RPGC --binSize 20 --effectiveGenomeSize {effective_genome} --ignoreForNormalization chrM"
	command2 = f"bamCoverage -p 8 -b {bam} -o {output}.neg.bw --filterRNAstrand forward --normalizeUsing RPGC --binSize 20 --effectiveGenomeSize {effective_genome} --ignoreForNormalization chrM"
	command3 = f"bamCoverage -p 8 -b {bam} -o {output}.bw --normalizeUsing RPGC --binSize 10 --effectiveGenomeSize {effective_genome} --ignoreForNormalization chrM"
	print (command1)
	print (command2)
	print (command3)
	return [command1,command2,command3]
	# return [command1,command2,command3]
	# return [command3]
	
	
	
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	# mainParser.add_argument('-o',"--output",  help="output file name for FDR bw", default="base_editor_score")
	mainParser.add_argument('-o',"--output",  help="just output label",required=True)
	mainParser.add_argument('file', type=str, nargs='+')


	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-e','--effectiveGenomeSize',  help="effectiveGenomeSize for bamCoverage", default=myPars['hg19_effectiveGenomeSize'])


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

## main function ##
def main():

	args = my_args()
	print (args.file)
	args.effectiveGenomeSize = myPars['%s_effectiveGenomeSize'%(args.genome)]
	if len(args.file)!=1:
		samtools_merge(args.file,"%s.merged.bam"%(args.output))
		run_list = depth_norm_bw("%s.merged.bam"%(args.output),args.effectiveGenomeSize,args.output)
		Parallel(n_jobs=3,verbose=10)(delayed(os.system)(m) for m in run_list)
	else:
		run_list = depth_norm_bw(args.file[0],args.effectiveGenomeSize,args.output)
		Parallel(n_jobs=3,verbose=10)(delayed(os.system)(m) for m in run_list)

if __name__ == "__main__":
	main()

