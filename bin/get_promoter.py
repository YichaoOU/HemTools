#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
import warnings
warnings.filterwarnings("ignore")

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

	mainParser.add_argument('-f',"--input",  help="gene list, any type of Entrez ID, Ensemble Gene ID, Ensemble Transcript ID, gene name", required=True)
	mainParser.add_argument('-u',  help="upstream bp",default=1000,type=int)
	mainParser.add_argument('-d',  help="downstream bp",default=200,type=int)
	mainParser.add_argument('--refseq',  help="use refseq to extract promoter (not recommended if gene names are obtained from HemTools pipeline)", action='store_true')
	# mainParser.add_argument('-o',"--output",  help="output bed file name",default="",type=int)
	mainParser.add_argument('-o',"--output",   help="output bed file name", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today())+".bed")	
	
	

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('--refseq_TSS',  help="refseq_TSS", default=myData['hg19_refseq_TSS'])
	genome.add_argument('--Ensembl_TSS',  help="Ensembl_TSS", default=myData['hg19_Ensembl_TSS'])
	genome.add_argument('--gene_name_db',  help="gene_name_db", default=myData['hg19_gene_name_db'])
	"""
	gene_name_db is a tsv file, each column is a type of gene id
	
	refseq TSS query is gene name
	
	Ensembl gene bed query is Ensembl transcript ID
	
	"""
	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

## https://www.biostars.org/p/172344/
def row_apply(r,u,d):
	if r[5] == "+" or r[5] == 1:
		start = r[2]-u
		end = r[2] + d
	elif r[5] == "-" or r[5] == -1:
		start = r[2]-d
		end = r[2] + u
	else:
		print (r)
	return [start,end]	

def get_target_id(gene_name_db,query,target_id_col=0):
	"""This is a general util to get the target id given
	a gene name conversion database and a query
	"""
	# print gene_name_db
	df = pd.read_csv(gene_name_db,sep="\t",header=None)
	# print (df.head())
	df[2] = df[2].str.upper()
	query = [x.upper() for x in query]
	unmatched_list = query
	target_id = []
	# df.index = df[target_id_col]
	# print df.head()
	for c in df.columns:	
		tmp = df[df[c].isin(unmatched_list)]
		# print "############%s#############"%(c)
		# print tmp.head()
		
		target_id += tmp[target_id_col].tolist()
		unmatched_list = list(set(unmatched_list)-set(tmp[c].tolist()))

	target_id = list(set(target_id))
	return target_id,unmatched_list
	
def main():

	args = my_args()
	args.gene_name_db = myData['%s_gene_name_db'%(args.genome)]
	args.refseq_TSS = myData['%s_refseq_TSS'%(args.genome)]
	args.Ensembl_TSS = myData['%s_Ensembl_TSS'%(args.genome)]
	if args.refseq:
		print ("Using RefSeq TSS database: %s"%(args.refseq_TSS))
	
		df = pd.read_csv(args.refseq_TSS,sep="\t",header=None)
		df.index = df[3]
	
		myGeneList = pd.read_csv(args.input,header=None)[0].tolist()
		print ("Total number of input gene is : %s"%(len(myGeneList)))
		overlap_gene = []
		not_in_count =[]
		for g in myGeneList:
			g = g.upper()
			if df.index.contains(g):
				overlap_gene.append(g)
			else:
				not_in_count.append(g)
		print ("Genes not found in refseq TSS database %s"%(len(not_in_count)))
		write_file(args.output+".not_found.list","\n".join(not_in_count))
		
		df = df.loc[overlap_gene]
		df = df.dropna()
		df[['start','end']] = df.apply(lambda x:row_apply(x,args.u,args.d), axis=1).apply(pd.Series)
				

	else:

		print ("Using Ensembl TSS database: %s"%(args.Ensembl_TSS))
		df = pd.read_csv(args.Ensembl_TSS,sep="\t",header=None)
		# df[4] = df[4].str.upper()
		if df.at[0,3]==".":
			df.index = df[4].str.upper()
		else:
			df.index = df[3].str.upper()
		
		myGeneList = pd.read_csv(args.input,header=None)[0].tolist()
		print ("Total number of input gene is : %s"%(len(myGeneList)))
		overlap_gene,unmatched_list = get_target_id(args.gene_name_db,myGeneList,2)
		# print (overlap_gene)
		print ("Genes not found in Ensembl TSS database: %s"%(len(unmatched_list)))
		write_file(args.output+".not_found.list","\n".join(unmatched_list))
		# print overlap_gene
		# print unmatched_list
		df = df.loc[overlap_gene]
		df = df.dropna()
		# df.to_csv("test.bed",sep="\t",header=False,index=False)
		df[['start','end']] = df.apply(lambda x:row_apply(x,args.u,args.d), axis=1).apply(pd.Series)
	
	# print (df.head())
	out_df = df[[0,'start','end',3,4,5]]
	out_df['start'] = out_df['start'].astype(int)
	out_df['end'] = out_df['end'].astype(int)
	out_df[5] = out_df[5].replace({1:"+",-1:"-"})
	out_df.to_csv(args.output,sep="\t",header=False,index=False)		

	
if __name__ == "__main__":
	main()

























