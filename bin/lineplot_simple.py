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
	mainParser.add_argument('-x',  help="define X-axis column name",required=True)
	mainParser.add_argument('-y',  help="define Y-axis column name",required=True)
	mainParser.add_argument('--ylabel',  help="define X-label", default="")
	mainParser.add_argument('--title',  help="define title", default="")

	mainParser.add_argument('--yscale_log',  help="log y-axis", action='store_true')

	mainParser.add_argument('-o',"--output",  help="output prefix",default="lineplot_"+username+"_"+str(datetime.date.today()))
	
	##------- add parameters above ---------------------
	# args = mainParser.parse_args()	
	args,unknown = mainParser.parse_known_args()
	known_pDict = vars(args)
	for i in range(0,len(unknown),2):
		mainParser.add_argument(unknown[i],default=unknown[i+1])
	args = mainParser.parse_args()
	user_pDict  = {k:v for k,v in vars(args).items() if k not in known_pDict or v != known_pDict[k]}

	return args,known_pDict,user_pDict


def make_lineplot(user_pDict,pDict):

	sns.set_style(pDict['sns_style'])

	x = []
	y = []
	colors = {}
	palette = "tab10"
	hue = []
	for k in user_pDict:
		if "_color" in k:
			colors[k.replace("_color","")] = user_pDict[k]
			continue
		tmp = pd.read_csv(user_pDict[k],sep="\t")
		x+= tmp[pDict['x']].tolist()
		y+= tmp[pDict['y']].tolist()
		hue+= [k]*tmp.shape[0]

		
	plot_df = pd.DataFrame()
	plot_df['x'] = x
	plot_df['y'] = y
	plot_df['hue'] = hue
	print (plot_df.head())
	if colors:
		palette = colors	

	sns.lineplot(data=plot_df,x="x", y="y", hue="hue",markers=True,palette=palette,marker='o')

	plt.title(pDict['title'])
	if pDict['yscale_log']:
		plt.yscale("log")
	plt.xlabel(pDict['xlabel'])
	plt.ylabel(pDict['ylabel'])
	plt.savefig("%s.pdf"%(pDict['output']), bbox_inches='tight')

def main():


	args,known_pDict,user_pDict = my_args()
	# print (args)
	print (known_pDict)
	print (user_pDict)

	make_lineplot(user_pDict,known_pDict)
	


if __name__ == "__main__":
	main()
















