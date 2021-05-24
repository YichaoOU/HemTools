#!/hpcf/apps/python/install/2.7.13/bin/python

import pandas as pd
import sys
import matplotlib
matplotlib.use('agg')
import os
import matplotlib as mpl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import argparse
import datetime
import getpass
import uuid
from scipy.interpolate import interp1d
import re, string
from matplotlib_venn import venn2
import subprocess
def wccount(filename):
	df = pd.read_csv(filename,sep="\t",header=None)
	df['name'] = df[0]+":"+df[1].astype(str)+"-"+df[2].astype(str)
	df = df.drop_duplicates("name")
	# out = subprocess.Popen(['wc', '-l', filename],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
	return df.shape[0]
def send_email(attachments):
	username = getpass.getuser()
	command = ' echo "{{message}}" | mailx {{attachments}} -s "{{subject}}" -- User_name@stjude.org '
	command = command.replace("{{message}}","two bed file venn"+"\n\nYour result is located at:\n"+os.getcwd())
	command = command.replace("{{subject}}","two bed file venn")
	command = command.replace("User_name",username)
	real_attachments = []
	for item in attachments:
		if os.path.isfile(item):
			real_attachments.append(item)
	attachments_string = map(lambda x: '-a "'+x+'" ',real_attachments)
	command = command.replace("{{attachments}}","".join(attachments_string))
	os.system(command)
	# print command
	
	
def my_args():
	username = getpass.getuser()
	
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument("-b1",help="bed file 1",required=True)	
	mainParser.add_argument("-b2",help="bed file 2",required=True)	
	mainParser.add_argument("-l1",help="label 1",required=True)	
	mainParser.add_argument("-l2",help="label 2",required=True)	
	mainParser.add_argument("-e1",help="extend b1 bed file by e1 bp",default=None,type=int)	
	mainParser.add_argument("-e2",help="extend b2 bed file by e2 bp",default=None,type=int)	
	mainParser.add_argument("--fontsize",help="label 2",default=10,type=int)	
	mainParser.add_argument('-o',"--output",  help="output file name",default=username+"_"+str(datetime.date.today()))

	## https://stackoverflow.com/questions/21168120/python-argparse-errors-with-in-help-string
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def extend_bed(bed_file,extend):
	df = pd.read_csv(bed_file,sep="\t",header=None)
	# df[1] = df[1].astype(int)-extend
	df[1] = [max(0,int(x)-extend) for x in df[1]]
	df[2] = df[2].astype(int)+extend
	# df[df < 0] = 0
	outfile = str(uuid.uuid4()).split("-")[-1]
	df[[0,1,2]].to_csv(outfile,sep="\t",header=False,index=False)
	return outfile
	

def main():
	args = my_args()
	outFile = "%s.overlap.bed"%(args.output)
	if args.e1:
		args.b1 = extend_bed(args.b1,args.e1)
	if args.e2:
		args.b2 = extend_bed(args.b2,args.e2)
	
	command = "module load bedtools;bedtools intersect -a %s -b %s -u > %s"%(args.b1,args.b2,outFile)
	os.system(command)
	F1 = wccount(args.b1)
	F2 = wccount(args.b2)
	out = wccount(outFile)
	
	print "A: Number of lines in %s: %s"%(args.b1,F1)
	print "B: Number of lines in %s: %s"%(args.b2,F2)
	print "Number of overlaps: %s"%(out)
	plt.rcParams.update({'font.size': args.fontsize})
	venn2( (F1-out, max(F2-out,0), out),(args.l1,args.l2))
	plt.savefig("%s.bed2venn.pdf"%(args.output), bbox_inches='tight')	
	send_email(["%s.bed2venn.pdf"%(args.output)])
	if args.e1:
		os.system("rm %s"%(args.e1))
	if args.e2:
		os.system("rm %s"%(args.e2))
	
	


if __name__ == "__main__":
	main()



