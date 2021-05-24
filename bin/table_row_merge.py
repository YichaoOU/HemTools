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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="merge input dataframes by rows")
	mainParser.add_argument('file', type=str, nargs='+')

	
	mainParser.add_argument("--header",  help="read with header",action='store_true')
	mainParser.add_argument("--index",  help="read with index",action='store_true')
	mainParser.add_argument("--file_path",  help="read with index",action='store_true')
	mainParser.add_argument("--file_name",  help="read with index",action='store_true')
	mainParser.add_argument('-o',"--output",  help="output table name",default=username+"_"+str(datetime.date.today())+"_"+addon_string+".tsv")


	
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
				
	
def general_df_reader(file,args):
	if args.header:
		if args.index:
			df = pd.read_csv(file,sep=guess_sep(file),index_col=0)
		else:
			df = pd.read_csv(file,sep=guess_sep(file))
	else:
		if args.index:
			df = pd.read_csv(file,sep=guess_sep(file),index_col=0,header=None)
		else:
			df = pd.read_csv(file,sep=guess_sep(file),header=None)
	return df


def main():

	args = my_args()

	df_list = [general_df_reader(f,args) for f in args.file]
	df = pd.concat(df_list)
	if args.file_path:
		index_list = [x.replace("./","").split("/")[0] for x in args.file]
		df.index = index_list
	df.to_csv(args.output,sep="\t")
	print ("Output to table: %s"%(args.output))
if __name__ == "__main__":
	main()


















































