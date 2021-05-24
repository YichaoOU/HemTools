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

Usage:

1. given one or more bed files, extract average signal for each bw file (basic)


2. given one or more bed files, extract average signal for each bw file for each sliding window


3. given one or more bed files, extract single base signal for each bw file


module load ucsc/041619


"""


def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('--bw_files',  help="input a list of bw files, use * to indicate all bw files in the current dir", default="*")
	mainParser.add_argument('--bed_files',  help="input a list of bed/Peak files, use * to indicate all bed/Peak files in the current dir", default="*" )
	mainParser.add_argument('--extend',  help="extend bed file", type=int,default=0 )
	mainParser.add_argument('-o',"--output",  help="output prefix",default=username+"_"+str(datetime.date.today())+"_"+addon_string+".averageBW")
	

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def clean_bed(x,extend):
	addon_string = str(uuid.uuid4()).split("-")[-1]
	output = x.split("/")[-1]+".bed4.%s"%(addon_string)
	
	if extend == 0:
		command = """awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$1":"$2"-"$3}' %s > %s"""%(x,output)
	else:
		command = """awk -F "\t" '{print $1"\t"$2-%s"\t"$3+%s"\t"$1":"$2"-"$3}' %s > %s"""%(extend,extend,x,output)
	
	os.system(command)
	# os.system("head %s"%(output))
	df = pd.read_csv(output,sep="\t",header=None)
	df = df.drop_duplicates(3)
	df = df.dropna()
	df[1] = df[1].astype(int)
	df[2] = df[2].astype(int)
	# df = df.astype(str)
	# print (df)
	df.to_csv(output,sep="\t",header=False,index=False)
	return output

def run_bigWigAverageOverBed(bed,bw):
	addon_string = str(uuid.uuid4()).split("-")[-1]
	out = bed+"-bwOverBed-%s-"%(addon_string)+bw.split("/")[-1]+".out"
	command = "bigWigAverageOverBed %s %s %s"%(bw,bed,out)
	os.system(command)
	return out

def parse_df(x):
	df = pd.read_csv(x,sep="\t",header=None,index_col=0)
	name = x.split("-bwOverBed-")[-1].replace(".bw","").replace(".rmdup","").replace(".uq","").replace(".out","").replace(".bdg","").replace("_FE","")
	# print (name)
	col_names = df.columns.tolist()
	col_names[-2] = name
	df.columns = col_names
	return df[name]

def summary_output(outfile,file_list):
	df = pd.concat([parse_df(x) for x in file_list],axis=1)
	df.to_csv(outfile)

def main():


	args = my_args()
	
	if args.bed_files == "*":
		bed_files = glob.glob("*.bed")+glob.glob("*.Peak")
	else:
		bed_files = glob.glob("%s"%(args.bed_files))
	bed_files = [clean_bed(x,args.extend) for x in bed_files ]
	
	if args.bw_files == "*":
		bw_files = glob.glob("*.bw")+glob.glob("*.bigWig")
	else:
		bw_files = glob.glob("%s"%(args.bw_files))

	# print (bw_files)
	for i in bed_files:
		print ("Processing bed file: %s"%(i))
		output_files = []
		for j in bw_files:
			out = run_bigWigAverageOverBed(i,j)
			output_files.append(out)
		os.system("rm %s"%(i))
		### main ####
		summary_output("%s%s.csv"%(i.replace(".bed4",""),args.output),output_files)
		for x in output_files:
			os.system("rm %s"%(x))

if __name__ == "__main__":
	main()
















