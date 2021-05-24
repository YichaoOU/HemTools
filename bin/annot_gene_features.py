#!/home/yli11/.conda/envs/py2/bin/python

import sys

sys.path = sys.path[1:]

from tf_target_finder.utils import *

def parse_config(x):
	myDict = {}
	with open(x) as f:
		for line in f:
			line = line.strip()
			if len(line) < 2:
				continue
			if line[0] == "#":
				continue
			line = line.split()
			## make sure it is case-insensitive
			myDict[line[0].lower()] = line[1]
			myDict[line[0]] = line[1]
	return myDict
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
myData = parse_config(p_dir+"../config/data.config")

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	
	mainParser.add_argument('-f',"--input_bed",  help="3 column bed file, additional columns are OK, but will be ignored",required=True)

	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update the annotation file", default='hg19',type=str)
	genome.add_argument('--tss',help="tss feature file, 4 columns, chr, start, end , gene name",default=None)		
	genome.add_argument("--exon",  help="exon feature file, 4 columns, chr, start, end , gene name",default=None)
	genome.add_argument("--promoter",  help="promoter feature file, 4 columns, chr, start, end , gene name",default=None)
	genome.add_argument("--UTR5",  help="5UTR feature file, 4 columns, chr, start, end , gene name",default=None)
	genome.add_argument("--UTR3",  help="3UTR feature file, 4 columns, chr, start, end , gene name",default=None)
	genome.add_argument("--intron",  help="intron feature file, 4 columns, chr, start, end , gene name",default=None)
	genome.add_argument("--gene_name_list",  help="a file containing id to name conversion",default=None)
	mainParser.add_argument('--coding',  help="focus on coding genes only ", action='store_true')
	mainParser.add_argument("-d1",help="extend query bed for intersection",default=0,type=int)	
	mainParser.add_argument("-d2",help="extending genomic features for intersection",default=0,type=int)	
	
	mainParser.add_argument('-o',"--output",  help="output intermediate file",default="output")
	mainParser.add_argument("--gene_names",  help="use gene names instead of gene id, only works for hg19 now", action='store_true')
	# mainParser.add_argument("--label",  help="prefix for the file",default="genomic_features")
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def get_feature(r):
	if r['Exon_gene'] != ".":
		return "Exon"
	if r['Promoter_gene'] != ".":
		return "Promoter"
	if r['5UTR_gene'] != ".":
		return "5UTR"
	if r['3UTR_gene'] != ".":
		return "3UTR"
	if r['Intron_gene'] != ".":
		return "Intron"
	return "Intergenic"	
	
def get_annotation_data(args):
	if args.coding:
		if args.tss is None:
			args.tss = myData['%s_gencode33_TSS_coding'%(args.genome)]
		if args.exon is None:
			args.exon = myData['%s_gencode33_exon_coding'%(args.genome)]
		if args.promoter is None:
			args.promoter = myData['%s_gencode33_promoter_coding'%(args.genome)]
		if args.UTR5 is None:
			args.UTR5 = myData['%s_gencode33_5UTR_coding'%(args.genome)]
		if args.UTR3 is None:
			args.UTR3 = myData['%s_gencode33_3UTR_coding'%(args.genome)]
		if args.intron is None:
			args.intron = myData['%s_gencode33_intron_coding'%(args.genome)]
		if args.gene_name_list is None:
			args.gene_name_list = myData['%s_gencode33_gene_name_list'%(args.genome)]
	else:

		if args.tss is None:
			args.tss = myData['%s_gencode33_TSS'%(args.genome)]
		if args.exon is None:
			args.exon = myData['%s_gencode33_exon'%(args.genome)]
		if args.promoter is None:
			args.promoter = myData['%s_gencode33_promoter'%(args.genome)]
		if args.UTR5 is None:
			args.UTR5 = myData['%s_gencode33_5UTR'%(args.genome)]
		if args.UTR3 is None:
			args.UTR3 = myData['%s_gencode33_3UTR'%(args.genome)]
		if args.intron is None:
			args.intron = myData['%s_gencode33_intron'%(args.genome)]
		if args.gene_name_list is None:
			args.gene_name_list = myData['%s_gencode33_gene_name_list'%(args.genome)]

def replace_name(myDict,x):
	out = []
	for i in x.split(","):
		try:
			out.append(myDict[i])
		except:
			out.append(i)
	return ",".join(list(set(out)))
	
def main():

	args = my_args()
	get_annotation_data(args)
	
	my_query = query(args.input_bed)
	my_query.extend_query(args.d1)
	my_query.find_nearest_TSS(args.tss)
	myDict = {}
	myDict['Exon'] = args.exon
	myDict['Promoter'] = args.promoter
	myDict['5UTR'] = args.UTR5
	myDict['3UTR'] = args.UTR3
	myDict['Intron'] = args.intron
	
	for k in myDict:
		file = myDict[k]
		my_query.find_EPI_target(file,k,args.d2)

	my_query.print_log()
	df = my_query.df
	# print (df.head())
	df['Genomic_features'] = df.apply(get_feature,axis=1)
	if args.gene_names:

		df2 = pd.read_csv(args.gene_name_list)
		gene_id_dict = df2.set_index('gene_id')['gene_name'].to_dict()
		transcript_id_dict = df2.set_index('transcript_id')['gene_name'].to_dict()
		for c in df.columns:
			if "gene" in c:
				df[c] = [replace_name(gene_id_dict,x) for x in df[c]]
				df[c] = [replace_name(transcript_id_dict,x) for x in df[c]]
	
	

	df.to_csv(args.output,sep="\t",index=False)

	
if __name__ == "__main__":
	main()




































