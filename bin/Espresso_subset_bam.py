#!/usr/bin/env python

import pandas as pd
import numpy as np
import scipy.stats as sts
from Levenshtein import distance

import gzip as gz
import pysam
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
import glob
from joblib import Parallel, delayed
import sys
import argparse
import plotly.express as px
import plotly.io as pio
import os
from Bio.Seq import Seq
from Bio import SeqIO
import swifter
import sys
import plotly.express as px


# Espresso_dir = sys.argv[1]
label = sys.argv[1]

exp = pd.read_csv(f"{label}_espresso_result/sample_N2_R0_abundance.esp",sep="\t")
rList = pd.read_csv(f"{label}_espresso_result/{label}_isoform.tsv",sep="\t",header=None)
rList[3] = rList[3].fillna("")

# get annotation overlapped with BCL11A
command = f"""
module load ucsc/051223
gtfToGenePred {label}_espresso_result/sample_N2_R0_updated.gtf {label}_espresso_result/sample_N2_R0_updated.genePred
genePredToBed {label}_espresso_result/sample_N2_R0_updated.genePred {label}_espresso_result/sample_N2_R0_updated.bed12
bedtools intersect -a {label}_espresso_result/sample_N2_R0_updated.bed12 -b /home/yli11/HemTools/share/misc/BCL11A.hg38.bed -u | cut -f 4 > {label}_espresso_result/BCL11A.isoform.list
"""
os.system(command)
# generate read list
isoform_list = pd.read_csv(f"{label}_espresso_result/BCL11A.isoform.list",header=None)[0].tolist()
os.system("mkdir -p Espresso_isoform_bam")
for i in isoform_list:
	if not "ENST" in i:
		continue
	tmp = rList[rList[3].str.contains(i)]
	tmp[0].to_csv(f"{label}_espresso_result/{i}.read.list",header=False,index=False)
	command = f"module load picard/2.9.4 samtools/1.7;java -jar /hpcf/apps/picard/install/2.9.4/picard.jar FilterSamReads I={label}.Aligned.out.st.bam O=Espresso_isoform_bam/{label}.{i}.bam READ_LIST_FILE={label}_espresso_result/{i}.read.list FILTER=includeReadList;samtools index Espresso_isoform_bam/{label}.{i}.bam"
	os.system(command)
	# print (command)
