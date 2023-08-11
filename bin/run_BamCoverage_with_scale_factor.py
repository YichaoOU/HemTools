#!/hpcf/apps/python/install/2.7.12/bin/python


import pandas as pd
import glob
from joblib import Parallel, delayed
import argparse
import os
def run_bamCoverage(output_dir,bam_input,bw_output,effectiveGenomeSize,scaleFactor,paired_end_flag):
	# bam_input = bam_input.replace("/home/syi/",'~/dirs/')
	# print (bam_input)
	
	if not os.path.isfile("%s.bai"%(bam_input)):
		samtools_sort = "samtools sort -o %s.sorted %s"%(bam_input,bam_input)
		print (samtools_sort)
		os.system(samtools_sort)
		# samtools_index = "samtools index -o %s.sorted"%(bam_input)
		samtools_index = "samtools index %s.sorted"%(bam_input)
		os.system(samtools_index)
		bam_input = bam_input+".sorted"
	
	command = "bamCoverage -b %s -o %s/%s.scale.bw --smoothLength=200 --ignoreForNormalization chrX chrM   --effectiveGenomeSize %s --numberOfProcessors 4 --scaleFactor %s "%(bam_input,output_dir,bw_output,effectiveGenomeSize,scaleFactor)
	if paired_end_flag:
		command+= "--centerReads"
	os.system(command)


def parse_df(f):
	df = pd.read_csv(f,sep="\t",index_col=0)
	df = df.loc[['Assigned']]
	assigned = float(df.sum().tolist()[0])
	return assigned

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="normalize bam files using scale factor")
	mainParser.add_argument('-f',"--input_list",  help="a 3-col tsv file containing bam, peak, output_name",required=True)
	mainParser.add_argument('-e','--effectiveGenomeSize',  help="effectiveGenomeSize for bamCoverage", default="2451960000")
	mainParser.add_argument('-o','--output_dir',  help="output_dir", default=".")
	mainParser.add_argument('--paired_end_flag', action='store_true')
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	df = pd.read_csv(args.input_list,sep="\t",header=None)
	print (df)
	files = ["%s/%s.out.summary"%(args.output_dir,x) for x in df[2]]
	numbers = [parse_df(f) for f in files]
	df['factor'] = [1/(x/numbers[-1]) for x in numbers]
	print (df)
	# Parallel(n_jobs=df.shape[0])(delayed(run_bamCoverage)(args.output_dir,df.get_value(i,0),df.get_value(i,2),args.effectiveGenomeSize,df.get_value(i,'factor'),args.paired_end_flag) for i in df.index.tolist())
	Parallel(n_jobs=2)(delayed(run_bamCoverage)(args.output_dir,df.get_value(i,0),df.get_value(i,2),args.effectiveGenomeSize,df.get_value(i,'factor'),args.paired_end_flag) for i in df.index.tolist())
	
if __name__ == "__main__":
	main()






