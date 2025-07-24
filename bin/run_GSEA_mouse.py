#!/usr/bin/env python


# for mouse single cell RNA_seq data
# run GSEA (based on logFC) and enrichR using gseapy
import pandas as pd
import sys
from gseapy.plot import barplot, dotplot
import gseapy as gp
from gseapy.plot import gseaplot
import matplotlib.pyplot as plt
import os

def run_enrichR(diff_list,gene_sets,out_file):
	enr = gp.enrichr(gene_list=diff_list,gene_sets=gene_sets,no_plot=False)
	enr.results.to_csv(f"{out_file}.enrichR.stats.csv",index=False)
	dotplot(enr.results,cutoff =0.1,ofname=f"{out_file}.enrichR.top10.dotplot.pdf")
	# plt.savefig(,bbox_inches='tight')
def run_GSEA(rnk,gene_sets,out_file):
	out_dir=os.getcwd()
	if "MJ.gmt" in gene_sets:
		pre_res = gp.prerank(rnk=rnk, gene_sets=read_gmt(gene_sets),min_size=2,processes=8,permutation_num=100,no_plot =True,max_size =1000)
	else:
		pre_res = gp.prerank(rnk=rnk, gene_sets=gene_sets,min_size=2,processes=8,permutation_num=100,no_plot =True,max_size =1000)
	res = pre_res.res2d
	os.system(f"mkdir -p {out_dir}/GSEA_plots_FDR_0.01")
	fdr = 0.01
	
	if len(gene_sets)<40:
		res.to_csv(f"{out_file}.GSEA.{gene_sets}.stats.csv")
	else:
		label=gene_sets.split("/")[-1]
		res.to_csv(f"{out_file}.GSEA.{label}.stats.csv")
	if not "MJ.gmt" in gene_sets:
		res = res[res.fdr<=fdr]
	for i in res.index.tolist():
		name = i.replace(" ","_").replace("/","_")
		try:
			gseaplot(rank_metric=pre_res.ranking, term=i, ofname=f'{out_dir}/GSEA_plots_FDR_0.01/{name}.pdf', **pre_res.results[i])
		except:
			continue

def read_gmt(f):
	# read gmt
	# lines = open("/research/rgs01/home/clusterHome/yli11/Data/Mouse/GMT/MJ.gmt").readlines()
	lines = open(f).readlines()
	MJ_sets={}
	for f in lines:
		if len(f)>10:
			items = f.strip().split()
			MJ_sets[items[0]] = items[2:]
	return MJ_sets

file=sys.argv[1]

out_file=sys.argv[2]


genesets=["KEGG_2019_Mouse"]
msigdb=["/research/rgs01/home/clusterHome/yli11/Data/Mouse/GMT/m2.cp.v2023.1.Mm.symbols.gmt","/research/rgs01/home/clusterHome/yli11/Data/Mouse/GMT/m5.go.v2023.1.Mm.symbols.gmt","/research/rgs01/home/clusterHome/yli11/Data/Mouse/GMT/mh.all.v2023.1.Mm.symbols.gmt","/research/rgs01/home/clusterHome/yli11/Data/Mouse/GMT/MJ.gmt"]



dff = pd.read_csv(file,index_col=0)
os.system(f"mkdir -p {out_file}_GSEA_mouse")
for cluster in dff.cluster.unique():
	print (file,cluster)
	df = dff[dff.cluster==cluster]
	df.index = df.gene.tolist()

	run_enrichR(df.gene.tolist(),genesets,out_file)
	rnk = df[['avg_log2FC']].reset_index()
	try:
		for g in genesets:
			print ("Running GSEA",g)
			tmp = rnk.copy()
			tmp['index'] = [x.upper() for x in tmp['index']]
			run_GSEA(tmp,g,out_file)
	except:
		print (genesets,"failed")
	for g in msigdb:
		try:
			print ("Running GSEA",g)
			run_GSEA(rnk,g,out_file)
		except:
			print ("Running GSEA",g,'failed')
	os.system(f"mv {out_file}.enrichR* Enrichr")
	os.system(f"mv {out_file}.GSEA* GSEA_Prerank")
	os.system(f"mkdir -p {cluster}")
	os.system(f"mv GSEA_Prerank/ {cluster}")
	os.system(f"mv Enrichr/ {cluster}")
	os.system(f"mv GSEA_plots_FDR_0.01/ {cluster}")
	os.system(f"mv {cluster}/ {out_file}_GSEA_mouse")
