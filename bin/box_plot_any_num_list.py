#!/usr/bin/env python


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
	mainParser.add_argument('--ylabel',  help="define Y-label", default="User values")
	mainParser.add_argument('--log2',  help="log2 transform raw values", action='store_true')
	mainParser.add_argument('-o',"--output",  help="output prefix",default="boxplot_"+username+"_"+str(datetime.date.today()))
	
	##------- add parameters above ---------------------
	# args = mainParser.parse_args()	
	args,unknown = mainParser.parse_known_args()
	known_pDict = vars(args)
	for i in range(0,len(unknown),2):
		mainParser.add_argument(unknown[i],default=unknown[i+1])
	args = mainParser.parse_args()
	user_pDict  = {k:v for k,v in vars(args).items() if k not in known_pDict or v != known_pDict[k]}

	return args,known_pDict,user_pDict


def make_boxplot(plot_df,pDict):

	import matplotlib
	matplotlib.use('agg')
	import matplotlib.pyplot as plt
	
	import seaborn as sns

	sns.set_style(pDict['sns_style'])
	if pDict['log2']:
		plot_df = plot_df.transform(lambda x:np.log2(x+1))
	# plot_df['value'] = list1+list2
	# plot_df['variable'] = ["Positive (n=%s)"%(n1)]*len(list1)+["Negative (n=%s)"%(n2)]*len(list2)


	plt.figure()
	ax=sns.boxplot(x="variable",y='value',data=plot_df,linewidth=3,palette="husl")
	for patch in ax.artists:
		r, g, bb, _ = patch.get_facecolor()
		patch.set_facecolor((r, g, bb, .8))
	

	plt.xticks(rotation=90)
	plt.ylabel(pDict['ylabel'])
	plt.xlabel("")
	plt.savefig("%s.pdf"%(pDict['output']), bbox_inches='tight')

def p2f(x):
	return float(x.strip('%'))

def get_dataframe(user_pDict):
	df = pd.DataFrame()
	value = []
	variable = []
	for k in user_pDict:
		try:
			tmp = pd.read_csv(user_pDict[k],header=None,sep="\t")
		except:
			continue
		current_value = []
		if "x" in user_pDict:
			if "rmdup" in user_pDict:
				tmp = tmp.drop_duplicates(int(user_pDict['rmdup']))
			current_value = tmp[int(user_pDict['x'])].tolist()
		else:
			try:
				tmp[0] = tmp[0].apply(p2f)
				tmp[0] = tmp[0].astype(float)
			except:
				continue
			current_value = tmp[0].tolist()
		value += current_value
		variable += ["%s (n=%s)"%(k,tmp.shape[0])]*tmp.shape[0]
	df['value'] = value
	df['variable'] = variable
	return df

def main():


	args,known_pDict,user_pDict = my_args()
	# print (args)
	print (known_pDict)
	print (user_pDict)

	plot_df = get_dataframe(user_pDict)
	# plot
	make_boxplot(plot_df,known_pDict)
	


if __name__ == "__main__":
	main()
















