#!/usr/bin/env python





import subprocess
import os
import pandas as pd
import glob

def overlap_count(TF,ATAC):
	command1 = "cat %s | wc -l"%(TF)
	# command1 = ["wc","-l",TF]
	total = subprocess.Popen(command1,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
	command2 = "bedtools intersect -a %s -b %s -u | wc -l "%(TF,ATAC)
	overlap = subprocess.Popen(command2,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
	return total.strip(),overlap.strip()
	

files = glob.glob("*.bed")+glob.glob("*Peak")+glob.glob("*peak")
ATAC_list = []
TF_list = []
for f in files:
	if "ATAC" in f.upper():
		ATAC_list.append(f)
	elif "DNASE" in f.upper():
		ATAC_list.append(f)
	else:
		TF_list.append(f)
print ("------------------ATAC----------------")
print (ATAC_list)
print ("------------------TF----------------")
print (TF_list)
lines = []
for TF in TF_list:
	for ATAC in ATAC_list:
		total,overlap = overlap_count(TF,ATAC)
		lines.append([TF,ATAC,int(total),int(overlap)])
		# print (lines)
		# exit()
df = pd.DataFrame(lines)
df.columns = ['TF','ATAC/DNase',"Total TF peaks","Open TF peaks"]
df.to_csv("summary_overlap.csv",index=False)
