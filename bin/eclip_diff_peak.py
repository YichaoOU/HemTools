#!/usr/bin/env python


import os
import sys
import string
import pandas as pd
## inside the jobID folder, run the following

wt=sys.argv[1]
ko=sys.argv[2]
input=sys.argv[3]
print ("Input is:",wt,ko,input)
src="/home/yli11/Programs/merge_peaks/bin/perl"

step1 = """
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

step2 = """
samtools view -F 260 -b $t*/$t.bam > $t.pri.bam
samtools index $t.pri.bam
samtools view -F 260 -b $c*/$c.bam > $c.pri.bam
samtools index $c.pri.bam
samtools view -c $t.pri.bam > $t.readnum.txt
samtools view -c $c.pri.bam > $c.readnum.txt
perl $src/overlap_peakfi_with_bam.pl $t.pri.bam $c.pri.bam $t.merged.bed $t.readnum.txt $c.readnum.txt $t.enriched_peak.final.bed
rm $t.pri.bam*
rm $c.pri.bam*
#rm $t.readnum.txt
#rm $c.readnum.txt

# rm $t.enriched_peak.final.bed.full
rm $t.merged.bed
"""

def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()


# WT vs input
step1 = step1.replace("$t",wt)
step1 = step1.replace("$c",input)
step1 = step1.replace("$src",src)
write_file("tmp.sh",step1)
os.system("module load R/3.5.1-rh7;bash tmp.sh")

# filter peak
df = pd.read_csv(f"{wt}.vs.{input}.bed",sep="\t",header=None)
# df = df[(df[3]>=2)&(df[4]>1)]
df = df[(df[3]>=0)&(df[4]>1)]
print (df.shape)
df.to_csv(f"{wt}.enriched_peak.bed",sep="\t",header=False,index=False)
os.system(f"merge_bed.py {wt}.enriched_peak.bed --keep_info -o {wt}.merged.bed;rm {wt}.enriched_peak.bed")


# WT vs input, vs KO
step2 = step2.replace("$t",wt)
step2 = step2.replace("$c",ko)
step2 = step2.replace("$src",src)
write_file("tmp.sh",step2)
os.system("module load R/3.5.1-rh7;bash tmp.sh")


# filter peak
df = pd.read_csv(f"{wt}.enriched_peak.final.bed",sep="\t",header=None)
# df = df[(df[3]>=2)&(df[4]>1)]
df = df[(df[3]>=0)&(df[4]>1)]
print (df.shape)
df = df.sort_values(4,ascending=False)
os.system(f"mv {wt}.enriched_peak.final.bed {wt}.enriched_peak.final.tmp.bed")
df.to_csv(f"{wt}.enriched_peak.final.bed",sep="\t",header=False,index=False)

os.system("rm tmp.sh")
