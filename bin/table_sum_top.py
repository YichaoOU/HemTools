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



def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="merge input dataframes by rows")
	mainParser.add_argument('-f',"--input",  help="input table name",required=True)


	mainParser.add_argument("-p",'--percent',  help="show as percent",action='store_true')
	mainParser.add_argument("-a",'--ascending',  help="ascending = True",action='store_true')

	mainParser.add_argument('-o',"--output",  help="output table name",default=username+"_"+str(datetime.date.today())+"_"+addon_string+".tsv")
	mainParser.add_argument('-n',"--num",  help="how many top to show",default=50,type=int)
	mainParser.add_argument('-i',"--index",  help="index by sep by ,",default=None)



	
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

	df = pd.read_csv(args.input,sep=guess_sep(args.input))
	if args.index:
		index_by = args.index.split(",")
		df = df.set_index(index_by)
	if args.percent:
		df.sum(axis=1).sort_values(ascending=args.ascending).divide(df.sum().sum()).head(n=args.num).to_csv(args.output,sep="\t",header=False)
	else:
		df.sum(axis=1).sort_values(ascending=args.ascending).head(n=args.num).to_csv(args.output,sep="\t",header=False)
	
	
if __name__ == "__main__":
	main()







