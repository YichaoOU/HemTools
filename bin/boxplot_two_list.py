#!/hpcf/apps/python/install/2.7.13/bin/python


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

1. wilcoxin test for 2 bw and 1 bed

2. MW test for 2 bed and 1 bw


module load ucsc/041619


"""

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-l1',  help="list1", required=True)
	mainParser.add_argument('-l2',  help="list2", required=True)
	mainParser.add_argument('--set_style',  help="searborn figure style, default is whitegrid, which is used by ggplot2. You can also use white", default="whitegrid")
	mainParser.add_argument('--log2',  help="log2 transform raw values", action='store_true')
	mainParser.add_argument('-o',"--output",  help="output prefix",default="signal_test_plot_"+username+"_"+str(datetime.date.today()))
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def make_pairwise_boxplot(list1,list2,output,flag,log_flag,sns_style):

	import matplotlib
	matplotlib.use('agg')
	import matplotlib.pyplot as plt
	
	import seaborn as sns

	sns.set_style(sns_style)
	plot_df = pd.DataFrame()
	if log_flag:
		list1 = [np.log2(x+1) for x in list1]
		list2 = [np.log2(x+1) for x in list2]
	plot_df['value'] = list1+list2
	n1=len(list1)
	n2 = len(list2)
	plot_df['variable'] = ["Positive (n=%s)"%(n1)]*len(list1)+["Negative (n=%s)"%(n2)]*len(list2)
	myMin = plot_df['value'].min()
	myMax = plot_df['value'].max()
	unit=(myMax-myMin)/50

	plt.figure()
	ax=sns.boxplot(x="variable",y='value',data=plot_df,linewidth=3,order=["Positive (n=%s)"%(n1),"Negative (n=%s)"%(n2)])
	for patch in ax.artists:
		r, g, bb, _ = patch.get_facecolor()
		patch.set_facecolor((r, g, bb, .8))
	

	
	y=myMax+unit*1
	h=unit*1.5
	plt.plot([0, 0, 1, 1], [y, y+h, y+h, y], lw=1.5, c="black")
	if flag=="MW":
		pvalue=scipy.stats.mannwhitneyu(list1,list2).pvalue
		print (pvalue)
		plt.text(0.5, y+h+unit, "Mann-Whitney rank test: %.2E" % pvalue, ha='center', va='bottom', color="black")
	if flag=="wilcoxon":
		plt.text(0.5, y+h+unit, "Wilcoxon signed rank test: %.2E" % scipy.stats.wilcoxon(list1,list2).pvalue, ha='center', va='bottom', color="black")
	if flag=="t-test":
		plt.text(0.5, y+h+unit, "Welch T-test: %.2E" % scipy.stats.ttest_ind(list1,list2,equal_var=False).pvalue, ha='center', va='bottom', color="black")
	
	plt.ylim(myMin-unit*5,myMax+unit*5)
	if log_flag:
		plt.ylabel("log2-transformed read counts")
	else:
		plt.ylabel("Normalized read counts")
	plt.xlabel("")
	plt.savefig("%s.pdf"%(output), bbox_inches='tight')


def main():


	args = my_args()


	## plot
	make_pairwise_boxplot(pd.read_csv(args.l1,header=None)[0].tolist(),pd.read_csv(args.l2,header=None)[0].tolist(),args.output,"MW",args.log2,args.set_style)
	


if __name__ == "__main__":
	main()
















