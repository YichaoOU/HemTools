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
	mainParser.add_argument('--sns_style',  help="searborn figure style, default is whitegrid, which is used by ggplot2. You can also use white", default="white")
	mainParser.add_argument('--xlabel',  help="define X-label", default="User values")
	mainParser.add_argument('--ylabel',  help="define X-label", default="")
	mainParser.add_argument('--title',  help="define title", default="")
	mainParser.add_argument('--axv',  help="verticle line", default=None)
	mainParser.add_argument('--min',  help="subset input values", default=None)
	mainParser.add_argument('--max',  help="subset input values", default=None)
	mainParser.add_argument('--bins',  help="subset input values", default="auto")
	mainParser.add_argument('--stat',  help="subset input values", default="count")
	mainParser.add_argument('--log2',  help="log2 transform raw values", action='store_true')
	mainParser.add_argument('--yscale_log',  help="log y-axis", action='store_true')
	mainParser.add_argument('--xscale_log',  help="log x-axis", action='store_true')
	mainParser.add_argument('--kde',  help="plot kde density plot", action='store_true')
	mainParser.add_argument('-o',"--output",  help="output prefix",default="histogram_"+username+"_"+str(datetime.date.today()))
	
	##------- add parameters above ---------------------
	# args = mainParser.parse_args()	
	args,unknown = mainParser.parse_known_args()
	known_pDict = vars(args)
	for i in range(0,len(unknown),2):
		mainParser.add_argument(unknown[i],default=unknown[i+1])
	args = mainParser.parse_args()
	user_pDict  = {k:v for k,v in vars(args).items() if k not in known_pDict or v != known_pDict[k]}

	return args,known_pDict,user_pDict


def make_histogram(user_pDict,pDict):

	sns.set_style(pDict['sns_style'])
	# plt.figure()
	# plot_list = {}
	min_v = 9999999
	max_v = -9999999
	values = []
	variables = []
	for k in user_pDict:
		if "_color" in k:
			continue
		tmp = pd.read_csv(user_pDict[k],header=None,comment="#")
		if pDict['log2']:
			tmp[0] = tmp[0].apply(lambda x:np.log2(x+1))
		if pDict['min']:
			tmp = tmp[tmp[0]>=float(pDict['min'])]
		if pDict['max']:
			tmp = tmp[tmp[0]<=float(pDict['max'])]
		if tmp[0].min() < min_v:
			min_v = tmp[0].min()
		if tmp[0].max() > max_v:
			max_v = tmp[0].max()
		values+= tmp[0].tolist()
		variables+= [k]*tmp.shape[0]
	# print (min_v,max_v)
	# min_v = float(min_v)
	# max_v = float(max_v)
	plot_df = pd.DataFrame()
	plot_df['values'] = values
	plot_df['variables'] = variables
	if pDict['bins'] != "auto":
		pDict['bins'] = int(pDict['bins'])
	sns.histplot(data=plot_df,x="values",hue="variables",kde=pDict['kde'],bins=pDict['bins'],stat=pDict['stat'])
	# for k in plot_list[k]:
		# try:
			# sns.distplot(tmp[0].tolist(),hist=True,color=user_pDict[k+"_color"],label=k+"",kde=pDict['kde'],hist_kws={"range": [min_v,max_v]})
		# except:
			# sns.distplot(tmp[0].tolist(),hist=True,label=k,kde=pDict['kde'],hist_kws={"range": [min_v,max_v]})
			# sns.histplot(tmp[0].tolist(),label=k,kde=pDict['kde'],hist_kws={"range": [min_v,max_v]})
	# plt.legend()

	plt.title(pDict['title'])
	if pDict['yscale_log']:
		plt.yscale("log")
	if pDict['xscale_log']:
		plt.xscale("log")

	if pDict['axv']:
		for i in pDict['axv'].split(","):
			i = float(i)
			plt.axvline(x=i, label='x=%s'.format(i), c="black",alpha=0.4,lw=1)
	# plt.xticks(rotation=90)
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
	make_histogram(user_pDict,known_pDict)
	


if __name__ == "__main__":
	main()
















