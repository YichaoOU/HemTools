#!/usr/bin/env python

import sys
import pandas as pd
import glob
import os


GeneName=sys.argv[1]
PAM=sys.argv[2]
ATG_dict=eval(sys.argv[3])
geneInfo = pd.read_csv("/home/yli11/Data/Human/hg38/annotations/gencode_info.bed",sep="\t",header=None)
geneInfo['Name'] = geneInfo[2].apply(lambda x:x.split("-")[0])
geneInfo = geneInfo[geneInfo['Name']==GeneName]
TX = [x.split(".")[0] for x in geneInfo[1].tolist()]
print ("### Step 1: Extract transcript ID Finished")
print (TX)

def read_exon_bed(f):
    df = pd.read_csv(f,sep="\t",header=None)
    return df
exon_files = [
'/home/yli11/Data/Human/hg38/annotations/UCSC_table_browser/hg38.3UTR.bed.gz',
'/home/yli11/Data/Human/hg38/annotations/UCSC_table_browser/hg38.5UTR.bed.gz',
'/home/yli11/Data/Human/hg38/annotations/UCSC_table_browser/hg38.exon.bed.gz',
]
df = pd.concat([read_exon_bed(f) for f in exon_files])
df[6] = [x.split("_")[0].split(".")[0] for x in df[3]]
df = df[df[6].isin(TX)]
df = df.drop_duplicates([0,1,2])
df[[0,1,2,3,4,5]].to_csv(f"{GeneName}.exon.bed",sep="\t",header=False,index=False)
print ("### Step 2: Extract exon bed file Finished")
print (df)


print ("### Step 3: finding all gRNAs, may take some time")

command = f"module load conda3/202011;source activate Cas_Offinder;module load bedtools;find_all_gRNA.py -f {GeneName}.exon.bed -e 20 -n 0 --PAM {PAM} -g /home/yli11/Data/Human/hg38/fasta/hg38.fa"
os.system(command)

gRNA= pd.read_csv("candidate_gRNA.bed",sep="\t",header=None)
print ("ALL gRNA size",gRNA.shape)
occ = pd.read_csv("candidate_gRNA.bed.off_targets.info.csv")
gRNA = gRNA[gRNA[3].isin(occ[occ.numOffTargets==0].seq.tolist())]
print ("### Step 4: sgRNA filtering Finished")
print (gRNA.shape)
gRNA.to_csv("candidate_gRNA.tsv",sep="\t",header=False,index=False)
command = f"get_editable_base_v2.py candidate_gRNA.tsv A 2,3,4,5,6,7 candidate_gRNA.editableA.bed"
os.system(command)
editA = pd.read_csv("candidate_gRNA.editableA.bed",sep="\t",header=None)
for c in ATG_dict:
	gRNA[f'is_{c}_ATG'] = [x in editA[editA[2].isin(ATG_dict[c])][3].tolist() for x in gRNA[3]]
iSTOP_file=sys.argv[4]
iSTOP = pd.read_csv(iSTOP_file)
iSTOP['gRNA'] = iSTOP['sgNG'].str.upper()
gRNA['is_iSTOP'] = [x[:20] in iSTOP['gRNA'].tolist() for x in gRNA[3]]
print (gRNA[gRNA.is_iSTOP==True])
gRNA['gRNA_seq'] = [x[:20] for x in gRNA[3]]
gRNA.columns = ['#chr','start','end','gRNA_PAM_seq','GC%','strand']+gRNA.columns[6:].tolist()
gRNA.to_csv(f"{GeneName}.gRNA.annot.tsv",sep="\t",index=False)


