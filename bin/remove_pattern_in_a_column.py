#!/hpcf/apps/python/install/2.7.13/bin/python
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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="merge input dataframes using row index. Assume input tables contain both row names and column names.")
	mainParser.add_argument('-s',"--sep",  help="this program can infer separator automatically, but it may fail. Use auto if the input tables contain different separators.",default="auto")
	mainParser.add_argument('-f',"--input",  help="input file",required=True)
	mainParser.add_argument("--use_col",  help="input col name",required=True)
	mainParser.add_argument("--remove_pattern",  help="things to remove",required=True)
	mainParser.add_argument("--remove_separator",  help="asd/34/8",required=True)
	

	
	mainParser.add_argument('-o',"--output",  help="output table name",default=username+"_"+str(datetime.date.today())+"_"+addon_string+".list")


	
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

	args = my_args()
	df = pd.read_csv(args.input,sep=guess_sep(args.input),index_col=0)
	# df = df[args.use_col]
	out = [x.split(args.remove_separator) for x in df[args.use_col]]
	# out = [x.split(remove_separator) for x in df[use_col]]
	out = pd.DataFrame(out)
	out.index = df.index.tolist()
	# out2 = pd.DataFrame((out==remove_pattern).astype(int).sum(axis=1))
	out2 = pd.DataFrame((out==args.remove_pattern).astype(int).sum(axis=1))
	out3 = out2[out2[0]==0]
	df = pd.DataFrame()
	df['filtered_names'] = out3.index.tolist()
	

	df.to_csv(args.output,sep="\t",index=False)
	print ("Output to table: %s"%(args.output))
if __name__ == "__main__":
	main()


















































