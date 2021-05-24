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

	mainParser.add_argument('-f',"--input",  help="a list of gene ids or gene names", required=True)
	mainParser.add_argument('-o',"--output",   help="output bed file name", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today())+".list")

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('--gene_db_UCSC',  help="gene_name_db", default=myData['hg19_gene_db_UCSC'])
	genome.add_argument('--gene_db_HGNC',  help="gene_name_db", default=myData['hg19_gene_db_HGNC'])
	genome.add_argument('--gene_name_db',  help="gene_name_db", default=myData['hg19_gene_name_db'])
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
"|".join(q_list)
def find_match_return_index(df,c,q):
	return df[df[c].str.contains(q,regex=False,case=False,na=False)].index.tolist()

def get_target_ids(df,target_col,query_list):
	index_list = []
	not_found = 
	for q in query_list
		found_flag = False
		for c in df.columns:
			if c == target_col:
				continue
			current_index_list  = find_match_return_index(df,c,q)
			if len(current_index_list)>0:
				found_flag = True
				index_list += current_index_list
	return df.loc[index_list][target_col].tolist()
	
def main():

	args = my_args()
	args.gene_db_UCSC = myData['%s_gene_db_UCSC'%(args.genome)]
	args.gene_db_HGNC = myData['%s_gene_db_HGNC'%(args.genome)]
	args.gene_name_db = myData['%s_gene_name_db'%(args.genome)]
	
	UCSC = pd.read_csv(args.gene_db_UCSC,sep="\t",dtype=str)
	HGNC = pd.read_csv(args.gene_db_HGNC,sep="\t",dtype=str)
	query_list = pd.read_csv(args.input,header=None)[0].tolist()
	
	
	Ensembl_T = get_target_ids(UCSC,'hg19.knownToEnsembl.value',query_list)
	Ensembl_G = get_target_ids(UCSC,'Ensembl ID(supplied by Ensembl)',query_list)
	
	
	
	print ("Genes not found in refseq TSS database %s"%(len(not_in_count)))
	write_file(args.output+".not_found.list","\n".join(not_in_count))
	

	
if __name__ == "__main__":
	main()























