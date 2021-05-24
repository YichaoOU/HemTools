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
	mainParser.add_argument('--bed',  help="input is bed file", action='store_true')
	mainParser.add_argument('--ascending',  help="input is bed file", action='store_true')
	mainParser.add_argument('--sort_by',  help="sort input by which columns", default=None)
	mainParser.add_argument('--remove_duplicates',  help="remove duplicates on a specific column", default=None)
	mainParser.add_argument('--index',  help=" index is false", action='store_true')
	mainParser.add_argument('-f',"--input",  help="data table input")
	mainParser.add_argument("--merge",  help="merge with a data frame",default=None)
	mainParser.add_argument("--subset",  help="subset a data frame with a list",default=None)
	mainParser.add_argument("--collapse",  help="collapse the remaining columns into one column",default=None)
	mainParser.add_argument("--remove_cols_str",  help="remove columns containg this string",default=None)
	mainParser.add_argument('-s',"--sep",  help="separator",default="\t")
	mainParser.add_argument('-o',"--output",  help="output table name",default=username+"_"+str(datetime.date.today())+"_"+addon_string+".csv")
	mainParser.add_argument("--header",  help="input table has header", action='store_true')

	
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

def infer_subset_col(df,myList):
	myDict = {}
	for c in df.columns:
		# print (df[c].tolist())
		# print (myList)
		myDict[c] = len(list(set(df[c].tolist()).intersection(myList)))
	out = pd.DataFrame.from_dict(myDict,orient="index")
	out = out.sort_values(0,ascending=False)
	return out.index.tolist()[0]

def merge_col(r,cols):
	out = []
	for c in cols:
		if r[c]==".":
			continue
		out.append(r[c])
	out = list(set(out))
	return ",".join(out)
def main():

	args = my_args()
	df = read_data(args)
	if args.remove_cols_str:
		remove_cols = []
		myList = args.remove_cols_str.split(",")
		for c in df.columns:
			for x in myList:
				if x in c:
					remove_cols.append(c)
					break
		df = df.drop(remove_cols,axis=1)
		
	if args.bed:
		args.sep="\t"
		df[1] = df[1].astype(int)
		df[2] = df[2].astype(int)
	if args.sort_by:
		

		columns = args.sort_by.split(",")
		if not args.header:
			columns = [int(x) for x in columns]
		df = df.sort_values(columns,ascending=args.ascending)

	#-------------- run jobs ----------------------
	if args.collapse:
		merging_cols = df.columns[int(args.collapse):]
		df['merged_info'] = df.apply(lambda r:merge_col(r,merging_cols),axis=1)
		df = df.drop(merging_cols,axis=1)
		df.to_csv(args.output,sep="\t",index=args.index,header=args.header)
	if args.remove_zero:
		if args.row:
			df = df.loc[(df!=0).any(axis=1)]
		elif args.col:
			df = df.loc[(df!=0).any(axis=0)]
		else:
			df = df.loc[(df!=0).any(axis=1)]
	if args.merge:
		df2 = pd.read_csv(args.merge,sep=guess_sep(args.merge),index_col=0,header=None)
		df3 = df2.loc[df.index.tolist()]
		df = pd.concat([df3[1],df],axis=1)
	if args.subset:
		myList = pd.read_csv(args.subset,header=None)[0].tolist()
		c = infer_subset_col(df,myList)
		df = df[df[c].isin(myList)]
	
	if args.remove_duplicates:
		if not args.header:
			columns = int(args.remove_duplicates)
		df = df.drop_duplicates(columns)
		
	# print (args.sep)
	# print (df)
	if args.sep=="\\t":
		args.sep="\t"
	#-------------- output ----------------------
	# if args.header:
		# df.to_csv(args.output,sep=args.sep,index=args.index)
	# else:
	df.to_csv(args.output,sep=args.sep,index=args.index,header=args.header)
if __name__ == "__main__":
	main()


















































