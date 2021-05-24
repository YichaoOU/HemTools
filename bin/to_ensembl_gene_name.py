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
	mainParser.add_argument('-o',"--output",   help="output bed file name", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('--gene_db_UCSC',  help="gene_name_db", default=myData['hg19_gene_db_UCSC'])
	genome.add_argument('--gene_db_HGNC',  help="gene_name_db", default=myData['hg19_gene_db_HGNC'])
	genome.add_argument('--gene_name_db',  help="gene_name_db", default=myData['hg19_gene_name_db'])
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def find_match_return_index(df,c,q):
	return df[df[c].str.contains(q,regex=False,case=False,na=False)].index.tolist()

def get_target_ids(df,target_col,query_list):
	
	not_found = []
	found_dict = {}
	for q in query_list:
		
		index_list = []
		for c in df.columns:
			if c == target_col:
				continue
			current_index_list  = find_match_return_index(df,c,q)
			index_list += current_index_list
		if len(index_list) == 0:
			not_found.append(q)
		else:
			found_dict[q] = df.loc[index_list][target_col].tolist()
	return not_found,found_dict
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def main():

	args = my_args()
	args.gene_db_UCSC = myData['%s_gene_db_UCSC'%(args.genome)]
	args.gene_db_HGNC = myData['%s_gene_db_HGNC'%(args.genome)]
	args.gene_name_db = myData['%s_gene_name_db'%(args.genome)]
	df = pd.read_csv(args.gene_name_db,sep="\t",header=None)
	
	UCSC = pd.read_csv(args.gene_db_UCSC,sep="\t",dtype=str)
	HGNC = pd.read_csv(args.gene_db_HGNC,sep="\t",dtype=str)
	query_list = pd.read_csv(args.input,header=None)
	if query_list.shape[0] != query_list[0].nunique():
		print ("Input list contains %s duplicates, that's OK."%(query_list.shape[0]-query_list[0].nunique()))
	query_list = query_list[0].unique().tolist()
	
	print ("searching in %s"%(args.gene_db_UCSC))
	not_found_UCSC,Ensembl_T = get_target_ids(UCSC,'hg19.knownToEnsembl.value',query_list)
	print ("searching in %s"%(args.gene_db_HGNC))
	not_found_HGNC,Ensembl_G = get_target_ids(HGNC,'Ensembl ID(supplied by Ensembl)',query_list)
	
	not_found = list(set(not_found_UCSC).intersection(not_found_HGNC))
	

	ids = []
	genes = []
	
	for q in query_list:
		if q in not_found:
			ids += [""]
			genes += [q]
		list1 = []
		list2 = []
		try:
			list1 = Ensembl_T[q]
		except:
			pass
		try:
			list2 = Ensembl_G[q]
		except:
			pass
		current_list = list(set(list1+list2))
		ids += current_list
		genes += [q]*len(current_list)
	
	
	
	out = pd.DataFrame()
	out['query_name'] = genes
	out['Ensembl_id'] = ids
	
	
	
	df_T = df.set_index(0)
	df_G = df.set_index(1)

	out['Ensembl_name'] = out['Ensembl_id'].map(merge_two_dicts(df_G[2].to_dict(), df_T[2].to_dict()))

	# print (out.head())
	out.to_csv("%s.gene_id_name_mapping.csv"%(args.output),index=False)
	
	tmp = out.copy()
	tmp = out[out['Ensembl_name'].isnull()]
	tmp = tmp.drop_duplicates('query_name')
	print ("Genes not found %s"%(tmp.shape[0]))
	tmp['query_name'].to_csv("%s.not_found.list"%(args.output),index=False,header=False)
	
	out = out.dropna()
	out = out.drop_duplicates('query_name')
	out['Ensembl_name'].to_csv("%s.for_get_promoter_py.list"%(args.output),index=False,header=False)
	
if __name__ == "__main__":
	main()























