#!/usr/bin/env python
import pandas as pd
import os
import sys
import sys
import os
import pandas as pd
import datetime
import getpass
import uuid
import argparse
import glob
"""
Every python wrapper is supposed to be similar, since they are using the same convention.

The only thing need to be changed is the guess_input function and the argparser function.

look for ## CHANGE THE FUNCTION HERE FOR DIFFERENT WRAPPER

variable inherents from utils:
myData
myPars
myPipelines
"""
def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="Parse Vartrix output")

	mainParser.add_argument('-f',"--sample_list",  help="input sample list",required=True)
	mainParser.add_argument('-ref',  help="ref",required=True,type=int)
	mainParser.add_argument('-alt',  help="alt",required=True,type=int)
	# mainParser.add_argument("--header",  help="read with header",action='store_true')
	mainParser.add_argument('-o',"--output",  help="output table name",default=username+"_"+str(datetime.date.today())+"_vartrix.tsv")
	mainParser.add_argument('-min',"--min_read_count",  help="total reads cover the variant",default=3,type=int)
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
	
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


def parse_file(f,min_read,ref,alt):
	file="{0}_results/{0}/outs/vartrix.matrix.var_coverage.out".format(f)
	df = pd.read_csv(file,sep=" ",header=None,skiprows=3)
	
	total_cells = pd.read_csv(file,sep=" ",header=None,skiprows=2,nrows=1)[1].tolist()[0]
	sum_df = df.groupby(1)[2].sum()
	# sum_df = sum_df[sum_df>=5]
	sum_df = sum_df[sum_df>=100]
	df = df[df[1].isin(sum_df.index)]
	df_alt = df[df[0]==alt]
	df_alt = df_alt.set_index(1)
	df_ref = df[df[0]==ref]
	df_ref = df_ref.set_index(1)
	
	cells_ref = df_ref[df_ref[2]>=min_read].index.tolist()
	cells_alt = df_alt[df_alt[2]>=min_read].index.tolist()
	ref_alt = set(cells_ref).intersection(cells_alt)
	ref_ref = set(cells_ref) - set(ref_alt)
	alt_alt = set(cells_alt) - set(ref_alt)
	return len(ref_ref),len(ref_alt),len(alt_alt),total_cells - len(ref_ref)-len(ref_alt)-len(alt_alt)

def parse_file2(f,min_read,ref,alt):
	file="{0}_results/{0}/outs/vartrix.matrix.var_coverage.out".format(f)
	df = pd.read_csv(file,sep=" ",header=None,skiprows=3)
	sum_df = df.groupby(1)[2].sum()
	sum_df = sum_df[sum_df>=min_read]
	df = df[df[1].isin(sum_df.index)]
	df_alt = df[df[0]==alt]
	df_alt = df_alt.set_index(1)
	df_alt[3] = df_alt[2]/sum_df
	df_ref = df[df[0]==ref]
	df_ref = df_ref.set_index(1)
	df_ref[3] = df_ref[2]/sum_df
	return df_alt[3].tolist(),df_ref[3].tolist()

def main():

	args = my_args()
	sample_list = pd.read_csv(args.sample_list,header=None)[0].tolist()
	genotype = []
	
	for s in sample_list:
		genotype.append(parse_file(s,args.min_read_count,args.ref,args.alt))
	df = pd.DataFrame(genotype)
	df.columns = ['ref/ref','ref/alt','alt/alt','No Call']
	df.index = sample_list
	df.to_csv(args.output,sep="\t")
	
if __name__ == "__main__":
	main()


















































