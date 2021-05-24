#!/home/yli11/.conda/envs/py2/bin/python

# exec(open("/home/yli11/HemTools/bin/interaction_annotate_gene.py").read())

# py2

import pandas as pd
import os
import numpy as np
import sys
# add gene exp info for OE

# interaction_ibed = "/home/yli11/dirs/20copy_project/captureC/new_data/captureC_analysis/20copy_hg19.called_interactions.tsv"
interaction_ibed = sys.argv[1]
df = pd.read_csv(interaction_ibed,sep="\t")



TSS_bed = "/home/yli11/Data/Human/hg19/annotations/hg19_main.kallisto.ensembl_v75.TSS.st.bed"

# gene_exp = "/home/yli11/dirs/20copy_project/RNAseq/exon_level_comparison/hg19_analysis/20copy_vs_Jurkat.gene.final.combined.tpm.csv"
gene_exp = sys.argv[2]

exp = pd.read_csv(gene_exp)
exp.index = exp['ext_gene'].tolist()

# output = "20copy_hg19.captureC.gene.tsv"
output = sys.argv[3]



distance_cutoff = 10000
# nearest TSS or all genes within 10kb
# 1. other end bed
tmp = df[['chr_OE','start_OE','end_OE','OE_name']].sort_values(['chr_OE','start_OE'])
tmp = tmp.drop_duplicates("OE_name")
tmp.to_csv("other_end.bed",sep="\t",header=False,index=False)

# 2. gene overlaped with other end bed
# os.system("module load bedtools/2.29.2;bedtools closest -a other_end.bed -b %s -d -k 100 -g /home/yli11/Data/Human/hg19/annotations/hg19.chrom.sizes.sorted > other_end_nearest_TSS.bed"%(TSS_bed))
os.system("module load bedtools/2.29.2;bedtools closest -a other_end.bed -b %s -d -k 100 > other_end_nearest_TSS.bed"%(TSS_bed))


annot = pd.read_csv("other_end_nearest_TSS.bed",sep="\t",header=None)
# get_nearest genes
OE_name = []
genes = []
distance = []
for s,d in annot.groupby(3):
	OE_name.append(s)
	current_genes = []
	current_distance = []
	d = d.sort_values(d.columns[-1])
	current_genes.append(d[7].tolist()[0])
	current_distance.append(d[d.columns[-1]].tolist()[0])
	d = d[d[d.columns[-1]]<=distance_cutoff]
	if d.shape[0]>0:
		current_genes+=d[7].tolist()
		current_genes = list(set(current_genes))
		current_distance += d[d.columns[-1]].tolist()
	genes.append(current_genes)
	distance.append(np.max(current_distance))

annot = pd.DataFrame({
"genes":genes,
"distance":distance
})
annot.index = OE_name

pd.set_option('display.max_columns', None)

df['OE_nearest_genes'] = df['OE_name'].map(annot['genes'].to_dict())
df['OE_nearest_genes_max_distance'] = df['OE_name'].map(annot['distance'].to_dict())
df['OE_nearest_Number_genes'] = [len(x) for x in df['OE_nearest_genes']]
df = df.explode('OE_nearest_genes')
out = pd.merge(left=df, right=exp, how='left', left_on='OE_nearest_genes', right_on='ext_gene')


out.to_csv(output,sep="\t",index=False)

qvalue = 0.01
LFC = 1
out2 = out.drop_duplicates("ext_gene")
out2 = out2[out2.logFC.abs()>=LFC]
out2 = out2[out2.qval.abs()<=qvalue]
# print (out2)
print (output,"UP",out2[out2.logFC>0].shape[0])
print (output,"DOWN",out2[out2.logFC<0].shape[0])




