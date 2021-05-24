#!/home/yli11/.conda/envs/py2/bin/python


import pandas as pd
import sys
import matplotlib
matplotlib.use('agg')
import argparse
import datetime
import getpass
import uuid
from tslearn.clustering import TimeSeriesKMeans
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from tslearn.clustering import KShape
from tslearn.clustering import KernelKMeans

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument('-f','--input',  help="input table", required=True)
	mainParser.add_argument('-t','--time_points',  help="input time points", required=True)
	mainParser.add_argument('-s',"--sep",  help="separator",default="\t")
	mainParser.add_argument('-n',"--nclusters",  help="input number of clusters",default=6,type=int)
	mainParser.add_argument('-m',"--metric",  help="metric for k-means,euclidean, dtw,softdtw",default="euclidean",type=str)
	mainParser.add_argument('--log2',  help="log2 transform raw values", action='store_true')
	mainParser.add_argument('--index',  help=" index is false", action='store_true')
	mainParser.add_argument('--header',  help=" header is false", action='store_true')
	# mainParser.add_argument('--kde',  help="plot kde density plot", action='store_true')
	mainParser.add_argument('-o',"--output_label",  help="output prefix",default="ts_kmeans_"+username+"_"+str(datetime.date.today()))
	mainParser.add_argument('--transpose',  help=" df transpose", action='store_true')
	mainParser.add_argument('--scale_t0',  help="scale data to t0", action='store_true')

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	

	return args

def general_df_reader(args):
	if args.header:
		if args.index:
			df = pd.read_csv(args.input,sep=args.sep,index_col=0)
		else:
			df = pd.read_csv(args.input,sep=args.sep)
	else:
		if args.index:
			df = pd.read_csv(args.input,sep=args.sep,index_col=0,header=None)
		else:
			df = pd.read_csv(args.input,sep=args.sep,header=None)
	if args.transpose:
		df = df.T
	return df


def main():


	args = my_args()
	df = general_df_reader(args)
	times = pd.read_csv(args.time_points,sep="\t",header=None)
	print (df.head())
	sns.clustermap(df.corr(),cmap="RdBu_r",linewidth=1,yticklabels=True,xticklabels=True)
	print ("Saving sample correlation plot to %s.corr.pdf"%(args.output_label))
	plt.savefig("%s.corr.pdf"%(args.output_label),bbox_inches='tight')

	new_columns = []
	for t in times[0].tolist():
		if t in new_columns:
			continue
		new_columns.append(t)
		df[t] = df[times[times[0]==t][1].tolist()].mean(axis=1)
	df = df[new_columns]
	if args.log2:
		df = df.transform(lambda x:np.log2(x+1))
	if args.scale_t0:
		df = df.subtract(df[new_columns[0]],axis=0)
	km = TimeSeriesKMeans(n_clusters=args.nclusters, verbose=True, random_state=0,metric=args.metric,n_jobs=-1,n_init=2,max_iter=500,tol=1e-8)
	# km = KShape(n_clusters=args.nclusters, verbose=True, random_state=0)
	# km = KernelKMeans(n_clusters=args.nclusters, verbose=True, random_state=0,n_jobs =-1)
	df['cluster'] = km.fit_predict(df.values)
	print ("Saving predicted clusters to %s.clusters.csv"%(args.output_label))
	df.to_csv("%s.clusters.csv"%(args.output_label))

	for s,d in df.groupby("cluster"):
		d = d[new_columns]
		cluster_size = d.shape[0]
		plot_df = pd.melt(d)
		plt.figure()
		if d.shape[0]>1000:
			d = d.sample(1000)
		for i,r in d.iterrows():
			plt.plot(r.tolist(), "k-",alpha=0.1)
		sns.lineplot(data=plot_df,x="variable",y="value",markers=True,marker='o',sort= False,color="red",markersize=10,linewidth=5)
		plt.title("Cluster: %s (n=%s)"%(s,cluster_size))

		print ("Vis predicted clusters to %s.clusters.%s.pdf"%(args.output_label,s))
		plt.savefig("%s.clusters.%s.pdf"%(args.output_label,s),bbox_inches='tight')

if __name__ == "__main__":
	main()








