#!/hpcf/apps/python/install/2.7.13/bin/python
import argparse
import pandas as pd
import uuid
from os.path import isfile,isdir
import os
"""Add two additional columns to circle-seq/change-seq output table.

The two columns are obtained from Homer annotatePeaks, which are annotation type (e.g., intron, exon) and gene name (if available).

default is hg38 gene annotation and gene name from Ensembl.

input: CHANGE-seq table
output: CHANGE-seq table.annot.txt




"""


data = {}
data['hg38_gene_info'] = "/home/yli11/Data/Human/hg38/annotations/gencode_info.bed"
data['hg38_gtf'] = "/home/yli11/Data/Human/hg38/annotations/gencode.v30.chr_patch_hapl_scaff.annotation.gtf"

current_file_base_name = __file__.split("/")[-1].replace(".py","")
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-g','--genome',  help="[currently only hg38]. Genome version: hg19, hg38, mm9, mm10.", default='hg38',type=str)
	mainParser.add_argument('-a','--homer_annotatePeaks',  help="Homer annotatePeaks.pl output. With this input, the program will skip running Homer.",default=".")
	mainParser.add_argument('-f','--input',  help="CHANGE-seq off-targets table",required=True)
	mainParser.add_argument('--remove_chr',  help="bioinformatic pain. some times the genome is specified in chrchr1",action='store_true')

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
	
def get_gene_name(x):
	if "ENST" in x:
		geneID = "ENST"+x.split("ENST")[-1].split(",")[0].split(")")[0]
	else:
		geneID = "."
	return geneID

def add_gene_cols(change_seq_input,homer_input,gene_info):
	df = pd.read_csv(change_seq_input,sep="\t",header=None)
	homer = pd.read_csv(homer_input,sep="\t",index_col=0)
	gene = pd.read_csv(gene_info,sep="\t",header=None)
	df.index = df[3]
	gene.index = gene[1]
	# homer.index = homer['Annotation']
	homer['Gene'] = homer['Annotation'].apply(get_gene_name)
	myDict = gene[2].to_dict()
	# homer['Gene'] = homer['Gene'].replace(myDict)
	homer['Gene'] = homer['Gene'].map(lambda x: myDict.get(x,x))
	homer = homer.loc[df.index.tolist()]
	df['Annotation'] = homer['Annotation']
	df['Gene'] = homer['Gene']
	df.to_csv(change_seq_input.replace(".txt",".annot.txt"),header=False,index=False,sep="\t")

def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()
	
def remove_chr(f):
	out_file = f.replace(".txt",".removed_chr.txt")
	outlines = []
	with open(f) as x:
		for line in x:
			outlines.append(line.replace("chr","",1))
	write_file(out_file,"".join(outlines))
	return out_file

def main():
	## initial parameters
	args =  my_args()
	gtf_file = data["%s_gtf"%(args.genome)]
	gene_info = data["%s_gene_info"%(args.genome)]
	
	if not isfile(args.input):
		print (args.input,"not found")
		
	## step 0 remove chr
	if args.remove_chr:
		args.input = remove_chr(args.input)

	## step 1 RUN HOMER
	tmp_output = str(uuid.uuid4()).split("-")[-1]
	command = "annotatePeaks.pl %s none -gtf %s > %s"%(args.input,gtf_file,tmp_output)
	os.system(command)
	
	## step 2 add columns
	add_gene_cols(args.input,tmp_output,gene_info)
	os.system("rm %s"%(tmp_output))
	
	

if __name__ == "__main__":
	main()
	














