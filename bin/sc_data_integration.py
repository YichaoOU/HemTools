#!/home/yli11/.conda/envs/pegasus/bin/python
import datetime
import getpass
import argparse
import pegasus as pg
import sys
import matplotlib
matplotlib.use('agg')
import matplotlib.pylab as plt
import os
import pandas as pd
"""

using pegasus for scRNA-seq data integration

input format is here:

https://pegasus.readthedocs.io/en/stable/usage.html

"""

# https://pegasusio.readthedocs.io/en/latest/_static/tutorials/pegasusio_tutorial.html

def my_args():
	username = getpass.getuser()

	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	# mainParser.add_argument('-s','--ref_seq',  help="input reference sequence", required=True)
	mainParser.add_argument('-f','--input_csv',  help="Need at least 2 columns with column names, Sample,Location, see: https://pegasus.readthedocs.io/en/stable/usage.html", required=True)
	mainParser.add_argument('--MT_prefix',  help="MT_prefix, seems that mm is mt- and human is MT-", default="MT-")
	mainParser.add_argument('--MT_percent',  help="MT_percent, default is 20, sometimes I use 10 or 5", default=20,type=float)
	mainParser.add_argument('--max_genes',  help="max_genes", default=6000,type=int)
	# mainParser.add_argument('--ref_name',  help="ref name", default=None)
	# mainParser.add_argument('-m','--min_freq',  help="default is 0.1%", default=0.1,type=float)
	mainParser.add_argument('-o',"--output",  help="output prefix pdf",default="sc_integration_"+username+"_"+str(datetime.date.today()))
	mainParser.add_argument("--citeseq",  help="is data is cite-seq",action='store_true')		

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()


	out = args.output
	command = "pegasus aggregate_matrix %s %s"%(args.input_csv,out)
	os.system(command)
	zarr_file="%s.zarr.zip"%(out)

	data = pg.read_input(zarr_file)
	if args.citeseq:
		data.select_data("%s-rna"%(data.uns['genome']))
	pg.qc_metrics(data, percent_mito=args.MT_percent,mito_prefix=args.MT_prefix,max_genes=args.max_genes)
	df_qc = pg.get_filter_stats(data)
	df_qc.to_csv("%s_qc_get_filter_stats.csv"%(out))

	pg.qcviolin(data, plot_type='gene')
	plt.savefig("%s_qcviolin_gene.pdf"%(out),bbox_inches='tight')

	pg.qcviolin(data, plot_type='count')
	plt.savefig("%s_qcviolin_UMI_count.pdf"%(out),bbox_inches='tight')

	pg.qcviolin(data, plot_type='mito')
	plt.savefig("%s_qcviolin_UMI_mito.pdf"%(out),bbox_inches='tight')


	# filtering
	pg.filter_data(data)
	pg.identify_robust_genes(data,percent_cells=0.05)
	pg.log_norm(data)




	print (data.obs['Channel'].value_counts())
	# save log norm data, rna
	df = pd.DataFrame.sparse.from_spmatrix(data.X)
	df.index = data.obs.index.tolist()
	df.columns = data.var.index.tolist()
	df.to_pickle("%s.rna.log_norm.pkl"%(out))

	if args.citeseq:
		data.select_data("%s-citeseq"%(data.uns['genome']))
		df = pd.DataFrame.sparse.from_spmatrix(data.X)
		df.index = data.obs.index.tolist()
		df.columns = data.var.index.tolist()
		df.to_pickle("%s.antibody.log_norm.pkl"%(out))
		data.select_data("%s-rna"%(data.uns['genome']))

	# without batch correction
	data_baseline = data.copy()
	pg.highly_variable_features(data_baseline, consider_batch=False,n_top=4000)
	data_baseline.var.loc[data_baseline.var['highly_variable_features']].sort_values(by='hvf_rank')

	pg.hvfplot(data_baseline)
	plt.savefig("%s_hvfplot_noBC.pdf"%(out),bbox_inches='tight')

	pg.pca(data_baseline,n_components=200)
	pg.neighbors(data_baseline,K=200)
	pg.louvain(data_baseline,resolution=2)
	pg.umap(data_baseline,n_neighbors=10,min_dist=0.4)
	pg.scatter(data_baseline, attrs=['louvain_labels', 'Channel'], basis='umap')
	plt.savefig("%s_without_BC.pdf"%(out),bbox_inches='tight')

	# with batch correction
	pg.highly_variable_features(data, consider_batch=True,n_top=4000)
	data.var.loc[data.var['highly_variable_features']].sort_values(by='hvf_rank')

	pg.hvfplot(data)
	plt.savefig("%s_hvfplot_noBC.pdf"%(out),bbox_inches='tight')

	data_harmony = data.copy()
	pg.pca(data_harmony,n_components=200)
	harmony_key = pg.run_harmony(data_harmony)
	pg.neighbors(data_harmony, rep=harmony_key,K=200)
	pg.louvain(data_harmony, rep=harmony_key,resolution=2)
	pg.umap(data_harmony, rep=harmony_key,n_neighbors=10,min_dist=0.4)
	pg.scatter(data_harmony, attrs=['louvain_labels', 'Channel'], basis='umap')
	plt.savefig("%s_Harmony_BC.pdf"%(out),bbox_inches='tight')
	pg.write_output(data_harmony,"%s_harmony.zarr"%(out))

	ddf = pd.DataFrame.sparse.from_spmatrix(data_harmony.X)
	ddf.index = data_harmony.obs.index.tolist()
	ddf.columns = data_harmony.var.index.tolist()
	data_harmony.select_data("%s-citeseq"%(data_harmony.uns['genome']))
	ddf2 = pd.DataFrame.sparse.from_spmatrix(data_harmony.X)
	ddf2.index = data_harmony.obs.index.tolist()
	ddf2.columns = data_harmony.var.index.tolist()
	df_all = pd.concat([ddf,ddf2],axis=1)
	df_all = df_all.sparse.to_dense()
	df_all = df_all.round(3)
	df_all.to_csv("%s.Harmony_correction.data.csv"%(out))
	### original harmony UMAP data
	out = data_harmony.obs.copy()
	out['UMAP1'] = data_harmony.obsm['X_umap'][:,0]
	out['UMAP2'] = data_harmony.obsm['X_umap'][:,1]
	from anndata import AnnData
	ann = AnnData(X=out[['UMAP1','UMAP2']],obs=out[['Channel','louvain_labels']])
	import scanpy as sc
	from matplotlib import rcParams
	sc.pl.scatter(ann, x="UMAP1",y="UMAP2",color='louvain_labels', legend_loc='on data',legend_fontsize=12, legend_fontoutline=2,frameon=False,title='clustering of cells')
	plt.savefig("%s_Scapy_UMAP.png"%(args.output),bbox_inches='tight')
	out.to_csv("%s_Harmony_UMAP.csv"%(args.output))


if __name__ == "__main__":
	main()


## custom for rick

# import pandas as pd
# df = pd.read_csv("Harmony_UMAP.csv")
# df2 = pd.read_csv("public_cluster_assignment.csv")
# df2.index = [x.split("_")[-1] for x in df2['Unnamed: 0']]
# df.index = [x.split("-")[-1] for x in df.barcodekey]
# df3 = pd.read_csv("info.csv",index_col=0)
# mydict = df2.ident.to_dict()
# mydict2 = df3.Source.to_dict()
# def replace_cluster(r):
	# if r.name in mydict:
		# return mydict[r.name]
	# else:
		# return mydict2[r.Channel]
# def replace_shape(r):
	# if r.name in mydict:
		# return "public data"
	# else:
		# return "Rick's data"
# df['cluster'] = df.apply(replace_cluster,axis=1)
# df['shape'] = df.apply(replace_shape,axis=1)
# df = df[~df.cluster.str.contains("Sample")]
# ann = AnnData(X=df[['UMAP1','UMAP2']],obs=df[['cluster']])
# sc.pl.scatter(ann, x="UMAP1",y="UMAP2",color='cluster',legend_fontsize=12, legend_fontoutline=2,frameon=False,title='clustering of cells')
# plt.savefig("cell_type_UMAP.pdf",bbox_inches='tight')
# df.to_csv("rick_public_cluster.annot.tsv",sep="\t")
# os.system('scatter_plotly.py -f rick_public_cluster.annot.tsv --index --header --xlabel UMAP1 --ylabel UMAP2 -x UMAP1 -y UMAP2 --title "Cell cluster" --color_using cluster --shape_using shape -o rick_public_cluster.annot')
