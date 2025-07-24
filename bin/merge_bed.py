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
	mainParser.add_argument('-e',"--extend",  help="get peak center and extend by",default=0,type=int)
	mainParser.add_argument('--cut3',  help="only use first 3 columns", action='store_true')
	mainParser.add_argument('--keep_info',  help="merge a bed6 file and randomly keep 4,5,6 columns if there is overlap", action='store_true')

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	input_files = " ".join(args.file)
	# os.system("module load bedtools; cat %s | sort -k1,1 -k2,2n - | bedtools merge -i - > %s"%(input_files,args.output))
	# os.system("module load bedtools; cat %s |cut -f 1,2,3| sort -k1,1 -k2,2n - | bedtools merge -i - > %s"%(input_files,args.output))
	if args.extend > 0:
		if args.cut3:
			os.system("module load bedtools; cat %s | sort -k1,1 -k2,2n - |cut -f 1,2,3 | bedtools merge -i - | awk -vOFS='\t' -vEXT=%s 'width=$3-$2 {if(width %% 2 != 0) {width+=1} ; mid=$2+width/2; print $1,mid-EXT,mid+EXT}' - > %s"%(input_files,args.extend,args.output))
		elif args.keep_info:
			os.system("module load bedtools; cat {0} | sort -k1,1 -k2,2n - |cut -f 1,2,3 | bedtools merge -i - > {1}.tmp;bedtools intersect -a {0} -b {1}.tmp -wa -wb > {1}.tmp.tmp".format(input_files,args.output))
			df = pd.read_csv("%s.tmp.tmp"%(args.output),sep="\t",header=None)
			df = df.drop_duplicates([6,7,8])
			df = df[[0,1,2,3,4,5]]
			df['mid'] = (df[2]-df[1])/2
			df['mid'] = df['mid'].astype(int)
			df[1] = df['mid']-args.extend
			df[2] = df['mid']+args.extend
			df[[0,1,2,3,4,5]].to_csv(args.output,sep="\t",header=False,index=False)
			os.system("rm %s.tmp*"%(args.output))
		else:
			command = "module load bedtools; cat %s | sort -k1,1 -k2,2n - | bedtools merge -i - | awk -vOFS='\t' -vEXT=%s 'width=$3-$2 {if(width %% 2 != 0) {width+=1} ; mid=$2+width/2; print $1,mid-EXT,mid+EXT}' - > %s"%(input_files,args.extend,args.output)
			print (command)
			os.system(command)
	else:
		if args.cut3:
			os.system("module load bedtools; cat %s | sort -k1,1 -k2,2n - |cut -f 1,2,3 | bedtools merge -i - > %s"%(input_files,args.output))
		elif args.keep_info:
			os.system("module load bedtools; cat {0} | sort -k1,1 -k2,2n - |cut -f 1,2,3 | bedtools merge -i - > {1}.tmp;bedtools intersect -a {0} -b {1}.tmp -wa -wb > {1}.tmp.tmp".format(input_files,args.output))
			df = pd.read_csv("%s.tmp.tmp"%(args.output),sep="\t",header=None)
			df = df.drop_duplicates([6,7,8])
			df = df[[0,1,2,3,4,5]]
			df.to_csv(args.output,sep="\t",header=False,index=False)
			os.system("rm %s.tmp*"%(args.output))
		else:
			os.system("module load bedtools; cat %s | sort -k1,1 -k2,2n - | bedtools merge -i - > %s"%(input_files,args.output))

if __name__ == "__main__":
	main()


















































