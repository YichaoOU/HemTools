#!/hpcf/apps/python/install/2.7.13/bin/python

import pandas as pd
import sys
import matplotlib
matplotlib.use('agg')
import os
import matplotlib as mpl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import argparse
import datetime
import getpass
import uuid
from scipy.interpolate import interp1d
import re, string
import matplotlib.colors as pltcolors



def plot_correlation(corr_matrix,labels, plot_filename, colormap='RdYlBu', image_format="png", plot_numbers=True, plotWidth=11, plotHeight=9.5):
	"""
	plots a correlation using a symmetric heatmap
	
	corr_matrix is pandas dataframe . values
	"""
	num_rows = len(labels)
	# set a font size according to figure length
	if num_rows < 6:
		font_size = 14
	elif num_rows > 40:
		font_size = 5
	else:
		font_size = int(14 - 0.25 * num_rows)
	mpl.rcParams.update({'font.size': font_size})
	# set the minimum and maximum values

	vmax = 1

	vmin = 0 if corr_matrix .min() >= 0 else -1

	# Compute and plot dendrogram.
	fig = plt.figure(figsize=(plotWidth, plotHeight))

	# axdendro = fig.add_axes([0.02, 0.12, 0.1, 0.66])
	# axdendro.set_axis_off()
	# y_var = sch.linkage(corr_matrix, method='complete')
	# z_var = sch.dendrogram(y_var, orientation='left',
						   # link_color_func=lambda k: 'darkred')
	# axdendro.set_xticks([])
	# axdendro.set_yticks([])
	cmap = plt.get_cmap(colormap)

	# this line simply makes a new cmap, based on the original
	# colormap that goes from 0.0 to 0.9
	# This is done to avoid colors that
	# are too dark at the end of the range that do not offer
	# a good contrast between the correlation numbers that are
	# plotted on black.
	if plot_numbers:
		cmap = pltcolors.LinearSegmentedColormap.from_list(colormap + "clipped",
														   cmap(np.linspace(0, 0.9, 10)))

	cmap.set_under((0., 0., 1.))
	# Plot distance matrix.
	axmatrix = fig.add_axes([0.13, 0.1, 0.6, 0.7])
	# index = z_var['leaves']
	# corr_matrix = corr_matrix[index, :]
	# corr_matrix = corr_matrix[:, index]
	if corr_matrix.shape[0] > 30:
		# when there are too many rows it is better to remove
		# the black lines surrounding the boxes in the heatmap
		edge_color = 'none'
	else:
		edge_color = 'black'

	img_mat = axmatrix.pcolormesh(corr_matrix,
								  edgecolors=edge_color,
								  cmap=cmap,
								  vmax=vmax,
								  vmin=vmin)
	axmatrix.set_xlim(0, num_rows)
	axmatrix.set_ylim(0, num_rows)

	axmatrix.yaxis.tick_right()
	axmatrix.set_yticks(np.arange(corr_matrix .shape[0]) + 0.5)
	axmatrix.set_yticklabels(np.array(labels).astype('str'))

	axmatrix.xaxis.set_tick_params(labeltop=True)
	axmatrix.xaxis.set_tick_params(labelbottom=False)
	axmatrix.set_xticks(np.arange(corr_matrix .shape[0]) + 0.5)
	axmatrix.set_xticklabels(np.array(labels).astype('str'), rotation=45, ha='left')

	axmatrix.tick_params(
		axis='x',
		which='both',
		bottom=False,
		top=False)

	axmatrix.tick_params(
		axis='y',
		which='both',
		left=False,
		right=False)

	# Plot colorbar
	axcolor = fig.add_axes([0.13, 0.065, 0.6, 0.02])
	cobar = plt.colorbar(img_mat, cax=axcolor, orientation='horizontal')
	cobar.solids.set_edgecolor("face")
	if plot_numbers:
		for row in range(num_rows):
			for col in range(num_rows):
				axmatrix.text(row + 0.5, col + 0.5,
							  "{:.2f}".format(corr_matrix[row, col]),
							  ha='center', va='center')

	fig.savefig(plot_filename, format=image_format)
	plt.close()


def my_args():
	username = getpass.getuser()

	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--input",help="correlation matrix with index and header",required=True)	
	mainParser.add_argument('-n',"--reorder_names",help="two columns showing old names and new names",required=True)	
	mainParser.add_argument('-s',"--sep",  help="this program can infer separator automatically, but it may fail. Use auto if the input tables contain different separators.",default="auto")
	mainParser.add_argument('--skiprows',  help="Pandas read_csv parameter to skip first N rows", default=0,type=int)
	# mainParser.add_argument('--cmap',  help="Pandas read_csv parameter to skip first N rows", default="jets",type=str)
	mainParser.add_argument('-o',"--output",  help="output file name",default=username+"_"+str(datetime.date.today()))
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def guess_sep(x):
	with open(x) as f:
		for line in f:
			if line[0] == "#":
				continue
			tmp1 = len(line.strip().split(","))
			tmp2 = len(line.strip().split("\t"))
			tmp3 = len(line.strip().split(" "))
			# print (tmp1,tmp2)
			if tmp1 > tmp2:
				return ","
			if tmp2 > tmp1: 
				return "\t"
			if tmp3 > tmp2: 
				return " "
			else:
				print ("Can't determine the separator. Please input manually")
				exit()


def main():
	## init
	args = my_args()
	if args.sep =="auto":
		args.sep=guess_sep(args.input)
	df = pd.read_csv(args.input,sep=args.sep,skiprows=args.skiprows,index_col=0)
	df.columns = [x.replace("'","").replace('"','') for x in df.columns]
	df.index = [x.replace("'","").replace('"','') for x in df.index]
	print (df)
	column_list = df.columns.tolist()
	if args.sep =="auto":
		args.sep=guess_sep(args.reorder_names)	
	new_names = pd.read_csv(args.reorder_names,sep=args.sep,header=None)
	print (new_names)
	df = df[new_names[0].tolist()]
	df = df.loc[new_names[0].tolist()]
	plot_correlation(df.values,new_names[1].tolist(), args.output)



if __name__ == "__main__":
	main()

