#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
# import pandas as pd
import datetime
import getpass
import uuid
import argparse
import glob
import re
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
	mainParser.add_argument('--run',  help="perform the actual merge fastq", action='store_true')

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
def define_fastq_label(x):
	lanes = ['L001','L002','L003','L004','L005','L006','L007','L008']
	for i in lanes:
		x = x.replace("%s_"%(i),"")
	return x.split("/")[-1]


def is_lane(x,y):
	lanes = ['L001','L002','L003','L004','L005','L006','L007','L008']
	items1 = re.split("_|-|\.",x)
	items2 = re.split("_|-|\.",y)
	num_diff = 0
	lane_diff = False
	if len(items2) != len(items1):
		return False
	for i in range(len(items1)):
		if items1[i] != items2[i]:
			num_diff+=1
			if items1[i] in lanes and items2[i] in lanes:
				lane_diff = True
	if lane_diff and num_diff==1:
		return True
	return False

def output_bash(groups,flag):
	for i in groups:
		command = "cat "+" ".join(groups[i]) + " > "+define_fastq_label(i)
		print command
		if flag:
			os.system(command)
	
def main():

	args = my_args()
	groups = {}
	used = []
	# print (args.file)
	for i in args.file:
		if i in used:
			continue
		groups[i] = [i]
		for j in args.file:
			if is_lane(i,j):
				groups[i].append(j)
				used.append(j)
	output_bash(groups,args.run)
			

if __name__ == "__main__":
	main()


















































