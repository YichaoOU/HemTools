#!/home/yli11/.conda/envs/py2/bin/python

import argparse
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import networkx as nx
import os

import scipy

# bedtools 0.25 has bug

def to_bed(x,out):
	x[1] = x[1].astype(int)
	x[2] = x[2].astype(int)
	x.to_csv(out,sep="\t",header=False,index=False)

def read_bedpe(f):
	df = pd.read_csv(f,sep="\t",header=None)
	df[1] = df[1].astype(int)
	df[2] = df[2].astype(int)	
	df[4] = df[4].astype(int)
	df[5] = df[5].astype(int)
	df = df.dropna()
	return df
	
def read_bed(f):
	df = pd.read_csv(f,sep="\s",header=None)
	df[1] = df[1].astype(int)
	df[2] = df[2].astype(int)	
	# df = df.dropna()
	return df
	
def mango2bed(df):

	tmp = df[[0,1,2]].copy()
	tmp2 = df[[3,4,5]].copy()
	tmp2.columns = tmp.columns
	tmp = pd.concat([tmp,tmp2],axis=0)
	tmp['name'] = tmp[0]+"-"+tmp[1].astype(str)+"-"+tmp[2].astype(str)
	tmp = tmp.drop_duplicates('name')
	to_bed(tmp,"mango.bed")
	

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument('-p',"--pos_bed",  help="positive bed file, chr, start, end, etc.",required=True)
	mainParser.add_argument('-n',"--neg_bed",  help="negative bed file, chr, start, end, etc.",required=True)
	mainParser.add_argument('-f',"--bedpe",  help="bedpe, chr, start, end, chr, start, end, etc.",required=True)
	mainParser.add_argument('-o',"--output",  default="output")

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def get_num_interactions(bed,bedpe):

	df = read_bedpe(bedpe)
	df['source'] = df[0]+"-"+df[1].astype(str)+"-"+df[2].astype(str)
	df['target'] = df[3]+"-"+df[4].astype(str)+"-"+df[5].astype(str)
	print (df.head())
	g=nx.from_pandas_edgelist(df, 'source', 'target')
	my_dict = g.degree
	df1 = [[x[0],x[1]] for x in g.degree]
	df1 = pd.DataFrame(df1)
	df1.columns=['Genomic coordinates','Number of contacts']
	df1 = df1.set_index('Genomic coordinates')
	print (df1.head())
	mango2bed(df)

	## overlap query bed with mango bed
	os.system("bedtools intersect -a %s -b mango.bed -wao > intersect.bed"%(bed))

	df2 = read_bed("intersect.bed")

	
	df2[df2.columns[-2]] = df2[df2.columns[-2]].map(df1['Number of contacts'].to_dict())
	df2 = df2.fillna(0)
	print ("This is df2")
	print (df2.head())
	return df2[df2.columns[-2]].tolist()


def make_pairwise_boxplot(list1,list2,output):

	sns.set_style("whitegrid")
	plot_df = pd.DataFrame()
	plot_df['value'] = list1+list2
	plot_df['variable'] = ["Positive"]*len(list1)+["Negative"]*len(list2)
	myMin = plot_df['value'].min()
	myMax = plot_df['value'].max()
	unit=(myMax-myMin)/50

	plt.figure()
	ax=sns.boxplot(x="variable",y='value',data=plot_df,linewidth=3,order=['Positive','Negative'])
	for patch in ax.artists:
		r, g, bb, _ = patch.get_facecolor()
		patch.set_facecolor((r, g, bb, .8))
	

	
	y=myMax+unit*1
	h=unit*1.5
	plt.plot([0, 0, 1, 1], [y, y+h, y+h, y], lw=1.5, c="black")
	plt.text(0.5, y+h+unit, "Welch's T-test: %.2E" % scipy.stats.ttest_ind(list1,list2,equal_var=False).pvalue, ha='center', va='bottom', color="black")
	
	plt.ylim(myMin-unit*5,myMax+unit*5)
	plt.ylabel("Number of interactions")
	plt.savefig("%s.pdf"%(output), bbox_inches='tight')



def main():

	args = my_args()

	pos_list = get_num_interactions(args.pos_bed,args.bedpe)
	neg_list = get_num_interactions(args.neg_bed,args.bedpe)
	make_pairwise_boxplot(pos_list,neg_list,args.output)


	
if __name__ == "__main__":
	main()





