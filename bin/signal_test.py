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
	mainParser.add_argument('--bw_file',  help="input 1 or 2 bw files", required=True, metavar="FILE",nargs='+')
	mainParser.add_argument('--bed_file',  help="input 1 or 2 bed files", required=True, metavar="FILE",nargs='+')
	mainParser.add_argument('--set_style',  help="searborn figure style, default is whitegrid, which is used by ggplot2. You can also use white", default="whitegrid")
	mainParser.add_argument('--log2',  help="log2 transform raw values", action='store_true')
	mainParser.add_argument('--extend',  help="extend left and right, bed file", type=int,default=0 )
	mainParser.add_argument('--label1',  help="label1", type=str,default="Positive" )
	mainParser.add_argument('--flag',  help="could be t-test or empty", type=str,default=None )
	mainParser.add_argument('--label2',  help="label2", type=str,default="Negative" )
	mainParser.add_argument('--ylabel',  help="label2", type=str,default="Normalized signal" )
	mainParser.add_argument('--showfliers',  help="1 or 0", type=int,default=1 )
	mainParser.add_argument('-o',"--output",  help="output prefix",default="signal_test_plot_"+username+"_"+str(datetime.date.today()))
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def clean_bed(x,extend):
	import pandas as pd
	addon_string = str(uuid.uuid4()).split("-")[-1]
	output = x.split("/")[-1]+".bed4.%s"%(addon_string)
	
	if extend == 0:
		command = """awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$1":"$2"-"$3}' %s > %s"""%(x,output)
	else:
		command = """awk -F "\t" '{print $1"\t"$2-%s"\t"$3+%s"\t"$1":"$2"-"$3}' %s > %s"""%(extend,extend,x,output)
	
	os.system(command)
	# os.system("head %s"%(output))
	df = pd.read_csv(output,sep="\t",header=None)
	df = df.drop_duplicates(3)
	df = df.dropna()
	df[1] = df[1].astype(int)
	df[2] = df[2].astype(int)
	# df = df.astype(str)
	# print (df)
	df.to_csv(output,sep="\t",header=False,index=False)
	return output

def run_bigWigAverageOverBed(bed,bw):
	addon_string = str(uuid.uuid4()).split("-")[-1]
	out = bed+"-bwOverBed-%s-"%(addon_string)+bw.split("/")[-1]+".out"
	# command = "bigWigAverageOverBed -minMax %s %s %s"%(bw,bed,out)
	command = "bigWigAverageOverBed %s %s %s"%(bw,bed,out)
	os.system(command)
	df = parse_df(out)
	df.columns=['mean']
	os.system("rm %s"%(out))
	print (df.head())
	return df

def parse_df(x):
	import pandas as pd
	df = pd.read_csv(x,sep="\t",header=None,index_col=0)
	return pd.DataFrame(df[df.columns[-1]])

def define_test_type(df_list):
	index1 = df_list[0].index.tolist()
	index2 = df_list[1].index.tolist()
	if len(list(set(index1)-set(index2)))==0:
		return "wilcoxon"
	return "MW"

def random_sample_average(list1,list2):
	df = pd.DataFrame()
	df[0] = list1
	df[1] = list2
	out = []
	for i in range(100):
		tmp = df.sample(n=295)
		p = scipy.stats.wilcoxon(tmp[0],tmp[1]).pvalue
		out.append(p)
	return np.mean(out)
	

def make_pairwise_boxplot(list1,list2,output,flag,log_flag,sns_style,l1="Positive",l2="Negative",showfliers=True,ylabel="Normalized signal"):

	import matplotlib
	matplotlib.use('agg')
	import matplotlib.pyplot as plt
	import pandas as pd
	import seaborn as sns

	sns.set_style(sns_style)
	plot_df = pd.DataFrame()
	if log_flag:
		list1 = [np.log2(x+1) for x in list1]
		list2 = [np.log2(x+1) for x in list2]
	plot_df['value'] = list1+list2
	l1 = l1+"(%s)"%(len(list1))
	l2 = l2+"(%s)"%(len(list2))
	plot_df['variable'] = [l1]*len(list1)+[l2]*len(list2)
	# myMin = plot_df['value'].min()
	# myMax = plot_df['value'].max()
	# unit=(myMax-myMin)/50

	plt.figure()
	ax=sns.boxplot(x="variable",y='value',data=plot_df,linewidth=3,order=[l1,l2],showfliers = showfliers)
	for patch in ax.artists:
		r, g, bb, _ = patch.get_facecolor()
		patch.set_facecolor((r, g, bb, .8))
	myMin,myMax = plt.gca().get_ylim()
	unit=(myMax-myMin)/50

	print (plot_df.groupby("variable").describe())
	y=myMax+unit*1
	h=unit*1.5
	plt.plot([0, 0, 1, 1], [y, y+h, y+h, y], lw=1.5, c="black")
	if flag=="MW":
		plt.text(0.5, y+h+unit, "Mann-Whitney rank test: %.2E" % scipy.stats.mannwhitneyu(list1,list2).pvalue, ha='center', va='bottom', color="black")
	if flag=="wilcoxon":
		plt.text(0.5, y+h+unit, "Wilcoxon signed rank test: %.2E" % scipy.stats.wilcoxon(list1,list2).pvalue, ha='center', va='bottom', color="black")
		# plt.text(0.5, y+h+unit, "Wilcoxon signed rank test: %.2E" % random_sample_average(list1,list2), ha='center', va='bottom', color="black")
	if flag=="t-test":
		plt.text(0.5, y+h+unit, "T - test: %.2E" % scipy.stats.ttest_ind(list1,list2).pvalue, ha='center', va='bottom', color="black")
		# plt.text(0.5, y+h+unit, "Wilcoxon signed rank test: %.2E" % random_sample_average(list1,list2), ha='center', va='bottom', color="black")
	
	plt.ylim(myMin-unit*5,myMax+unit*5)
	if log_flag:
		plt.ylabel("log2-transformed %s"%(ylabel))
	else:
		plt.ylabel(ylabel)
	plt.xlabel("")
	plt.title(output)
	plot_df.to_csv("%s.csv"%(output),index=False)
	plt.savefig("%s.pdf"%(output), bbox_inches='tight')
	plt.savefig("%s.png"%(output), bbox_inches='tight')


def main():


	args = my_args()
	print args.bed_file
	
	print args.bw_file
	
	# clean bed
	
	bed_files = []
	for i in args.bed_file:
		bed_files.append(clean_bed(i,args.extend))
		
	# bw over bed
	values = []
	for i in bed_files:
		for j in args.bw_file:
			values.append(run_bigWigAverageOverBed(i,j)) 
	

	## determine test type
	if not args.flag:
		flag = define_test_type(values)
	## plot
	make_pairwise_boxplot(values[0]["mean"].tolist(),values[1]["mean"].tolist(),args.output,flag,args.log2,args.set_style,l1=args.label1,l2=args.label2,showfliers=args.showfliers,ylabel=args.ylabel)
	
	for m in bed_files:
		os.system("rm %s"%m)
	

if __name__ == "__main__":
	main()
















