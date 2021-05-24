#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os

import datetime
import getpass
import uuid
import argparse
"""
Given a main table, and any number of query tables, add columns to the main
table using the query tables, by default, all columns in a query are added,
User can specify which column to add.

main table and query table should have a column used to match index

"""
def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--main_table",  help="data table input",required=True)
	mainParser.add_argument('file', type=str, nargs='+')
	mainParser.add_argument("--header",  help="input table has header", action='store_true')
	mainParser.add_argument('-s',"--sep",  help="separator, for output, input sep is either tab or comma, will be automatically determined",default="\t")
	mainParser.add_argument('-i',"--main_index_col",  help="index_col for the main table",required=True)
	mainParser.add_argument("--query_index_col",  help="index_col for the query table(s)",default=None)
	mainParser.add_argument("--query_header",  help="A list of 1 or 0, e.g, 1,1,0; 1: has header. 0: no header",default=None)
	mainParser.add_argument("--query_add_col",  help="A list of column names to be add, LFC:FDR,0,",default=None)
	mainParser.add_argument('-o',"--output",  help="output table name",default=username+"_add_columns_"+str(datetime.date.today())+"_"+addon_string+".tsv")
	
	
	
	


	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def read_data(file, header,index_col):
	if header:
		df = pd.read_csv(file,sep=guess_sep(file))
	else:
		index_col = int(index_col)
		df = pd.read_csv(file,sep=guess_sep(file),header=None)
	df.index = df[index_col].tolist()	
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

def main():

	args = my_args()
	global pd
	import pandas as pd
	# read main table
	df_main = read_data(args.main_table, args.header,args.main_index_col)

	
	# read query tables
	q_index = args.query_index_col.split(",")
	q_header = args.query_header.split(",")
	q_add = args.query_add_col.split(",")
	for i in range(len(args.file)):
		
		file = args.file[i]
		print (file)
		if q_header[i]=="1":
			header = True
		else:
			header = False
		# print (q_header,header,q_add)
		index = q_index[i]
		df = read_data(file, header,index)
		df.index.name = "query"
		for c in q_add[i].split(":"):
			if not header:
				c = int(c)
			temp = pd.DataFrame(df.groupby('query')[c].apply(lambda x:",".join([str(j) for j in x])))
			df_main["%s_%s"%(file,c)] = temp[c]
	
	

	if args.sep=="\\t":
		args.sep="\t"
	#-------------- output ----------------------

	df_main.to_csv(args.output,sep=args.sep,index=False)
if __name__ == "__main__":
	main()


















































