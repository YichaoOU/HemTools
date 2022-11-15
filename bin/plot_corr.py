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

def smart_names(my_list):
	my_count = {}
	for x in my_list:
		for i in re.split('_|-|\.',x):
			try:
				my_count[i]+=1
			except:
				my_count[i]=1
	my_count = pd.DataFrame.from_dict(my_count,orient="index")
	my_count = my_count[my_count[0]>1]
	my_count[1] = my_count[0]/float(len(my_list))
	my_count = my_count[my_count[1]<=0.95]
	good_names = my_count.index.tolist()
	new_list = []
	for x in my_list:
		current_name = []
		for i in re.split('_|-|\.',x):
			if i in good_names:
				current_name.append(i)
		if len(current_name)==0:
			new_list.append(x)
		else:
			new_list.append("_".join(current_name))
	return new_list
def send_email(attachments):
	username = getpass.getuser()
	command = ' echo "{{message}}" | mailx {{attachments}} -s "{{subject}}" -- User_name@stjude.org '
	command = command.replace("{{message}}","plot corr"+"\n\nYour result is located at:\n"+os.getcwd())
	command = command.replace("{{subject}}","plot corr")
	command = command.replace("User_name",username)
	real_attachments = []
	for item in attachments:
		if os.path.isfile(item):
			real_attachments.append(item)
	attachments_string = map(lambda x: '-a "'+x+'" ',real_attachments)
	command = command.replace("{{attachments}}","".join(attachments_string))
	os.system(command)
	# print command
	
	
def my_args():
	username = getpass.getuser()
	default = "95%"
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--input",help="correlation matrix with index and header",required=True)	
	mainParser.add_argument('-s',"--sep",  help="this program can infer separator automatically, but it may fail. Use auto if the input tables contain different separators.",default="auto")
	mainParser.add_argument('--skiprows',  help="Pandas read_csv parameter to skip first N rows", default=0,type=int)
	mainParser.add_argument('--use_cols',  help="use which columns", default="")
	mainParser.add_argument('--log2',  help="log2 transform value", action='store_true')
	mainParser.add_argument('--annot',  help="annot", action='store_true')
	mainParser.add_argument('--cmap',  help="Pandas read_csv parameter to skip first N rows", default="RdBu_r",type=str)
	mainParser.add_argument('-o',"--output",  help="output file name",default=username+"_"+str(datetime.date.today()))
	mainParser.add_argument("--size", help="Figure size, default=Ncol/4",default="auto")
	mainParser.add_argument("--smart_label",  help="try to infer a meaning unique group name, string will be splited by . - |, items that occur only once or occur above %s will be removed"%default.replace(r"%", r"%%"), action='store_true')
	## https://stackoverflow.com/questions/21168120/python-argparse-errors-with-in-help-string
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

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

def main():
	## init
	args = my_args()
	if args.sep =="auto":
		args.sep=guess_sep(args.input)
	df = pd.read_csv(args.input,sep=args.sep,skiprows=args.skiprows,index_col=0)
	if args.use_cols:
		cols = args.use_cols.split(",")
		df = df[cols]
	if args.log2:
		df = df.transform(lambda x:np.log2(x+1))
		df = df.corr()
	column_list = df.columns.tolist()
	if args.smart_label:
		column_list = smart_names(column_list)
		df.columns = column_list
		df.index = column_list
	if args.size == "auto":
		args.size = min(int(len(column_list)/4),8)
	else:
		args.size = int(args.size)
	print (df.head())
	sns.set(font_scale=0.3)
	print ("plotting correlation matrix clustering based on euclidean distance")
	# plt.figure()
	sns.clustermap(df,cmap=args.cmap,fmt='.2f',annot=args.annot,figsize=(args.size,args.size),method="average",metric="euclidean")
	plt.savefig("%s.euclidean.pdf"%(args.output), bbox_inches='tight')	
	# plt.close()
	print ("plotting correlation matrix clustering based on cosine distance")
	# plt.figure()
	sns.clustermap(df,cmap=args.cmap,figsize=(args.size,args.size),method="average",metric="cosine")
	plt.savefig("%s.cosine.pdf"%(args.output), bbox_inches='tight')		

if __name__ == "__main__":
	main()



