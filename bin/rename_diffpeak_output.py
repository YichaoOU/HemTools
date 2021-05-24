#!/hpcf/apps/python/install/2.7.13/bin/python



import sys
import pandas as pd
import numpy as np
deseq2_file = sys.argv[1]

treatment_name = sys.argv[2]

logFC_cutoff = np.log2(1.5)
FDR_cutoff = 0.05
df = pd.read_csv(deseq2_file,sep="\t")
sel_cols2 = ['Chr','Start','End']
df = df[df['logFC'] >=logFC_cutoff]
df = df[abs(df['adj.P.Val']) <=FDR_cutoff]
df[sel_cols2].to_csv(deseq2_file+".gain_in_%s.bed"%(treatment_name),sep="\t",index=False,header=False)

df = pd.read_csv(deseq2_file,sep="\t")
sel_cols2 = ['Chr','Start','End']
df = df[df['logFC'] <=-logFC_cutoff]
df = df[abs(df['adj.P.Val']) <=FDR_cutoff]
df[sel_cols2].to_csv(deseq2_file+".loss_in_%s.bed"%(treatment_name),sep="\t",index=False,header=False)








