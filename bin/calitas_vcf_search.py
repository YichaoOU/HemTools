#!/usr/bin/env python

import pandas as pd
import sys
import os
import argparse
import swifter
import re

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-g',"--gRNA", help="gRNA string: CTTGTCAAGGCTATTGGTCAngg", required=True)
	mainParser.add_argument('-f',"--input",  help="input vcf", required=True)
	mainParser.add_argument('-o',"--output_label",  help="output_label", required=True)
	mainParser.add_argument("--genome_fasta",  help="output_label", default="/home/yli11/Data/Human/hg38/fasta/hg38.main.fa")


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	df = pd.read_csv(args.input,sep="\t",header=None,comment="#")
	df = df[df[5]>0]
	df['GT'] = df[9].swifter.apply(lambda x: x.split(":")[0].replace("/","|").split("|"))
	df2 = df.explode("GT")
	df2 = df2[df2.GT!="0"]
	df2 = df2[df2.GT!="."]
	def get_variant(r):
		items = r[4].split(",")
		GT_index = int(r.GT)-1
		return items[GT_index]
	df2['ALT'] = df2.swifter.apply(get_variant,axis=1)   
	df2 = df2[df2.ALT!="*"]
	main_chr=["chr10","chr12","chr14","chr16","chr18","chr1","chr21","chr2","chr4","chr6","chr8","chrM","chrY","chr11","chr13","chr15","chr17","chr19","chr20","chr22","chr3","chr5","chr7","chr9","chrX"]
	for chr in main_chr:
		tmp = df2[df2[0]==chr]
		vcf_out = f"{args.output_label}.{chr}.vcf"
		with open(vcf_out, 'a') as file:
			file.write('##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n')
			tmp[[0,1,2,3,"ALT",5,6,6]].to_csv(file,sep="\t",header=False,index=False)
		command = f"module load htslib;bgzip -c {vcf_out} > {vcf_out}.gz;tabix -p vcf {vcf_out}.gz"
		os.system(command)
		bsub = f"""bsub -q priority -P Genomics -R 'rusage[mem=20000]' "module load calitas; calitas SearchReference -i {args.gRNA} -I {args.output_label}.{chr} -r {args.genome_fasta} -o {args.output_label}.{chr}.calitas.5.2.2.tsv --max-guide-diffs 5 --max-total-diffs 5 --max-pam-mismatches 2 --max-gaps-between-guide-and-pam 2 -v {vcf_out}.gz -c {chr}" """
		os.system(bsub)
		print (bsub)

# calitas SearchReference -i CTTGTCAAGGCTATTGGTCAngg -I g34 -r /home/yli11/Data/Human/hg38/fasta/hg38.main.fa -o g34.hits.5.1.3.tsv --max-guide-diffs 5 --max-pam-mismatches 1 --max-gaps-between-guide-and-pam 3 -v test3.vcf.gz -c chrY
# calitas SearchReference -i CTTGTCAAGGCTATTGGTCAngg -I g34 -r /home/yli11/Data/Human/hg38/fasta/hg38.main.fa -o g34.hits.5.1.3.tsv --max-guide-diffs 5 --max-pam-mismatches 1 --max-gaps-between-guide-and-pam 3 -v test3.vcf.gz -c chrY


if __name__ == "__main__":
	main()


















