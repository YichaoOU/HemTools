#!/usr/bin/env python
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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="merge bedfiles into one")
	mainParser.add_argument('file', type=str, nargs='+')
	mainParser.add_argument('-o',"--output",  help="output table name",default=username+"_"+str(datetime.date.today())+"_"+addon_string+".bed")

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	input_files = " ".join(args.file)
	# os.system("module load bedtools; cat %s | sort -k1,1 -k2,2n - | bedtools merge -i - > %s"%(input_files,args.output))
	os.system("module load bedtools; cat %s |cut -f 1,2,3| sort -k1,1 -k2,2n - | bedtools merge -i - > %s"%(input_files,args.output))

if __name__ == "__main__":
	main()


















































