#!/usr/bin/env python

import os

# os.system("module load bedtools;bedtools intersect -a OUT.extended_annotation.bed12 -b /home/yli11/Data/Human/hg38/annotations/BCL11A.bed -u | cut -f 4 > BCL11A.novel.list")
os.system("cp /home/yli11/dirs/MBNL1_Project_all_data_needed/yichao/bam_all/bam_remove_mono_exon/isoquant_bam_yli11_2025-04-18_isoQuant_isoseq_default_pacbio/OUT/BCL11A.novel.list BCL11A.novel.list")
os.system("cp /home/yli11/dirs/MBNL1_Project_all_data_needed/yichao/bam_all/bam_remove_mono_exon/isoquant_bam_yli11_2025-04-18_isoQuant_isoseq_default_pacbio/OUT/OUT.extended_annotation.gtf OUT.extended_annotation.gtf")
os.system("grep -f BCL11A.novel.list OUT.extended_annotation.gtf > BCL11A.novel.gtf")
# os.system("grep -f BCL11A.novel.list OUT.transcript_model_reads.tsv > BCL11A.transcript_model_reads.tsv")
os.system("grep -f BCL11A.novel.list OUT.read_assignments.tsv > BCL11A.read_assignments.tsv")
os.system("grep -f BCL11A.novel.list OUT.transcript_model_grouped_tpm.tsv > BCL111A.transcript_model_grouped_tpm.tsv")
os.system("head -n 1 OUT.transcript_model_grouped_tpm.tsv > header")
os.system("cat header BCL111A.transcript_model_grouped_tpm.tsv > BCL111A.transcript_model_grouped_tpm.add_header.tsv")
os.system("grep -f BCL11A.novel.list OUT.transcript_grouped_tpm.tsv > BCL111A.transcript_grouped_tpm.tsv;head -n 1 OUT.transcript_grouped_tpm.tsv > header;cat header BCL111A.transcript_grouped_tpm.tsv > BCL111A.transcript_grouped_tpm.add_header.tsv")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# df = pd.read_csv("BCL111A.transcript_grouped_tpm.add_header.tsv",sep="\t",index_col=0)
# df.columns = ["_".join(x.split("_")[:-3]) for x in df.columns]
# df = df[df.max(axis=1)>=1]
# df = df.transform(lambda x:np.log2(x+1))
# sns.clustermap(df,cmap="viridis",figsize=(6,8),yticklabels=True)
# plt.savefig("BCL111A.transcript_grouped_tpm.add_header.png",bbox_inches='tight')

df = pd.read_csv("BCL111A.transcript_grouped_tpm.add_header.tsv",sep="\t",index_col=0)
df = df.transform(lambda x:np.log2(x+1))
tequila_cols =[]
isoseq_cols=[]
for c in df.columns:
    if "Nanopore" in c or "Pacbio" in c:
        tequila_cols.append(c)
    else:
        isoseq_cols.append(c)
sns.clustermap(df[df[tequila_cols].max(axis=1)>2][tequila_cols],cmap="viridis",figsize=(6,10),yticklabels=True)
plt.savefig("BCL111A.tequila.png",bbox_inches='tight')

sns.clustermap(df[df[isoseq_cols].max(axis=1)>0.5][isoseq_cols],cmap="viridis",figsize=(8,9),yticklabels=True,xticklabels=True)
plt.savefig("BCL111A.ISOseq.png",bbox_inches='tight')


