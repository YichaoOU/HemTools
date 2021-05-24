#!/home/yli11/.conda/envs/py2/bin/python
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
from matplotlib_venn import venn2
import subprocess
import pandas as pd
import seaborn as sns
# %matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import scipy
import seaborn as sns
import glob
from scipy.stats import gaussian_kde

def send_email(attachments):
	username = getpass.getuser()
	command = ' echo "{{message}}" | mailx {{attachments}} -s "{{subject}}" -- User_name@stjude.org '
	command = command.replace("{{message}}","scatter correlation density plot"+"\n\nYour result is located at:\n"+os.getcwd())
	command = command.replace("{{subject}}","%s scatter correlation density plot"%(attachments[0]))
	command = command.replace("User_name",username)
	real_attachments = []
	for item in attachments:
		if os.path.isfile(item):
			real_attachments.append(item)
	attachments_string = map(lambda x: '-a "'+x+'" ',real_attachments)
	command = command.replace("{{attachments}}","".join(attachments_string))
	os.system(command)
	# print command
def add_identity(axes, *line_args, **line_kwargs):
	identity, = axes.plot([], [], *line_args, **line_kwargs)
	def callback(axes):
		low_x, high_x = axes.get_xlim()
		low_y, high_y = axes.get_ylim()
		low = max(low_x, low_y)
		high = min(high_x, high_y)
		identity.set_data([low, high], [low, high])
	callback(axes)
	axes.callbacks.connect('xlim_changed', callback)
	axes.callbacks.connect('ylim_changed', callback)
	return axes
def plot_scatter(x,y,df,output,highlight,regression=False,background_dots_color='#0000ff',highlight_color="red",lowess=False,diagnal_line=False):

	# x="treatment_mean"
	# y="control_mean"
	highlight_list = []
	fit_reg = True
	if highlight != None:
		fit_reg = regression
		try:
			highlight_list = pd.read_csv(highlight,header=None,sep="asdasdasdasd")[0].tolist()
		except:
			highlight_list = highlight.split(",")
	# print (highlight_list)
	df = df[[x,y]]
	print (df.shape)
	df = df.dropna()
	print (df.shape)
	# print (df.head())
	# print (set(highlight_list)-set(df.index))
	linewidth=1
	n_boot=30
	if diagnal_line:
		linewidth=0
		n_boot=0
	# df = df.transform(lambda x:np.log2(x+1))
	# df[0]
	# df[x] = df[x].apply(lambda x:np.log2(x+1))
	# df[y] = df[y].apply(lambda x:np.log2(x+1))

	cmap_blue = clr.LinearSegmentedColormap.from_list('custom blue', ['#e8e8e8',background_dots_color], N=1000)

	R2 = scipy.stats.pearsonr(df[x],df[y])[0]
	# R2 = scipy.stats.spearmanr(df[x],df[y])[0]
	
	
	f, ax = plt.subplots(figsize=(6, 6))
	
	# R2 = R2*R2

	# sns.regplot(data=df,x=x,y=y,scatter_kws={'alpha':0.3,'s':2,"color":"black"},line_kws={'linewidth':linewidth,'color':'black','label':r"$\rho$=%.3f"%(R2)},fit_reg=fit_reg,lowess=lowess,robust=True,n_boot=n_boot) # too slow
	scatter=True
	non_highlight = list(set(df.index)-set(highlight_list))
	df_non_highlight = df.loc[non_highlight]
	if df_non_highlight.shape[0]>4000:
		df_non_highlight = df_non_highlight.sample(n=4000)
	df = pd.concat([df_non_highlight,df.loc[highlight_list]])
	non_highlight = list(set(df.index)-set(highlight_list))
	# if df.shape[0]>8000:
		# df = df.sample(n=8000)
	sns.regplot(data=df,x=x,y=y,scatter=scatter,scatter_kws={'alpha':0.3,'s':2,"color":"black"},line_kws={'linewidth':linewidth,'color':'black','label':r"$\rho$=%.3f"%(R2)},fit_reg=fit_reg,lowess=lowess)
	# sns.regplot(data=df,x=x,y=y,scatter_kws={'alpha':0.3,'s':2,"color":"black"},line_kws={'linewidth':1,'color':'black','label':r"$\rho$=%.3f"%(R2)},fit_reg=False)
	
	xy = np.vstack([df.loc[non_highlight][x],df.loc[non_highlight][y]])
	z = gaussian_kde(xy)(xy)
	plt.scatter(x=df.loc[non_highlight][x],y=df.loc[non_highlight][y],c=z,alpha=0.3,s=50,cmap=cmap_blue,label=None,edgecolors="")
	if highlight == None:
		plt.legend()

	if regression:
		plt.legend()
	if highlight != None:
		plt.scatter(df.loc[highlight_list][x], df.loc[highlight_list][y], color=highlight_color,s=10,label = df.loc[highlight_list].index)
		if not regression:
			add_identity(ax, color='grey', ls='--')
			vmin = df.min().min()
			vmax = df.max().max()
			margin = (vmax-vmin)*0.1
			plt.xlim(vmin-margin,vmax+margin)
			plt.ylim(vmin-margin,vmax+margin)
	if diagnal_line:
		add_identity(ax, color='grey', ls='--')
		vmin = df.min().min()
		vmax = df.max().max()
		margin = (vmax-vmin)*0.1
		plt.xlim(vmin-margin,vmax+margin)
		plt.ylim(vmin-margin,vmax+margin)
		plt.legend()
	# ax = plt.gca()
	# diag_line, = ax.plot(ax.get_xlim(), ax.get_ylim(), ls="-", c=".3")
	# max_value = df.max().max()
	# plt.xlim(0,max_value)
	# plt.ylim(0,max_value)
	# plt.yscale('log')
	# plt.xscale('log')
	plt.savefig(output,bbox_inches='tight')
	
	
def my_args():
	username = getpass.getuser()
	
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument("-f",help="data table",required=True)	
	mainParser.add_argument("-s",help="sep",default="\t",type=str)	
	mainParser.add_argument("-x",help="column name for x axis",required=True,type=str)	
	mainParser.add_argument("-y",help="column name for y axis",required=True,type=str)	
	mainParser.add_argument("--index",help="index name for index",default=None,type=str)	
	mainParser.add_argument('--regression',  help="by default it is a dignal line", action='store_true')
	mainParser.add_argument('--diagnal_line',  help="force to draw a dignal line", action='store_true')
	mainParser.add_argument('--lowess',  help="fit a curve", action='store_true')
	mainParser.add_argument('-bc','--background_dots_color',  help="background_dots_color", default="#0000ff")
	mainParser.add_argument('-hc','--highlight_color',  help="highlight_color", default="#ff1500")
	mainParser.add_argument("--highlight",help="column name for y axis, sep by comma",default=None,type=str)	
	

	mainParser.add_argument('-o',"--output",  help="output file name",default=username+"_"+str(datetime.date.today())+".correlation_scatter_density.png")

	## https://stackoverflow.com/questions/21168120/python-argparse-errors-with-in-help-string
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():
	args = my_args()
	df = pd.read_csv(args.f,sep=args.s,comment="#")
	df = df.dropna()
	if not args.index == None:
		df.index = df[args.index].tolist()
		# print (df.head())
	plot_scatter(args.x,args.y,df,args.output,args.highlight,regression = args.regression,background_dots_color=args.background_dots_color,highlight_color=args.highlight_color,lowess=args.lowess,diagnal_line=args.diagnal_line)
	
	send_email([args.output])

	


if __name__ == "__main__":
	main()



