#!/usr/bin/env python

import sys
import os
import warnings
warnings.filterwarnings("ignore")
import datetime
import getpass
import pybedtools
import argparse
"""

"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
username = getpass.getuser()
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	

	mainParser.add_argument('-f',"--hic",  help=".hic file", required=True)
	mainParser.add_argument("--chr",  help="which chr to call", required=True)
	mainParser.add_argument("--juicer_commands",  help="juicer_tools commands to call interactions", default=None)
	mainParser.add_argument("-b","--bed",  help="user input bed file to subset interactions", default=None)
	mainParser.add_argument("--juicer_tools_path",  help="juicer_tools_path", default="/home/yli11/HemTools/share/script/jar/juicer_tools_1.13.01.jar")
	# mainParser.add_argument("--HICCUPS_parameters",  help="HICCUPS_parameters", default="-r 5000,10000,25000  -k KR -f 1,1,1  -p 4,2,1  -i 7,5,3  -t 0.02,1.5,1.75,2 -d 20000,20000,50000 --threads 0 --cpu")

	# mainParser.add_argument("--HICCUPS_parameters",  help="HICCUPS_parameters relaxed (final)", default="-r 25000 -k KR -f 0.2  -p 2 -i 5 -t 0.02,1.5,1.75,2 -d 20000 --cpu")
	# mainParser.add_argument("--HICCUPS_parameters",  help="HICCUPS_parameters relaxed (final)", default="-r 25000 -k VC -f 0.2  -p 2 -i 5 -t 0.02,1.5,1.75,2 -d 20000 --cpu")
	# mainParser.add_argument("--HICCUPS_parameters",  help="HICCUPS_parameters relaxed (best for now)", default="-r 25000 -k VC_SQRT -f 0.2  -p 2 -i 5 -t 0.02,1.5,1.75,2 -d 20000 --cpu")
	mainParser.add_argument("--HICCUPS_parameters",  help="HICCUPS_parameters relaxed (best for now)", default="-r 25000 -k VC_SQRT -f 0.2  -p 2 -i 5 -t 0.02,1.5,1.75,2 -d 20000 --cpu")
	# mainParser.add_argument("--HICCUPS_parameters",  help="HICCUPS_parameters relaxed (best for now)", default="-r 25000 -k VC_SQRT -f 1  -p 2 -i 7 -t 0.02,1.5,1.75,2 -d 20000 --cpu")
	# mainParser.add_argument("--HICCUPS_parameters",  help="HICCUPS_parameters relaxed (best for now)", default="-r 10000 -k VC_SQRT -f 1  -p 2 -i 7 -t 0.02,1.5,1.75,2 -d 20000 --cpu")


	# mainParser.add_argument('--refseq',  help="use refseq to extract promoter (not recommended if gene names are obtained from HemTools pipeline)", action='store_true')
	# mainParser.add_argument('-o',"--output",  help="output bed file name",default="",type=int)
	# mainParser.add_argument('-o',"--output",   help="output bed file name", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today())+".bed")	

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. Used for homer annotation", default='hg19',type=str)
	# genome.add_argument('--refseq_TSS',  help="refseq_TSS", default=myData['hg19_refseq_TSS'])
	# genome.add_argument('--Ensembl_TSS',  help="Ensembl_TSS", default=myData['hg19_Ensembl_TSS'])
	# genome.add_argument('--gene_name_db',  help="gene_name_db", default=myData['hg19_gene_name_db'])


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	import pandas as pd
	command = f"module load java/10.0.2;java -jar {args.juicer_tools_path} hiccups  -c {args.chr} {args.HICCUPS_parameters} {args.hic} {args.jid} "
	print (command)
	os.system(command)
	df1 = pd.read_csv(f"{args.jid}/merged_loops.bedpe",sep="\t",header=None,comment="#")
	df2 = pd.read_csv(f"{args.jid}/enriched_pixels_25000.bedpe",sep="\t",header=None,comment="#")
	try:
		df3 = pd.read_csv(f"{args.jid}/enriched_pixels_50000.bedpe",sep="\t",header=None,comment="#")
	except:
		df3 = pd.read_csv(f"{args.jid}/enriched_pixels_10000.bedpe",sep="\t",header=None,comment="#")
	df = pd.concat([df1,df2,df3])
	df[0] = ['chr'+x for x in df[0]]
	df[3] = ['chr'+x for x in df[3]]
	# print (df.shape)
	if args.bed: # get interaction regions to the given bed, output is also tsv file (use homer annotation)

		# df['L1'] = df[0]+"_"+df[1].astype(str)+"_"+df[2].astype(str)
		# df['L2'] = df[3]+"_"+df[4].astype(str)+"_"+df[5].astype(str)
		L1 = pybedtools.BedTool.from_dataframe(df[[0,1,2,3,4,5]])
		L2 = pybedtools.BedTool.from_dataframe(df[[3,4,5,0,1,2]])
		query_bed = pd.read_csv(args.bed,sep="\t",header=None)
		for r in query_bed.values:
			query = pybedtools.BedTool(f'{r[0]} {r[1]} {r[2]}', from_string=True)
			L1_overlap = L1.intersect(query,u=True).to_dataframe()
			L2_overlap = L2.intersect(query,u=True).to_dataframe()
			# print (L1_overlap)
			# print (L2_overlap)
			df2 = pd.concat([L1_overlap,L2_overlap])
			if df2.shape[0]==0:
				continue
			df2.columns = list(range(6))
			print (df2.shape)
			# exit()
			myList = [3,4,5]
			df2 = df2.drop_duplicates(myList)
			df2 = df2[myList]
			df2.to_csv(f"{args.jid}/{r[3]}.interacted_region.bed",sep="\t",header=False,index=False)
			command = f"module load homer/4.10;annotatePeaks.pl {args.jid}/{r[3]}.interacted_region.bed {args.genome}  > {args.jid}/{args.jid}.{r[3]}.annot.tsv"
			# print (command)
			os.system(command)

# x = pybedtools.BedTool.from_dataframe(df)
# Under the hood this is actually just saving a temp file that will be cleaned up once you exit Python, but it's a little more convenient than doing it yourself.

# By the way, there's also

# y = x.to_dataframe()
	
if __name__ == "__main__":
	main()

























