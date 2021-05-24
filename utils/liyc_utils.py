
"""pandas, seaborn, sklearn utils

This is an independent util script.

source activate py2

"""
import re
from glasbey import Glasbey
import plotly.graph_objs as go
import plotly.io as plio
import plotly.express as px
import plotly
plotly.io.orca.config.executable = "/home/yli11/.conda/envs/py2/bin/orca"
import plotly.io as pio
pio.orca.config.use_xvfb = True
import datetime
import uuid
import matplotlib
import pandas as pd
matplotlib.use('agg')
import seaborn as sns
import numpy as np
import scipy
import glob
import sys
import matplotlib.pyplot as plt
import os
from joblib import Parallel, delayed
from os.path import isfile,isdir
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
import matplotlib
import numpy as np
import scipy
import glob
import sys
import matplotlib.pyplot as plt
import os
import numpy as np
import getpass
import argparse
from matplotlib_venn import venn3,venn2
sys.setrecursionlimit(99999)
import umap

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans,AgglomerativeClustering,DBSCAN




"""some notes

common parameters
-----------------


for plotting
------------

xlabel="",ylabel="",title=""



sns
---

clustermap, heatmap can be saved directly by sns

barplot savefig has to use plt.savefig(bbox_inches='tight')
plotly colors
https://plot.ly/python/plotly-express/
"""
def longestSubstringFinder22(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""

def longestSubstringFinder(string1, string2):
	answers = {}
	s1 = re.split("\.|_|-",string1)
	s2 = re.split("\.|_|-",string2)
	flag = False
	count = 0
	
	for i in range(len(s1)):
		try:
			if not count in answers:
				answers[count] = []
			if s1[i] == s2[i]:
				answers[count].append(s1[i])
			else:
				count += 1
		except:
			break
	for k in answers:
		answers[k] = "_".join(answers[k])
	df = pd.DataFrame.from_dict(answers,orient="index")
	# print (df)
	df['len'] = [len(x.split("_")) for x in df[0]]
	df = df.sort_values("len",ascending=False)
	
	return [df[0].tolist()[0],df['len'].tolist()[0]]

def guess_label(names):
	lines = []
	for i in names:
		
		for j in names:
			if j == i:
				continue
			current = [i,j]
			current+=longestSubstringFinder(i,j)
			lines.append(current)
	df = pd.DataFrame(lines)
	# print (df)
	df = df.sort_values(3,ascending=False)
	df = df.drop_duplicates(0)
	return df[3].tolist()



def common_substring_liyc(myList):
	common_list =[]
	for i in re.split('_|-|\.|,',myList[0]):
		flag = True
		for j in myList[1:]:
			if not i in j:
				flag = False
				break
		if flag:
			common_list.append(i)
	newList = []
	for i in myList:
		new_name = []
		for j in re.split('_|-|\.|,',i):
			if j.isnumeric():
				continue
			if j in common_list:
				continue
			if len(j) == 1:
				continue
			if len(j) <=3:
				letter_flag = False
				number_flag = False
				for x in j:
					if x.upper() in ['A',"B","C"]:
						letter_flag = True
					if x.isdigit():
						number_flag = True
				if number_flag and letter_flag:
					continue
			new_name.append(j)
		newList.append("_".join(new_name))
	return newList
from difflib import SequenceMatcher
def similar(a, b):
	return 1-SequenceMatcher(None, a, b).ratio()
from sklearn.metrics import pairwise_distances
def stringList_to_distanceMatrix(myList):
	my_iter = []
	for i in myList:
		for j in myList:
			my_iter.append([i,j])

	values = Parallel(n_jobs=-1,verbose=10)(delayed(similar)(x[0],x[1]) for x in my_iter)
	df = pd.DataFrame(np.reshape(values, (len(myList), len(myList))))
	df.index = myList
	df.columns = myList
	return df
	
def group_similar_names(myList,k):
	myList = common_substring_liyc(myList)
	print (myList)
	X = stringList_to_distanceMatrix(myList)
	# X = pairwise_distances(myList,myList,similar,-1)
	print (X)

	model = AgglomerativeClustering(n_clusters=k, affinity="precomputed",linkage="average")
	model.fit(X)
	df = pd.DataFrame()
	df[0]=myList
	df[1] = model.labels_
	print (df)
	myDict = {}
	for s,d in df.groupby(1):
		myList = d[0].tolist()
		print (s,myList)
		try:
			common = common_substring_liyc_return_string(myList)
		except:
			common = myList[0]
		myDict[s] = common
	print (myDict)

	df[1] = df[1].replace(myDict)
	print (myDict)
	print (df)
	return df[1].tolist()

def common_substring_liyc_return_string(myList):
	common_list =[]
	for i in re.split('_|-|\.|,',myList[0]):
		flag = True
		for j in myList[1:]:
			if not i in j:
				flag = False
				break
		if flag:
			common_list.append(i)
	return "_".join(common_list)
	
def group_similar_names_dbscan(myList):
	myList = common_substring_liyc(myList)
	print (myList)
	X = stringList_to_distanceMatrix(myList)
	# X = pairwise_distances(myList,myList,similar,-1)
	print (X)

	model = DBSCAN( metric="precomputed",n_jobs=-1,min_samples=1,eps=0.09)
	model.fit(X)
	df = pd.DataFrame()
	df[0]=myList
	df[1] = model.labels_
	print (df)
	myDict = {}
	for s,d in df.groupby(1):
		myList = d[0].tolist()
		print (s,myList)
		try:
			common = common_substring_liyc_return_string(myList)
		except:
			common = myList[0]
		myDict[s] = common
	print (myDict)

	df[1] = df[1].replace(myDict)
	print (df)
	return df[1].tolist()
	

def general_df_reader(args):
	if args.header:
		if args.index:
			df = pd.read_csv(args.input,sep=args.sep,index_col=0)
		else:
			df = pd.read_csv(args.input,sep=args.sep)
	else:
		if args.index:
			df = pd.read_csv(args.input,sep=args.sep,index_col=0,header=None)
		else:
			df = pd.read_csv(args.input,sep=args.sep,header=None)
	return df

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
				

def read_csv_with_index(x):
	df = pd.read_csv(x,index_col=0)
	return df
	
def top_row_mean(df,n=50):
	tmp = df.copy()
	tmp['mean']=tmp.mean(axis=1)
	tmp = tmp.sort_values('mean',ascending=False)
	selected_list = tmp.index.tolist()[:n]
	print ("the minimal mean value given top %s is %s"%(n,tmp.at[selected_list[-1],'mean']))
	return df.loc[selected_list]

def row_mean_cutoff(df,c=5):
	return df[df.mean(axis=1) >= c]

def row_mean_percent_col_cutoff(df,frac=0.1,c=5):
	N = int(frac*df.shape[1])
	mean_list = np.mean(np.partition(df.values, -N)[:, -N:], 1)
	return df[mean_list >= c]
	
# def clustermap(df,output_name,xlabel="",ylabel="",title="",reIndexDict="",show_x=True,show_y=True,W="",H="",figure_type="png",method='average', metric='euclidean', z_score=None, standard_scale=None):
def clustermap(df,output_name,xlabel="",ylabel="",title="",reIndexDict="",show_x=True,show_y=True,W="",H="",figure_type="png",method='average', metric='euclidean', z_score=None, standard_scale=None):
	"""sns clustermap with some options"""
	df = df.copy()
	return_file_name = "%s.%s"%(output_name,figure_type)
	if not reIndexDict=="":
		df.index = [reIndexDict[x] for x in df.index.tolist()]
	if H=="":
		H = int(df.shape[0]/4)
		if H > 200:
			H=200
		if H < 2:
			H = 2
	if W=="":
		W = int(df.shape[1]/4)
		if W > 200:
			W=200
		if W < 2:
			W=2
	# print (df.head())
	# df.to_csv("test.csv")
	# print (df.isnull().any().any())
	# print (show_x,show_y)
	print ("%s size is %s * %s"%(return_file_name,W,H))
	# for x in df.dtypes:
		# if str(x) !="float64":
			# print (x)
	## I had one bug caused by that W is string type
	size_limit = 1000
	if df.shape[0] * df.shape[1] > size_limit*size_limit:
		if df.shape[0] > size_limit:
			print ("N row is %s. Taking %s random rows"%(df.shape[0],size_limit))
			df = df.sample(n=size_limit)
		if df.shape[1] > size_limit:
			print ("N col is %s. Taking %s random cols"%(df.shape[1],size_limit))
			df = df.sample(n=size_limit,axis=1)
	g=sns.clustermap(df,xticklabels=show_x,yticklabels=show_y,figsize=(int(W),int(H)),method=method, metric=metric, z_score=z_score, standard_scale=standard_scale)
	# for c in df.columns:
		# df[c] = df[c].astype(np.float)
	# plt.figure(figsize=(W,H))
	# g=sns.clustermap(df,xticklabels=show_x,yticklabels=show_y)
	# g=sns.clustermap(df)
	ax = g.ax_heatmap
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)	
	ax.set_title(title)	
	# plt.savefig(return_file_name, bbox_inches='tight')
	g.savefig(return_file_name,dpi=300)
	return return_file_name
	
def barplot_with_err(df,output_name,x,y,err,xlabel="",ylabel="",title="",figure_type="png",W="",H=""):
	return_file_name = "%s.%s"%(output_name,figure_type)
	## to do: get a sense of best W and H
	plt.figure(figsize=(int(W),int(H)))
	g=sns.barplot(x,y,data=df,yerr=df[err].tolist())
	for item in g.get_xticklabels():
		item.set_rotation(90)
	g.set(xlabel=xlabel, ylabel=ylabel,title=title)
	plt.savefig(return_file_name, bbox_inches='tight',dpi=300)
	return return_file_name

def plotly_scatter(plot_df,is_discrete=True,colorscale='Viridis',showlegend=True,xlabel="",ylabel="",title="",figure_type="png",output="output",width=500,height=500,text=False):
	
	"""
	
	
	https://plot.ly/python/line-and-scatter/
	
	maybe later try: go.Scattergl
	https://community.plot.ly/t/what-colorscales-are-available-in-plotly-and-which-are-the-default/2079
	This is the list of Plotly colorscales:
	[‘Blackbody’,
	‘Bluered’,
	‘Blues’,
	‘Earth’,
	‘Electric’,
	‘Greens’,
	‘Greys’,
	‘Hot’,
	‘Jet’,
	‘Picnic’,
	‘Portland’,
	‘Rainbow’,
	‘RdBu’,
	‘Reds’,
	‘Viridis’,
	‘YlGnBu’,
	‘YlOrRd’]	
	
	
	"""
	### discrete
	n_unique = plot_df['color'].nunique()
	color_set = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']	
	if n_unique >20 and n_unique <= 50:
		palette = [(228,26,28),(55,126,184),(77,175,74),(152,78,163),(255,127,0),(255,255,51),(166,86,40),(247,129,191),(153,153,153)]
		gb = Glasbey(base_palette=palette)
		p=gb.generate_palette(size=(n_unique-20))
		color_set_tmp = gb.convert_palette_to_rgb(p)
		color_set = color_set+["rgb%s"%(str(x)) for x in color_set_tmp]
	if is_discrete:
		# fig = go.Figure(data=go.Scatter(x=plot_df[0],
										# y=plot_df[1],
										# mode='markers',
										# text=plot_df['text'],
										# color=plot_df['color'],
										# marker=dict(
											# size=plot_df['size']
																						
											# )
										# ))
		if n_unique < 50:
			plot_df['color'] = plot_df['color'].astype(str)
		# print (plot_df)
		# size_max = 20
		try:
			size_max = plot_df['size'].astype(int).max()
		except:
			size_max=20
		if text:
			try:
				fig = px.scatter(plot_df,x="x",y='y',color='color',symbol='symbol',size='size',hover_data=['text'],text='text',color_discrete_sequence=color_set,template="plotly_white",size_max=size_max)
			except:
				fig = px.scatter(plot_df,x="x",y='y',text='text',color='color',size='size',hover_data=['text'],color_discrete_sequence=color_set,template="plotly_white",size_max=size_max)
		else:	
			try:
				fig = px.scatter(plot_df,x="x",y='y',color='color',symbol='symbol',size='size',hover_data=['text'],color_discrete_sequence=color_set,template="plotly_white",size_max=size_max)
			except:
				fig = px.scatter(plot_df,x="x",y='y',color='color',size='size',hover_data=['text'],color_discrete_sequence=color_set,template="plotly_white",size_max=size_max)
	else:
		# fig = go.Figure(data=go.Scatter(x=plot_df[0],
										# y=plot_df[1],
										# mode='markers',
										# text=plot_df['text'],
										# marker=dict(
											# size=plot_df['size'],
											# color=plot_df['color'],
											# colorscale=colorscale
																						
											# )
										# ))
		print ("input is continous data")
		fig = px.scatter(plot_df,x="x",y='y',color='color',size='size',hover_data=['text'],color_continuous_scale=px.colors.sequential.Rainbow,template="plotly_white",opacity=0.7)
		# https://medium.com/@abel.rech66/introduction-to-plotly-express-ee7bc478f333

	fig.update_layout(
		title=go.layout.Title(
			text=title
		),
		xaxis=go.layout.XAxis(
			title=go.layout.xaxis.Title(
				text=xlabel
			)
		),
		yaxis=go.layout.YAxis(
			title=go.layout.yaxis.Title(
				text=ylabel
			)
		),
		showlegend=showlegend
	)	

	# fig.update_layout(
	# 	title=go.layout.Title(
	# 		text=title,
	# 		xref="paper",
	# 		x=0
	# 	),
	# 	xaxis=go.layout.XAxis(
	# 		title=go.layout.xaxis.Title(
	# 			text=xlabel,
	# 			font=dict(
	# 				family="Courier New, monospace",
	# 				size=18,
	# 				color="#7f7f7f"
	# 			)
	# 		)
	# 	),
	# 	yaxis=go.layout.YAxis(
	# 		title=go.layout.yaxis.Title(
	# 			text=ylabel,
	# 			font=dict(
	# 				family="Courier New, monospace",
	# 				size=18,
	# 				color="#7f7f7f"
	# 			)
	# 		)
	# 	),
	# 	showlegend=showlegend
	# )				
	fig.write_html('%s.html'%(output), include_plotlyjs=True,auto_open=False)
	# fig.to_html('%s.html'%(output))
	# fig.write_image('%s.%s'%(output,figure_type), format=figure_type, width=width, height=height)

