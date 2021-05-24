#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
import pandas as pd
import datetime
import getpass
import uuid
import argparse
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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('--remove_zero',  help="remove all rows or cols that are zero", action='store_true')
	mainParser.add_argument('--row',  help="results on rows. This is to the opposite of pandas row and col, which is operations on rows or cols. For example, operations (e.g., find zeros) on cols will result in removing rows.", action='store_true')
	mainParser.add_argument('--col',  help="results on cols", action='store_true')
	mainParser.add_argument('--index',  help=" index is false", action='store_true')
	mainParser.add_argument('-f',"--input",  help="data table input",required=True)

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def read_data(args):
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
				

def main():

	args = my_args()
	df = read_data(args)

	#-------------- run jobs ----------------------
	if args.remove_zero:
		if args.row:
			df = df.loc[(df!=0).any(axis=1)]
		elif args.col:
			df = df.loc[(df!=0).any(axis=0)]
		else:
			df = df.loc[(df!=0).any(axis=1)]
	if not args.merge=="":
		df2 = pd.read_csv(args.merge,sep=guess_sep(args.merge),index_col=0,header=None)
		df3 = df2.loc[df.index.tolist()]
		df = pd.concat([df3[1],df],axis=1)
	
	#-------------- output ----------------------
	if args.header:
		df.to_csv(args.output,sep=args.sep,index=args.index)
	else:
		df.to_csv(args.output,sep=args.sep,index=args.index,header=False)
if __name__ == "__main__":
	main()







































