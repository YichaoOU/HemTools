#!/usr/bin/env python
import argparse
import pandas as pd
import matplotlib
matplotlib.use('agg')
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import sys

def row_apply(x):
	return '#%02x%02x%02x' % (x['r'],x['g'],x['b'])


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-e',"--emission_df",required=True)	
	mainParser.add_argument('-a',"--annotation_df",required=True)	
	mainParser.add_argument('-c',"--chromatin_state_definition_df",required=True)	
	mainParser.add_argument('-o',"--output",default="chromHMM_heatmap.pdf")	
	# mainParser.add_argument('-e',"--emission_df",required=True)	
	# mainParser.add_argument('-e',"--emission_df",required=True)	


	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def plot():

	"""
	
	input
	-----
	
	args.chromatin_state_definition_df
	
	chromatin state label, r,g,b, chromHMM_col_order
	

	"""
	
	args = my_args()


	emission = pd.read_csv(args.emission_df,sep="\t",index_col=0) ## original chromHMM output
	annotation = pd.read_csv(args.annotation_df,sep="\t",index_col=0) ## original chromHMM output
	text = pd.read_csv(args.chromatin_state_definition_df,sep="\t",index_col=0) ## specific format
	text['hex'] = text.apply(row_apply,axis=1)
	
	annotation = annotation.drop(['Base'])
	annotation.index = [int(x) for x in annotation.index.tolist()]
	annotation.columns = list(map(lambda x:x.split(".")[0],annotation.columns))
	num_states = emission.shape[0]
	num_markers = emission.shape[1]
	num_features = annotation.shape[1]
	text['order'] = list(range(num_states))
	## reorder emission and annotation df
	emission = emission.loc[text['chromHMM_col_order'].tolist()]
	# print annotation.head()
	# print emission.head()
	annotation = annotation.loc[text['chromHMM_col_order'].tolist()]
	
	
	##--------------- define colors --------------------------------------------
	cmap_blue = clr.LinearSegmentedColormap.from_list('custom blue', ['#%02x%02x%02x' % (255,255,255),'#%02x%02x%02x' % (0,0,255)], N=255)
	cmap_green = clr.LinearSegmentedColormap.from_list('custom dark green', ['#%02x%02x%02x' % (255,255,255),'#%02x%02x%02x' % (9,113,19)], N=255)
	cmap_purple = clr.LinearSegmentedColormap.from_list('custom purple', ['#%02x%02x%02x' % (255,255,255),'#%02x%02x%02x' % (114,6,106)], N=255)
	cmap_green2 = clr.LinearSegmentedColormap.from_list('custom green', ['#%02x%02x%02x' % (255,255,255),'#%02x%02x%02x' % (7,106,111)], N=255)
	cmap_red = clr.LinearSegmentedColormap.from_list('custom red', ['#%02x%02x%02x' % (255,255,255),'#%02x%02x%02x' % (111,7,7)], N=255)


	width = 1+num_markers+num_features
	## define the entire figure name
	fig1 = plt.figure(constrained_layout=False,figsize = (width,num_states))
	## define grid
	gs1 = fig1.add_gridspec(nrows=1, ncols=width, left=0, right=1, wspace=0.001, hspace=0.01)
	sns.set(font_scale=4)
	print (text)
	## define first sub figure g, which is the chromatin_state_labels
	chromatin_state_labels = fig1.add_subplot(gs1[:, 0:1])
	# print (pd.DataFrame(list(range(1,num_states))))
	g = sns.heatmap(pd.DataFrame(text['order']),\
	linecolor ='black',linewidths =3,\
	annot =pd.DataFrame(list(range(1,num_states+1))),\
	cmap=ListedColormap(text['hex']),cbar=False,\
	xticklabels=False,yticklabels=True,\
	ax=chromatin_state_labels,\
	annot_kws={"size": 25})
	g.set(xlabel="",ylabel="")
	
	## define emission sub figure a
	f1_ax1 = fig1.add_subplot(gs1[:, 1:(1+num_markers)])
	a=sns.heatmap(emission,cmap=cmap_blue,
	annot = emission,fmt='.2f',
	alpha=0.9,cbar=False,yticklabels=False,ax=f1_ax1,annot_kws={"size": 25})
	a.set(xlabel="",ylabel="")

	## define annotation sub figure b
	f1_ax2 = fig1.add_subplot(gs1[:, (1+num_markers):width])
	b=sns.heatmap((annotation-annotation.min())/annotation.max(),cmap=cmap_purple,
	vmin=0,vmax=1,cbar=False,alpha=0.9,
	annot = annotation,fmt='.1f',
	yticklabels=False,xticklabels=True,ax=f1_ax2,annot_kws={"size": 25})
	b.set(xlabel="",ylabel="")

	## rotate x ticks
	plt.xticks(rotation=90) 
	plt.savefig(args.output, bbox_inches='tight')




	
	
	

	
if __name__ == "__main__":
	plot()










