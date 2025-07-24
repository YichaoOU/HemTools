#!/usr/bin/env python

import pandas as pd
import sys
import os
import argparse
import glob

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output", help="output file", default="merged.bed")
	mainParser.add_argument('-e',"--file_extension", help="output file", default="merged.bed")


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def read_bed(f):
	print ("Reading: %s"%(f))
	df = pd.read_csv(f,sep="\t",header=None)
	df[1] = df[1].astype(int)
	df[2] = df[2].astype(int)
	return df[[0,1,2]]

def main():

	args = my_args()
	df_list = [read_bed(f) for f in glob.glob(f"*{args.file_extension}")]
	df = pd.concat(df_list)
	df[1] = [int(max(0,x-50)) for x in df[1]]
	df[2] = [int(x+50) for x in df[2]]
	df = df.sort_values([0,1])
	df.to_csv("tmp.bed",sep="\t",header=False,index=False)
	command = f"module load bedtools;bedtools merge -i tmp.bed > tmp2.bed"
	os.system(command)
	df = read_bed("tmp2.bed")
	df[3] = df[1]/2+df[2]/2
	# print(df.head())
	df[1] = [int(max(0,x-100)) for x in df[3]]
	df[2] = [x+200 for x in df[1]]
	df[3] = df[0]+":"+df[1].astype(str)+"-"+df[2].astype(str)
	df[[0,1,2]].to_csv("tmp2.bed",sep="\t",header=False,index=False)
	command = f"module load bedtools;bedtools merge -i tmp2.bed > tmp3.bed"
	os.system(command)
	df = read_bed("tmp3.bed")
	df[3] = df[0]+":"+df[1].astype(str)+"-"+df[2].astype(str)
	df.to_csv(args.output,sep="\t",header=False,index=False)
	os.system("rm tmp.bed;rm tmp2.bed;rm tmp3.bed")



if __name__ == "__main__":
	main()


















