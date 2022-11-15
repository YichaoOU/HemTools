#!/home/yli11/.conda/envs/captureC/bin/python



# run GSEA (based on logFC) and enrichR using gseapy
import pandas as pd
import sys
from gseapy.plot import barplot, dotplot
import gseapy as gp
from gseapy.plot import gseaplot
import matplotlib.pyplot as plt
import os
def guess_sep(x):
	with open(x) as f:
		for line in f:
			tmp1 = len(line.strip().split(","))
			tmp2 = len(line.strip().split("\t"))
			# print (tmp1,tmp2)
			if tmp1 > tmp2:
				return ","
			if tmp2 > tmp1: 
				return "\t"
			else:
				print ("Can't determine the separator. Please input manually")
				exit()
def run_enrichR(diff_list,gene_sets,out_file):
	enr = gp.enrichr(gene_list=diff_list,gene_sets=gene_sets,no_plot=True)
	enr2.results.to_csv(f"{out_file}.enrichR.stats.csv",index=False)
	dotplot(enr2.res2d,cutoff =0.1,ofname=f"{out_file}.enrichR.dotplot.pdf")
	# plt.savefig(,bbox_inches='tight')
def run_GSEA(rnk,gene_sets,out_file):
	out_dir=os.path.dirname(out_file)
	pre_res = gp.prerank(rnk=rnk, gene_sets=gene_sets,processes=8,permutation_num=100,no_plot =True,max_size =1000)
	res = pre_res.res2d
	os.system(f"mkdir -p {out_dir}/GSEA_plots_FDR_0.01")
	fdr = 0.01
	res.to_csv(f"{out_file}.GSEA.stats.csv",index=False)
	res = res[res.fdr<=0.01]
	for i in res.index.tolist():
		name = i.replace(" ","_")
		gseaplot(rank_metric=pre_res.ranking, term=i, ofname=f'{out_dir}/GSEA_plots_FDR_0.01/{name}.pdf', **pre_res.results[i])


file=sys.argv[1]

# data frame with gene name as in first column, header should be included
logFC_cutoff = float(sys.argv[2])
pvalue_cutoff = float(sys.argv[3])
logFC_col_name = sys.argv[4]
pvalue_col_name = sys.argv[5]
out_file=sys.argv[6]


genesets=["GO_Biological_Process_2021","GO_Cellular_Component_2021","GO_Molecular_Function_2021","KEGG_2019_Mouse","KEGG_2019_Human","KEGG_2021_Human","KEGG_2016","Reactome_2016","WikiPathways_2019_Mouse","WikiPathways_2019_Human"]
msigdb = "/home/yli11/Data/Human/MSigDB/msigdb.v7.5.1.symbols.gmt"


df = pd.read_csv(file,sep=guess_sep(file),index_col=0)
df.index = [x.upper() for x in df.index]
diff_list = df[df[logFC_col_name].abs()>=logFC_cutoff]
diff_list = diff_list[diff_list[pvalue_col_name]<=pvalue_cutoff].index.tolist()
run_enrichR(diff_list,genesets,out_file)
rnk = df2[logFC_col_name].reset_index()
run_GSEA(rnk,genesets+[msigdb],out_file)

