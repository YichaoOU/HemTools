#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="Heatmap for exon level expression")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-q',"--query",  help="query gene name", required=True)
	# mainParser.add_argument("--remove_first_line",  help="bdg file list", default=None)
	# mainParser.add_argument("--data_frame",  help="The input is a table, not bdg file list, index and header are required in this data frame", action='store_true' )
	mainParser.add_argument('-o',"--output",  help="output prefix",default="Heatmap_exon_"+username+"_"+str(datetime.date.today()))


	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-e','--exon_bed',  help="chrome size", default=myData['hg19_exon_bed'])
	genome.add_argument('--gene_name_db',  help="gene_name_db", default=myData['hg19_gene_name_db'])

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
import random
def plot_heatmap(df,output):
	tmp = df.sort_values(1,ascending=False)
	tmp = tmp[tmp.columns[6:]]
	columns = []
	for c in tmp.columns:
		if "-" in str(c):
			columns.append("_".join(c.split("-")[1:]).replace(".markdup",""))
		else:
			columns.append(c)
	# print (columns)
	tmp.columns = columns
	print (tmp.head())
	
	tmp2 = tmp.copy()
	for c in tmp.columns:
		tmp[c] = tmp[c]+random.uniform(0.000001, 0.0000000001)
	g=sns.clustermap(tmp,
				   standard_scale=0,
				   col_cluster=True,
				   row_cluster=False,
				   figsize=(max(tmp.shape[1],10),max(tmp.shape[0]/1.5,8)),
				   cmap="RdBu_r",
				   xticklabels=True,
				   linewidth=1,  
				   annot=tmp2.transform(lambda x:np.log2(x+1)),
				   yticklabels=True)
	# print ()
	col_reorder = [tmp.columns[i] for i in g.dendrogram_col.reordered_ind]
	tmp = tmp[col_reorder]
	tmp = tmp.div(tmp.max(axis=1), axis=0)
	tmp2 = tmp2[col_reorder]
	plt.figure(figsize=(max(tmp.shape[1],10),max(tmp.shape[0]/1.7,8)))
	g=sns.heatmap(tmp,
				   cmap="RdBu_r",
				   xticklabels=True,
				   linewidth=1,  
				   annot=tmp2.transform(lambda x:np.log2(x+1)),
				   yticklabels=True)
	plt.savefig(output, bbox_inches='tight')

def get_target_id(gene_name_db,query):
	"""This is a general util to get the target id given
	a gene name conversion database and a query
	"""
	# print gene_name_db
	df = pd.read_csv(gene_name_db,sep="\t",header=None )

	df = df.apply(lambda x: x.astype(str).str.upper())
	query = query.upper()

	target_id = []

	for c in df.columns:	
		tmp = df[df[c].isin([query])]
		if tmp.shape[0] == 0:
			continue
		for j in tmp.columns:
			target_id += tmp[j].tolist()

	target_id = list(set(target_id))
	print ("Found the following IDs matching your query:")
	print (target_id)
	if len(target_id) == 0:
		print ("No Match Found. Exit...")
		exit()
	return target_id
	
def main():

	args = my_args()
	args.gene_name_db = myData['%s_gene_name_db'%(args.genome)]
	args.exon_bed = myData['%s_exon_bed'%(args.genome)]
	if args.output == "Heatmap_exon_"+username+"_"+str(datetime.date.today()):
		args.output == "Heatmap_%s_"%(args.query)+username+"_"+str(datetime.date.today())

	#-------------- run jobs ----------------------
	# RUN INTERACTIVELY	
	# subset bed
	overlap_gene = get_target_id(args.gene_name_db,args.query)
	exon_bed = pd.read_csv(args.exon_bed,sep="\t",header=None)
	exon_bed[1] = exon_bed[1].astype(int)
	exon_bed[2] = exon_bed[2].astype(int)
	exon_bed = exon_bed[exon_bed[3].apply(lambda x:x.upper()).isin(overlap_gene)]
	exon_bed[3] = args.query
	exon_sub_bed = "%s.exon.bed"%(args.query)
	exon_bed.index = exon_bed[0]+":"+exon_bed[1].astype(str)+"-"+exon_bed[2].astype(str)
	exon_bed = exon_bed[~exon_bed.index.duplicated(keep='first')]

	exon_bed.to_csv(exon_sub_bed,sep="\t",header=False,index=False)
	
	
	# bw over bed
	command = "module load python/2.7.13 ucsc/041619;bw_over_bed.py"
	os.system(command)
	# clean bed
	files = glob.glob("%s*averageBW.csv"%(exon_sub_bed))
	df = pd.read_csv(files[0],index_col=0)
	df3 = pd.concat([exon_bed,df.loc[exon_bed.index]],axis=1)
	df3.to_csv("%s.clean.bed.tsv"%(exon_sub_bed),sep="\t",header=True,index=False)
	os.system("rm %s"%(exon_sub_bed))
	# plot
	plot_heatmap(df3,args.output)
	
if __name__ == "__main__":
	main()







































