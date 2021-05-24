#!/home/yli11/.conda/envs/py2/bin/python

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import numpy as np
import datetime
import getpass
import uuid
import argparse
import glob
import scipy
import pandas as pd
"""

Usage:

box plot for multiple lists

dynamic argparse options

plot df format
	# plot_df['value'] 
	# plot_df['variable'] 

"""

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('--sns_style',  help="searborn figure style, default is whitegrid, which is used by ggplot2. You can also use white", default="whitegrid")
	mainParser.add_argument('--xlabel',  help="define X-label", default="User values")
	mainParser.add_argument('--ylabel',  help="define X-label", default="")
	mainParser.add_argument('--title',  help="define title", default="")
	mainParser.add_argument('--min',  help="subset input values", default=None)
	mainParser.add_argument('--max',  help="subset input values", default=None)
	mainParser.add_argument('--log2',  help="log2 transform raw values", action='store_true')
	mainParser.add_argument('--yscale_log',  help="log y-axis", action='store_true')
	mainParser.add_argument('--kde',  help="plot kde density plot", action='store_true')
	mainParser.add_argument('-o',"--output",  help="output prefix",default="countplot_"+username+"_"+str(datetime.date.today()))
	
	##------- add parameters above ---------------------
	# args = mainParser.parse_args()	
	args,unknown = mainParser.parse_known_args()
	known_pDict = vars(args)
	for i in range(0,len(unknown),2):
		mainParser.add_argument(unknown[i],default=unknown[i+1])
	args = mainParser.parse_args()
	user_pDict  = {k:v for k,v in vars(args).items() if k not in known_pDict or v != known_pDict[k]}

	return args,known_pDict,user_pDict


def make_count_barplot(user_pDict,pDict):

	sns.set_style(pDict['sns_style'])

	values = []
	variables = []
	colors = {}
	palette = "tab10"
	for k in user_pDict:
		if "_color" in k:
			colors[k.replace("_color","")] = user_pDict[k]
			continue
		tmp = pd.read_csv(user_pDict[k],header=None,comment="#")
		values+= tmp[0].tolist()
		variables+= [k]*tmp.shape[0]

		
	plot_df = pd.DataFrame()
	plot_df['values'] = values
	plot_df['variables'] = variables
	print (plot_df.groupby(['variables','values']).size())
	if pDict['min']:
		plot_df = plot_df[plot_df['values']>=float(pDict['min'])]
	if pDict['max']:
		plot_df = plot_df[plot_df['values']<=float(pDict['max'])]
	if colors:
		palette = colors	
	if plot_df['variables'].nunique() > 1:
		print (plot_df.head())
		# sns.countplot(data=plot_df,x="values",hue="variables",palette=palette)
		sns.countplot(data=plot_df,x="values",hue="variables")
	else:
		sns.countplot(data=plot_df,x="values",palette=palette)

	plt.title(pDict['title'])
	if pDict['yscale_log']:
		plt.yscale("log")
	plt.xticks(rotation=90)
	plt.xlabel(pDict['xlabel'])
	plt.ylabel(pDict['ylabel'])
	plt.savefig("%s.pdf"%(pDict['output']), bbox_inches='tight')

def p2f(x):
	return float(x.strip('%'))

def main():


	args,known_pDict,user_pDict = my_args()
	# print (args)
	print (known_pDict)
	print (user_pDict)

	# plot_df = get_dataframe(user_pDict)
	# plot
	make_count_barplot(user_pDict,known_pDict)
	


if __name__ == "__main__":
	main()
















