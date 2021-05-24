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
	mainParser.add_argument('-f','--input',  help="input data table, tsv with column names", required=True)
	mainParser.add_argument('--use_col',  help="which column to use to extract unique items", required=True)
	mainParser.add_argument('-o','--output',  help="output file name",default="unique_items.list")
	
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

def unique_items(x):
	return [i.replace("['","").replace("']","").replace(" ","").replace("'","") for i in x.split(",")]

def main():

	args = my_args()
	df = pd.read_csv(args.input,sep="\t")
	myList = [unique_items(x) for x in df[args.use_col].tolist()]
	flat_list = [item for sublist in myList for item in sublist]
	flat_list = list(set(flat_list))

	write_file(args.output,"\n".join(flat_list))
if __name__ == "__main__":
	main()


















































