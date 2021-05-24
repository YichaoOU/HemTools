#!/usr/bin/env python
import sys
import os
import pandas as pd
import matplotlib
import getpass
import uuid
import argparse
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as clr
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import scipy
import glob
import datetime

"""Plot heatmap given data frame


"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="plot heatmap given dataframe.")
	mainParser.add_argument('-f',"--input",  help="data table input",required=True)
	mainParser.add_argument("--sort_by",  help="usually this column should be logFC",required=True)
	mainParser.add_argument('-c1',"--value_cutoff_max",  help="subset genes by filtering out values above the cutoff, usually it should be p-value, input should be: column_name,value",default=None)
	mainParser.add_argument('-c2',"--value_cutoff_min",  help="subset genes by filtering out values below the cutoff, usually it should be log p-value, input should be: column_name,value",default=None)
	mainParser.add_argument("--index_by",  help="if the first column is not the correct index, which one?",default=None)
	mainParser.add_argument("--remove_cols",default="")
	mainParser.add_argument('-o',"--output",  help="output table name",default="gene_exp_heatmap."+username+"_"+str(datetime.date.today()))
	mainParser.add_argument("-pdf",  help="plot pdf instead of png, can be slower for large dataset", action='store_true')
	mainParser.add_argument("-W", "--width", help="Figure width, maximal use 200, usually 8 to 20",type=int,required=True)
	mainParser.add_argument("-H", "--height", help="Figure height, maximal use 200, usually 10 to 50",type=int,required=True)
	mainParser.add_argument("--fontsize", help="you can choose from 8 to 20 ",type=int,default=10)
	mainParser.add_argument("--linewidths", help="you can choose from 0, 0.1 ",type=float,default=0.1)
	mainParser.add_argument("--log2_transform",  help="input values will be log2 transformed", action='store_true')
	mainParser.add_argument("--show_name",  help="by default, >100 genes, name will not be shown, this option enforce to show name", action='store_true')
	
	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
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
				

def plot_n_save(df,args):
	df_z = df.T
	for c in df_z:
		df_z[c] = (df_z[c] - df_z[c].mean())/df_z[c].std()
	plt.figure(figsize=(args.width,args.height))
	if df_z.T.shape[0]<=100 or args.show_name:
		g=sns.heatmap(df_z.T,vmin=-2,vmax=2,cmap="RdBu_r",linewidths=args.linewidths,yticklabels=df_z.columns.tolist())
		g.set_yticklabels(g.get_ymajorticklabels(), fontsize = args.fontsize)
	else:
		g=sns.heatmap(df_z.T,vmin=-2,vmax=2,cmap="RdBu_r",yticklabels="")
	if args.pdf:
		plt.savefig("%s_heatmap.pdf"%(args.output), bbox_inches='tight')
	else:
		plt.savefig("%s_heatmap.png"%(args.output), bbox_inches='tight')

def main():

	args = my_args()
	"""below is the same for very dataframe scripts
	
	by default our input dataframe is bed format, which is \t separated with no header no index 
	
	"""

	df = pd.read_csv(args.input,sep=guess_sep(args.input),index_col=0)
	if args.value_cutoff_max != None:
		name,value = args.value_cutoff_max.split(",")
		value = float(value)
		df = df[df[name]<=value]
		df = df.drop([name],axis=1)
	if args.value_cutoff_min != None:
		name,value = args.value_cutoff_min.split(",")
		value = float(value)
		df = df[df[name]>=value]
		df = df.drop([name],axis=1)
	if args.index_by != None:
		df = df.set_index(args.index_by)
	df = df.sort_values(args.sort_by)
	df = df.drop([args.sort_by],axis=1)
	#-------------- pre-processing ----------------------
	remove_cols = str(args.remove_cols).split(",")
	try:
		remove_cols.remove("")
	except:
		pass
	if len(remove_cols)>0:
		df = df.drop(remove_cols,axis=1)
	if args.log2_transform:
		df = df.transform(lambda x:np.log2(x+1))
	print ("ploting size:",df.shape)
	plot_n_save(df,args)


if __name__ == "__main__":
	main()




