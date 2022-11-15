#!/usr/bin/env python

import os
import sys

peaks = sys.argv[1]
tad = sys.argv[2]
gtf = sys.argv[3]
cap = sys.argv[4]

TAD_command="bed_TAD_gene.py %s %s %s"%(peaks,tad,gtf)

nearest_gene_command="module load homer/4.10;annotatePeaks.pl %s mm9 -gtf %s > %s.annot.txt"%(peaks,gtf,peaks)

captureC_command = "bed_Capture_gene.py %s %s"%(peaks,cap)

os.system(TAD_command)
os.system(captureC_command)
os.system(nearest_gene_command)

command = 'sed "1d" %s.annot.txt | cut -f 16 > %s.list1'%(peaks,peaks)
os.system(command)
command = 'cat %s.TAD.gene.bed | cut -f 4 > %s.list2'%(peaks,peaks)
os.system(command)
command = 'cat %s.capC.gene.bed | cut -f 5 > %s.list3'%(peaks,peaks)
os.system(command)

# command = "cat {0}.list1 {0}.list2 {0}.list3 > {0}.target.list".format(peaks)
command = "cat {0}.list1 {0}.list3 > {0}.target.list".format(peaks)
os.system(command)
# filter by DEG

import pandas as pd
deg = sys.argv[5]
df = pd.read_csv(deg,sep="\t")
total_list = pd.read_csv("%s.target.list"%(peaks),header=None)
overlap = set(df.index).intersection(total_list[0])
df = df.loc[overlap]
df.to_csv("%s.direct_targets.rmTAD.tsv"%(deg.split("/")[-1]),sep="\t")

# get_target_gene_list.py STHSC.06.peaks.bed GSE119347_BMHSC_TADs.bed.gz Mus_musculus.mm10_mm9.93.filtered.gtf target.bed ClusterST-HSC.2.DEG.orig.ident.logFC02.FDR001.tsv


command = "cat {0}.list1 {0}.list2 {0}.list3 > {0}.target2.list".format(peaks)
os.system(command)
# filter by DEG

import pandas as pd
# deg = sys.argv[5]
df = pd.read_csv(deg,sep="\t")
total_list = pd.read_csv("%s.target2.list"%(peaks),header=None)
overlap = set(df.index).intersection(total_list[0])
df = df.loc[overlap]
df.to_csv("%s.direct_targets.all.tsv"%(deg.split("/")[-1]),sep="\t")


os.system("rm {0}.list1 {0}.list2 {0}.list3".format(peaks))
