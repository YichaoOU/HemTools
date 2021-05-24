#!/hpcf/apps/python/install/2.7.13/bin/python

import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pylab as plt
import numpy as np
import scipy
import glob
import sys
import matplotlib.colors as clr
import argparse
import seaborn as sns
import re
def replace_by_list(x,myDict):
    for m in myDict:
        x = x.replace(m,str(myDict[m]))
    return x
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
				
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--file",  help="bed file",required=True)
	mainParser.add_argument('-o',"--output", default="output",help="output file name")
	mainParser.add_argument("--columns", default="None",help="specify column names, sep=,",type=str)
	mainParser.add_argument("--col_order", default="None",help="specify column order, sep=,",type=str)
	mainParser.add_argument("--sort_by", default="None",help="sort value by",type=str)
	mainParser.add_argument("--label", default="None",help="A label file, sep=tab",type=str)
	mainParser.add_argument('--ascending', action='store_true')
	mainParser.add_argument('--col_norm', action='store_true')
	
	
	



	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()

	if args.columns != "None":
		df = pd.read_csv(args.file,index_col=0,header=None,sep=guess_sep(args.file))
		df.columns = args.columns.split(",")
		df = df[args.col_order.split(",")]
	else:
		df = pd.read_csv(args.file,index_col=0)

	if args.label != "None":
		label = pd.read_csv(args.label,sep=guess_sep(args.label),index_col=0,header=None)
		# print label
		label[1] = label[1].map(lambda x: re.sub(r'\W+', '', x))
		myDict = label[1].to_dict()
		df.index = [replace_by_list(x,myDict) for x in df.index]

	fig, ax = plt.subplots(1, 1, figsize =(int(df.shape[1]*0.8),int(df.shape[0]*0.8)))
	cmap_red = clr.LinearSegmentedColormap.from_list('custom red', ['#%02x%02x%02x' % (255,255,255),'#%02x%02x%02x' % (111,7,7)], N=255)
	if args.sort_by != "None":
		df = df.sort_values(args.sort_by,ascending=args.ascending)
	# print df.head()
	if args.col_norm:
		normalized_df=(df-df.min())/(df.max()-df.min())
		sns.heatmap(normalized_df,fmt='.2f',annot=df,linewidths=.5,cbar =False,cmap=cmap_red)
	else:
		sns.heatmap(df,fmt='.2f',annot=True,linewidths=.5,cbar =False,cmap=cmap_red)
	ax.xaxis.tick_top()
	ax.xaxis.set_label_position('top') 
	plt.xticks(rotation=45) 
	plt.savefig("%s.pdf"%(args.output), bbox_inches='tight')


if __name__ == "__main__":
	main()


	
