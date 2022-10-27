#!/usr/bin/env python


import os
import sys
import string
import pandas as pd
from copy import deepcopy as dp
## inside the jobID folder, run the following

wt=sys.argv[1]
wt_input=sys.argv[2]
ko=sys.argv[3]
ko_input=sys.argv[4]

print ("Input is:",wt,ko,input)
src="/home/yli11/Programs/merge_peaks/bin/perl"

template = """
samtools view -F 260 -b $t*/$t.bam > $t.pri.bam
samtools index $t.pri.bam
samtools view -F 260 -b $c*/$c.bam > $c.pri.bam
samtools index $c.pri.bam
samtools view -c $t.pri.bam > $t.readnum.txt
samtools view -c $c.pri.bam > $c.readnum.txt
perl $src/overlap_peakfi_with_bam.pl $t.pri.bam $c.pri.bam $t*/$t.bed $t.readnum.txt $c.readnum.txt $t.vs.$c.bed
rm $t.pri.bam*
rm $c.pri.bam*
rm $t.readnum.txt
rm $c.readnum.txt
rm $t.vs.$c.bed.full
"""


def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()


# WT vs input
step1 = dp(template)
step1 = step1.replace("$t",wt)
step1 = step1.replace("$c",wt_input)
step1 = step1.replace("$src",src)
write_file("tmp.sh",step1)
os.system("module load R/3.5.1-rh7;bash tmp.sh")

# filter peak
df = pd.read_csv(f"{wt}.vs.{wt_input}.bed",sep="\t",header=None)
df = df[(df[3]>=2)&(df[4]>2)]
print (df.shape)
df.to_csv(f"{wt}.enriched_peak.bed",sep="\t",header=False,index=False)

# KO vs input
step2 = dp(template)
step2 = step2.replace("$t",ko)
step2 = step2.replace("$c",ko_input)
step2 = step2.replace("$src",src)
write_file("tmp.sh",step2)
os.system("module load R/3.5.1-rh7;bash tmp.sh")

# filter peak
df = pd.read_csv(f"{ko}.vs.{ko_input}.bed",sep="\t",header=None)
df = df[(df[3]>=2)&(df[4]>2)]
print (df.shape)
df.to_csv(f"{ko}.enriched_peak.bed",sep="\t",header=False,index=False)

os.system(f"rm tmp.sh;module load bedtools;bedtools intersect -a {wt}.enriched_peak.bed -b {ko}.enriched_peak.bed -v > {wt}.vs.{ko}.final.bed")
os.system(f"merge_bed.py {wt}.vs.{ko}.final.bed --keep_info -o {wt}.final.bed;rm {wt}.vs.{ko}.final.bed")


