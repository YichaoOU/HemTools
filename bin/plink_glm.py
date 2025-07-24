#!/usr/bin/env python

import pandas as pd
import sys
import os
import argparse
from joblib import Parallel, delayed
import uuid

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default="PLINK_GLM_output")	
	# group.add_argument('--outward',  help="get outward reads", action='store_true')
	# group.add_argument('--inward',  help="get inward reads", action='store_true')
	# group = mainParser.add_mutually_exclusive_group(required=True)
	# group.add_argument('-p','--pipeline_name',  help="which pipeline to run, e.g., atac_seq")
	# group.add_argument("--list_pipelines",  help="list all available pipelines",action='store_true')		
	# group.add_argument("--guess_input",  help="Let the program generate the input files for you.",action='store_true')
	# group.add_argument("--user_lsf",  help="user defined lsf file")
	
	
	mainParser.add_argument('-f',"--input",  help="quantative counts",required=True)
	mainParser.add_argument('-v',"--vcf",  help="vcf file for PLINK",required=True)
	mainParser.add_argument('-p',"--plink_parameters",  help="additional parameters",default="")

	
	# mainParser.add_argument('--softlinks',  help=argparse.SUPPRESS,default="")
	# mainParser.add_argument('--treatment_bam',  help=argparse.SUPPRESS)
	# mainParser.add_argument('--port',  help=argparse.SUPPRESS)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def run_plink(vcf,pheno,pheno_name,out_dir,parameters):
	## tmp bed here is a specific command for my porject
	## pheno_name is chr_start_end, and start-100 end+100 is tmp_bed
	rand_str = str(uuid.uuid4()).split("-")[-1]
	chr,start,end = pheno_name.split("_")
	# if pheno_name!="chr9_121888844_121888867":
		# return 0
	start = int(start)-100
	end = int(end)+100
	tmp_bed = pd.DataFrame([chr,start,end]).T
	tmp_bed_file = rand_str+".plink.tmp.bed"
	tmp_bed.to_csv(tmp_bed_file,sep="\t",header=False,index=False)
	# faster if you load plink2, 13min to 1 min
	# command = f"module load plink2;plink2 --vcf {vcf} --extract bed0 {tmp_bed_file} --pheno {pheno} --pheno-name {pheno_name} --glm --output-chr 26 --freq counts --out {out_dir}/{pheno_name} {parameters}"
	command = f"plink2 --vcf {vcf} --extract bed0 {tmp_bed_file} --pheno {pheno} --pheno-name {pheno_name} --glm --output-chr 26 --freq counts --out {out_dir}/{pheno_name} {parameters}"
	# print (command)
	os.system(command)
	os.system('rm '+tmp_bed_file)
def main():

	args = my_args()
	os.system("mkdir %s"%(args.jid))
	df = pd.read_csv(args.input,sep="\t")
	if df.columns[0]!="#IID":
		print (args.input,"PLINK pheno format error, need to have the first column name as #IID or #FID")
		exit()
	# run_plink(args.vcf,args.input,"chr10_107611596_107611619",args.jid,args.plink_parameters)
	# run_plink(args.vcf,args.input,"chr11_113638924_113638947",args.jid,args.plink_parameters)
	Parallel(n_jobs=-1,verbose=10)(delayed(run_plink)(args.vcf,args.input,pheno_name,args.jid,args.plink_parameters) for pheno_name in df.columns[1:].tolist())



if __name__ == "__main__":
	main()


















