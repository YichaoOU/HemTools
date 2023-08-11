#!/usr/bin/env python

'''
rename for 10x single cell RNA-seq or ATAC-seq experiments

parse current and subfolders for fastq

output ln -s commands to rename

'''

import pandas as pd
import os
import glob
import sys

def detect_lane(f):
    items = f.split("_")
    for i in range(1,5):
        for j in items:
            if f"L00{i}"==j:
                return j
    return "Failed"
def detect_read_type(f):
    items = f.split("_")
    for i in ['R1','R2','R3','I1','I2']:
        for j in items:
            if i==j:
                return j
    return "Failed"
def rename_fastq(id,label):
    files = glob.glob(f"{id}*gz")+glob.glob(f"*/{id}*gz")
    for f in files:
        lane = detect_lane(f)
        read = detect_read_type(f)
        if lane == read:
            print (f,"is failed to correct name")
            continue
        new_name = f"{label}_S1_{lane}_{read}_001.fastq.gz"
        command = f"ln -s {f} {new_name}"
        print (command)
# df = pd.read_csv("label.tsv",sep="\t",header=None)
"""
2461498	Bt_WT_I 
2461499	Bt_WT_II
2461500	Bt_WT_III
2461501	Bt_WT_IV

"""
df = pd.read_csv(sys.argv[1],sep="\t",header=None)
for i,r in df.iterrows():
    rename_fastq(r[0],r[1])



