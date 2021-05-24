#!/home/yli11/.conda/envs/py2/bin/python


import matplotlib
import pandas as pd
matplotlib.use('agg')
import os
import glob
import argparse
import seaborn as sns
import gzip
import yaml
import numpy as np
import matplotlib.pyplot as plt
import datetime
import getpass
import uuid
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
				



def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="plot heatmap given a table, keep order.")

	mainParser.add_argument('-f',"--input",  help="data table input, assume index and header",required=True)
	mainParser.add_argument('-s',"--sep",  help="separator",default=None)
	mainParser.add_argument('-o',"--output",  help="output table name",default=username+"_"+str(datetime.date.today())+".heatmap")
	mainParser.add_argument("-W", "--width", help="Figure width, by default, w=N_col, if given, will replace the default value",type=int,default=None)
	mainParser.add_argument("-H", "--height", help="Figure height, by default, w=N_row/2, if given, will replace the default value",type=int,default=None)
	mainParser.add_argument("-c", "--cmap", help="python cmap",type=str,default="RdBu_r")
	# mainParser.add_argument("--drop",  help="generate motif html", action='store_true')
	mainParser.add_argument('-d',"--drop",  help="drop a column", default=None)



	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()

	if args.sep == "None":
		df = pd.read_csv(args.input,sep=guess_sep(args.input),index_col=0)
	else:
		df = pd.read_csv(args.input,sep=args.sep,index_col=0)
	if args.drop != None:
		df = df.drop([args.drop],axis=1)
	if args.width == None:
		args.width =df.shape[1]
	if args.height == None:
		args.height =int(df.shape[0])+1
	plt.figure(figsize=(args.width,args.height))
	g=sns.heatmap(df,annot=True,cmap=args.cmap,linewidth=0.2,fmt=".1f")
	# plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
	# plt.setp(g.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
	plt.savefig("%s.pdf"%(args.output.replace(".pdf","")),bbox_inches='tight')





if __name__ == "__main__":
	main()











