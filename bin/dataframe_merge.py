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
	mainParser.add_argument('file', type=str, nargs='+')
	mainParser.add_argument('-s',"--sep",  help="this program can infer separator automatically, but it may fail. Use auto if the input tables contain different separators.",default="auto")
	mainParser.add_argument("--index_col",  help="which col to use as index",default=0,type=int)
	mainParser.add_argument("--rename_index_by_folder",  help="<-5 will be inactive",default=-9,type=int)
	mainParser.add_argument("--glob",  help="glob the current dir with file name match to given string",default="None")
	mainParser.add_argument("--header_list",  help="sep by , define your own colum names",default="None")
	mainParser.add_argument("--drop",  help="try drop this column(s), seperated by ,",default="None")
	mainParser.add_argument("--name_col_with_filename",default="None")
	mainParser.add_argument("--rename_col_with_filename", action='store_true')
	mainParser.add_argument("--by_row", action='store_true')
	mainParser.add_argument("--index", action='store_true')
	mainParser.add_argument("--fillna", default=None)
	
	mainParser.add_argument("--intersection",  help="merge dataframes only on overlapping row names",action='store_true')
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
				
	
def parse_df(x,args):
	sep = args.sep
	error_flag=False
	if sep =="auto":
		error_flag = True
		sep=guess_sep(x)
		args.sep = sep
	if args.header_list == "None":
		if args.index_col==0:
			df = pd.read_csv(x,sep=sep,index_col=0)
		elif args.index_col==-1:
			df = pd.read_csv(x,sep=sep)
		else:
			df = pd.read_csv(x,sep=sep)
			df = df.set_index(df.columns[args.index_col])	
	else:
		if args.index_col==0:
			df = pd.read_csv(x,sep=sep,index_col=0,header=None)
		elif args.index_col==-1:
			df = pd.read_csv(x,sep=sep,header=None)
		else:
			df = pd.read_csv(x,sep=sep,header=None)
			df = df.set_index(df.columns[args.index_col])	
		# print (df.head())
		# print (args.header_list)
		# print (df.head())
		# df.columns = args.header_list.split(",") # 7/2/2021, causing error, why do I have it here?
			
	print ("%s shape: %s X %s"%(x,df.shape[0],df.shape[1]))
	# print (df.head())
	dup_df = df[df.index.duplicated()]
	if dup_df.shape[0]>0:
		print ("%s contains %s number of duplicated index, which are removed from this analysis"%(x,dup_df.shape[0]))
		print (df.loc[dup_df.index.tolist()].head(n=20))
		print ("-------- see duplicated rows above ---------")
		df = df[~df.index.duplicated()]
	is_null = df.isnull().any().any()
	if is_null:
		print ("%s contain NaN values!"%(x))
		if error_flag:
			print ("This could be caused by incorrect separator.")
		else:
			print ("If you are not aware of it, please double-check your input data.")
			
	if args.drop != "None":
		drop_columns = args.drop.split(",")
		try:
			df = df.drop(drop_columns,axis=1)
		except:
			pass
	if args.rename_col_with_filename:
		df.columns = ["%s_%s"%(x,c) for c in df.columns]
	if args.name_col_with_filename != "None":
		df[x] = df[args.name_col_with_filename]
		df = df.drop([args.name_col_with_filename],axis=1)
	# print (df.head())
	if args.rename_index_by_folder>=-5:
		df.index = [x.split("/")[args.rename_index_by_folder]] * df.shape[0]
	return df

def main():

	args = my_args()
	print (args)
	if args.glob != "None":
		files = glob.glob("%s"%(args.glob))
		print (files)
		df_list = [parse_df(x,args) for x in files]
	else:
		print (args.file)
		df_list = [parse_df(x,args) for x in args.file]
	if args.intersection: # default by col
		df = pd.concat(df_list,join="inner",axis=1)
	elif args.by_row:
		df = pd.concat(df_list)
	else:
		df = pd.concat(df_list,axis=1)
	is_null = df.isnull().any().any()
	if is_null:
		print ("%s contain NaN values!"%("Merged table"))
	print ("%s shape: %s X %s"%("Merged table",df.shape[0],df.shape[1]))
	try:
		df.columns = args.header_list.split(",")
	except:
		pass
	if args.fillna:
		for c in args.fillna.split(","):
			df[c] = df[c].fillna(0)
	if args.sep=="\\t":
		args.sep="\t"
	if args.index_col == -1:
		df.to_csv(args.output,sep=args.sep,index=False)
	else:
		df.to_csv(args.output,sep=args.sep)
	print ("Output to table: %s"%(args.output))
if __name__ == "__main__":
	main()


















































