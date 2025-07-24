#!/usr/bin/env python


import pandas as pd
import numpy as np
import scipy.stats as sts
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
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import os
from Bio.Seq import Seq
from Bio import SeqIO
import swifter
import sys
import plotly.express as px
from Levenshtein import distance
import pybedtools
from pybedtools import BedTool
pd.options.display.max_columns = 100
pd.options.display.max_rows = 100

from scipy import stats
import pandas as pd
import glob
import os
import scipy
from statsmodels.stats.multitest import multipletests

def fisher_exact_generic_ABE(r, gRNA, control):
    try:
        # Dynamically calculate total edited reads for gRNA
        total_edited_gRNA = sum(r[(f"{gRNA}_{i}", "#Reads")]
                                for i in range(1, 4) if (f"{gRNA}_{i}", "#Reads") in r.index)

        # Dynamically calculate total edited reads for control
        total_edited_control = sum(r[(f"{control}_{i}", "#Reads")]
                                   for i in range(1, 4) if (f"{control}_{i}", "#Reads") in r.index)

        # Dynamically calculate total reads for gRNA
        total_gRNA = sum(r[(f"{gRNA}_{i}", "Reads_total")]
                         for i in range(1, 4) if (f"{gRNA}_{i}", "Reads_total") in r.index)

        # Dynamically calculate total reads for control
        total_control = sum(r[(f"{control}_{i}", "Reads_total")]
                            for i in range(1, 4) if (f"{control}_{i}", "Reads_total") in r.index)
        # print (total_edited_gRNA,total_gRNA)
        # Perform chi-squared test
        _, p, _, _ = stats.chi2_contingency([
            [total_edited_gRNA, total_gRNA - total_edited_gRNA],
            [total_edited_control, total_control - total_edited_control]
        ])
    except Exception as e:
        # print (e)
        return 1  # Default p-value if an error occurs
    return p
from scipy import stats
import pandas as pd
import glob
import os
import scipy
from statsmodels.stats.multitest import multipletests

def fisher_exact_generic_cas9(r, gRNA, control):
    try:
        # Dynamically calculate total edited reads for gRNA
        total_edited_gRNA = sum(r[(f"{gRNA}_{i}", "total_indel")]
                                for i in range(1, 4) if (f"{gRNA}_{i}", "total_indel") in r.index)

        # Dynamically calculate total edited reads for control
        total_edited_control = sum(r[(f"{control}_{i}", "total_indel")]
                                   for i in range(1, 4) if (f"{control}_{i}", "total_indel") in r.index)

        # Dynamically calculate total reads for gRNA
        total_gRNA = sum(r[(f"{gRNA}_{i}", "Reads_total")]
                         for i in range(1, 4) if (f"{gRNA}_{i}", "Reads_total") in r.index)

        # Dynamically calculate total reads for control
        total_control = sum(r[(f"{control}_{i}", "Reads_total")]
                            for i in range(1, 4) if (f"{control}_{i}", "Reads_total") in r.index)
        # print (total_edited_gRNA,total_gRNA)
        # Perform chi-squared test
        _, p, _, _ = stats.chi2_contingency([
            [total_edited_gRNA, total_gRNA - total_edited_gRNA],
            [total_edited_control, total_control - total_edited_control]
        ])
    except Exception as e:
        # print (e)
        return 1  # Default p-value if an error occurs
    return p


design_file=sys.argv[1]
def read_allele_edit_tsv(f):
    df = pd.read_csv(f,sep="\t")
    df['label'] = f.split("/")[-1].split(".")[0]
    return df
df = pd.concat([read_allele_edit_tsv(f) for f in glob.glob("*.allele.edit.tsv")])
def read_edit_eff(f):
    df = pd.read_csv(f,sep="\t",index_col=0)
    df['label'] = f.split("/")[-1].split(".")[0]
    df['Sample'] = df.index.tolist()
    df = df[['label','Sample','Reads_total','total_indel','indel_frequency']]
    return df
df2_list = [read_edit_eff(f) for f in glob.glob("*.edit_eff.tsv")]
df_indel = pd.concat(df2_list)


info = pd.read_csv(design_file,sep="\t",header=None,index_col=0)
N_info  = info.shape[0]
df = df[df.label.isin(info.index.tolist())]
N_label = df.label.nunique()
if N_info!=N_label:
    print ("N_info!=N_label")
    print (f"something is wrong with {design_file}")
df['condition'] = df.label.map(info[1])
df['rep'] = df.label.map(info[2])
df = df.merge(df_indel,how="left",left_on=['Sample','label'],right_on=['Sample','label'])
df['condition_rep'] = df.condition+"_"+df.rep.astype(str)


for label in info[1].unique():
	if label=="Control":
		continue
	tmp = df[df.condition.isin(['Control',label])]
	order_lst = ["#Reads", "%Reads", "#Reads_other", "%Reads_other", "total_indel", "indel_frequency", "Reads_total"]
	tmp = tmp.pivot(index=['Sample','gRNA'],values=order_lst,columns=['condition_rep'])
	sorted_columns = sorted(
	    tmp.columns, 
	    key=lambda x: (x[1], order_lst.index(x[0]))  # Custom sort based on your rules
	)
	tmp = tmp[sorted_columns]
	tmp.columns = tmp.columns.reorder_levels([1, 0])
	for c in ['Control']:
	    tmp[("STATS",f'gRNA_vs_{c}.P_value')] = tmp.apply(lambda r:fisher_exact_generic_ABE(r,label,c),axis=1)
	    tmp[("STATS",f'gRNA_vs_{c}.FDR')] = multipletests(pvals=tmp[("STATS",f'gRNA_vs_{c}.P_value')].tolist(), alpha=0.05, method="fdr_bh")[1]
	    tmp[("STATS",f'gRNA_vs_{c}.DIFF')] = tmp.apply(lambda r:(r[(f"{label}_1","%Reads")]+r[(f"{label}_2","%Reads")]+r[(f"{label}_3","%Reads")])/3-(r[(f"{c}_1","%Reads")]+r[(f"{c}_2","%Reads")])/2,axis=1)
	tmp[('STATS','total_reads_treated')]=tmp[[(f"{label}_1","Reads_total"),(f"{label}_2","Reads_total"),(f"{label}_3","Reads_total")]].sum(axis=1)
	tmp[('STATS','total_reads_control')]=tmp[[("Control_1","Reads_total"),("Control_2","Reads_total")]].sum(axis=1)
	total = tmp.shape[0]
	passed = tmp[(tmp[('STATS','total_reads_treated')]>=1000)&(tmp[('STATS','total_reads_control')]>=1000)].shape[0]
	tmp[('STATS','read_count_FLAG')] = (tmp[('STATS','total_reads_treated')]>=1000)&(tmp[('STATS','total_reads_control')]>=1000)
	print (label,passed,total,passed/total*100)
	tmp[('STATS','Significance')] = (tmp[("STATS",f'gRNA_vs_{c}.FDR')]<=0.05)&(tmp[('STATS','gRNA_vs_Control.DIFF')]>=0.5)  
	tmp.sort_values([('STATS','Significance'),('STATS','gRNA_vs_Control.DIFF')],ascending=False)
	tmp.to_csv(f"{label}.hybrid_capture.pivot_tabe.add_chi_square_stats.csv")  


"""
# ABE
# digenome files
files= glob.glob("/home/yli11/dirs/shengdar_group/users/Jackie/Manuscripts/2024-08-08_CHANGEseq-BE-paper_with_CHANGEseq_and_digenomeseq/Data/Digenome-seq/digenomeseq_ABE/*bed")
def read_dg(f):
    df = pd.read_csv(f,sep="\t",header=None)
    df['file'] = f.split("/")[-1]
    return df
dg = pd.concat([read_dg(f) for f in files])
dg.head()

# CHANGE-seq-BE
files = glob.glob("/home/yli11/dirs/shengdar_group/users/Jackie/Manuscripts/2024-08-08_CHANGEseq-BE-paper_with_CHANGEseq_and_digenomeseq/Data/CHANGEseq-BE/CHANGEseq-BE-ABE/*")
ch = pd.concat([pd.read_csv(f,sep="\t") for f in files])
ch.head()


# WGS results
def read_allele_edit_tsv(f):
    df = pd.read_csv(f,sep="\t")
    df['label'] = f.split("/")[-1].split(".")[0]
    return df
df = pd.concat([read_allele_edit_tsv(f) for f in glob.glob("*.allele.edit.tsv")])
# df = df[~df.Sample.isin(rerun_failed)]
# df2 = pd.concat([read_allele_edit_tsv(f) for f in glob.glob("crispressoWGS_BE_yli11_2024-11-19/*.allele.edit.tsv")])
# df = pd.concat([df,df2])
df.head()

def to_bed(r):
    tmp = r.Sample.split("_")
    r['gRNA'] = tmp[0]
    r['chr'] = tmp[-3]
    r['start'] = int(tmp[-2])
    r['end'] = int(tmp[-1])
    return r
df = df.swifter.apply(to_bed,axis=1)

def check_overlap(A,Ac,As,Ae, B,Bc,Bs,Be,tolerance):
    result = []
    for idx, row in A.iterrows():
        # Check if any row in B has the same chr and overlapping start and end positions
        condition = ((B[Bc] == row[Ac]) &
                     (B[Bs] <= row[Ae]+tolerance) &
                     (B[Be] >= row[As]-tolerance))
        if condition.any():
            result.append(True)
        else:
            result.append(False)
    return result

tmp = df.drop_duplicates("Sample")
tmp

tmp['is_in_CHANGE_seq_BE'] = check_overlap(tmp,'chr','start','end', ch,"#Chromosome","Start","End",5)

tmp['is_in_DiGenome'] = check_overlap(tmp,'chr','start','end', dg,0,1,2,5)
tmp = tmp.set_index("Sample")
df['is_in_CHANGE_seq_BE'] = df.Sample.map(tmp['is_in_CHANGE_seq_BE'])
df['is_in_DiGenome'] = df.Sample.map(tmp['is_in_DiGenome'])

def read_edit_eff(f):
    df = pd.read_csv(f,sep="\t",index_col=0)
    df['label'] = f.split("/")[-1].split(".")[0]
    df['Sample'] = df.index.tolist()
    df = df[['label','Sample','Reads_total','total_indel','indel_frequency']]
    return df
df2_list = [read_edit_eff(f) for f in glob.glob("*.edit_eff.tsv")]
df_indel = pd.concat(df2_list)
# df_indel = df_indel[~df_indel.Sample.isin(rerun_failed)]
# df_indel2 = pd.concat([read_edit_eff(f) for f in glob.glob("crispressoWGS_BE_yli11_2024-11-19/*.edit_eff.tsv")])
# df_indel = pd.concat([df_indel,df_indel2])
df_indel.head()

def get_complete_df(df,df_indel,design_label):
	info = pd.read_csv(f"{design_label}.info.tsv",sep="\t",header=None,index_col=0)
	N_info  = info.shape[0]
	df = df[df.label.isin(info.index.tolist())]
	N_label = df.label.nunique()
	if N_info!=N_label:
		print ("N_info!=N_label")
		print (f"something is wrong with {design_label}")
	df['condition'] = df.label.map(info[1])
	df['rep'] = df.label.map(info[2])
	df_control = df[(df.condition=="Control")&(df.gRNA.isin(info[info[1]!="Control"][1]))]
	df3 = df[df.gRNA==df.condition]
	if set(df3.gRNA)!=set(info[info[1]!="Control"][1]):
		print (set(df.gRNA))
		print (set(info[info[1]!="Control"][1]))
		print (f"something is wrong with {design_label}")
	df_out = pd.concat([df3,df_control])
	df_out = df_out.sort_values("#Reads",ascending=False)
	df_out2 = df_out.merge(df_indel,how="left",left_on=['Sample','label'],right_on=['Sample','label'])
	df_out2['condition_rep'] = df_out2.condition+"_"+df_out2.rep.astype(str)
	if df_out2[df_out2.Reads_total.isnull()].shape[0]!=0:
		print (f"something is wrong with {design_label}")
	return df_out2

design_label=sys.argv[1]
out_df={}
out_df[design_label] = get_complete_df(df.copy(),df_indel,design_label)


# for label in ["ABE_CRL","ABE_MKSR","ABE_PCSK9"]:
# ABE code
for label in [design_label]:
    gRNA = out_df[label].gRNA.unique()
    df_out2 = out_df[label].copy()
    for g in gRNA:
        tmp = df_out2[df_out2.gRNA==g]
        order_lst = ["#Reads", "%Reads", "#Reads_other", "%Reads_other", "total_indel", "indel_frequency", "Reads_total"]
        tmp = tmp.pivot(index=['Sample','is_in_CHANGE_seq_BE','is_in_DiGenome','gRNA'],values=order_lst,columns=['condition_rep'])
        sorted_columns = sorted(
            tmp.columns, 
            key=lambda x: (x[1], order_lst.index(x[0]))  # Custom sort based on your rules
        )
        tmp = tmp[sorted_columns]
        tmp.columns = tmp.columns.reorder_levels([1, 0])
        for c in ['Control']:
            tmp[("STATS",f'gRNA_vs_{c}.P_value')] = tmp.apply(lambda r:fisher_exact_generic_ABE(r,g,c),axis=1)
            tmp[("STATS",f'gRNA_vs_{c}.FDR')] = multipletests(pvals=tmp[("STATS",f'gRNA_vs_{c}.P_value')].tolist(), alpha=0.05, method="fdr_bh")[1]
        tmp[('STATS','total_reads_treated')]=tmp[[(f"{g}_1","Reads_total"),(f"{g}_2","Reads_total"),(f"{g}_3","Reads_total")]].sum(axis=1)
        tmp[('STATS','total_reads_control')]=tmp[[("Control_1","Reads_total"),("Control_2","Reads_total"),("Control_3","Reads_total")]].sum(axis=1)
        total = tmp.shape[0]
        passed = tmp[(tmp[('STATS','total_reads_treated')]>=1000)&(tmp[('STATS','total_reads_control')]>=1000)].shape[0]
        tmp[('STATS','read_count_FLAG')] = (tmp[('STATS','total_reads_treated')]>=1000)&(tmp[('STATS','total_reads_control')]>=1000)
        print (g,passed,total,passed/total*100)
        tmp[('STATS','Significance')] = tmp[("STATS",f'gRNA_vs_{c}.FDR')]<=0.05    
        tmp.to_csv(f"{label}.hybrid_capture.{g}.pivot_tabe.add_chi_square_stats.csv")  
# Cas9 code, 3 T 3 control
# for label in ["cas9_VK"]:
for label in [design_label]:
    gRNA = out_df[label].gRNA.unique()
    df_out2 = out_df[label].copy()
    for g in gRNA:
        tmp = df_out2[df_out2.gRNA==g]
        order_lst = ["#Reads", "%Reads", "#Reads_other", "%Reads_other", "total_indel", "indel_frequency", "Reads_total"]
        tmp = tmp.pivot(index=['Sample','is_in_CHANGE_seq_BE','is_in_DiGenome','gRNA'],values=order_lst,columns=['condition_rep'])
        sorted_columns = sorted(
            tmp.columns, 
            key=lambda x: (x[1], order_lst.index(x[0]))  # Custom sort based on your rules
        )
        tmp = tmp[sorted_columns]
        tmp.columns = tmp.columns.reorder_levels([1, 0])
        for c in ['Control']:
            tmp[("STATS",f'gRNA_vs_{c}.P_value')] = tmp.apply(lambda r:fisher_exact_generic_cas9(r,g,c),axis=1)
            tmp[("STATS",f'gRNA_vs_{c}.FDR')] = multipletests(pvals=tmp[("STATS",f'gRNA_vs_{c}.P_value')].tolist(), alpha=0.05, method="fdr_bh")[1]
        tmp[('STATS','total_reads_treated')]=tmp[[(f"{g}_1","Reads_total"),(f"{g}_2","Reads_total"),(f"{g}_3","Reads_total")]].sum(axis=1)
        tmp[('STATS','total_reads_control')]=tmp[[("Control_1","Reads_total"),("Control_2","Reads_total"),("Control_3","Reads_total")]].sum(axis=1)
        total = tmp.shape[0]
        passed = tmp[(tmp[('STATS','total_reads_treated')]>=1000)&(tmp[('STATS','total_reads_control')]>=1000)].shape[0]
        tmp[('STATS','read_count_FLAG')] = (tmp[('STATS','total_reads_treated')]>=1000)&(tmp[('STATS','total_reads_control')]>=1000)
        print (g,passed,total,passed/total*100)
        tmp[('STATS','Significance')] = tmp[("STATS",f'gRNA_vs_{c}.FDR')]<=0.05    
        tmp.to_csv(f"{label}.hybrid_capture.{g}.pivot_tabe.add_chi_square_stats.csv")  
# Cas9 code, 3 T 2 control
# for label in ["cas9_MKSR"]:
for label in [design_label]:
    gRNA = out_df[label].gRNA.unique()
    df_out2 = out_df[label].copy()
    for g in gRNA:
        tmp = df_out2[df_out2.gRNA==g]
        order_lst = ["#Reads", "%Reads", "#Reads_other", "%Reads_other", "total_indel", "indel_frequency", "Reads_total"]
        tmp = tmp.pivot(index=['Sample','is_in_CHANGE_seq_BE','is_in_DiGenome','gRNA'],values=order_lst,columns=['condition_rep'])
        sorted_columns = sorted(
            tmp.columns, 
            key=lambda x: (x[1], order_lst.index(x[0]))  # Custom sort based on your rules
        )
        tmp = tmp[sorted_columns]
        tmp.columns = tmp.columns.reorder_levels([1, 0])
        for c in ['Control']:
            tmp[("STATS",f'gRNA_vs_{c}.P_value')] = tmp.apply(lambda r:fisher_exact_generic_cas9(r,g,c),axis=1)
            tmp[("STATS",f'gRNA_vs_{c}.FDR')] = multipletests(pvals=tmp[("STATS",f'gRNA_vs_{c}.P_value')].tolist(), alpha=0.05, method="fdr_bh")[1]
        tmp[('STATS','total_reads_treated')]=tmp[[(f"{g}_1","Reads_total"),(f"{g}_2","Reads_total"),(f"{g}_3","Reads_total")]].sum(axis=1)
        tmp[('STATS','total_reads_control')]=tmp[[("Control_1","Reads_total"),("Control_2","Reads_total")]].sum(axis=1)
        total = tmp.shape[0]
        passed = tmp[(tmp[('STATS','total_reads_treated')]>=1000)&(tmp[('STATS','total_reads_control')]>=1000)].shape[0]
        tmp[('STATS','read_count_FLAG')] = (tmp[('STATS','total_reads_treated')]>=1000)&(tmp[('STATS','total_reads_control')]>=1000)
        print (g,passed,total,passed/total*100)
        tmp[('STATS','Significance')] = tmp[("STATS",f'gRNA_vs_{c}.FDR')]<=0.05    
        tmp.to_csv(f"{label}.hybrid_capture.{g}.pivot_tabe.add_chi_square_stats.csv") 



# CBE code
# CBE has mRNA and Control as control
def fisher_exact(r,gRNA,control):
    try:
        total_edited_gRNA = r[(f"{gRNA}_1","#Reads")]+r[(f"{gRNA}_1","#Reads_other")]+r[(f"{gRNA}_2","#Reads")]+r[(f"{gRNA}_2","#Reads_other")]
        total_edited_control = r[(f"{control}_1","#Reads")]+r[(f"{control}_1","#Reads_other")]+r[(f"{control}_2","#Reads")]+r[(f"{control}_2","#Reads_other")]
        total_gRNA = r[(f"{gRNA}_1","Reads_total")]+r[(f"{gRNA}_2","Reads_total")]
        total_control = r[(f"{control}_1","Reads_total")]+r[(f"{control}_2","Reads_total")]
        _,p,_,_ = stats.chi2_contingency([
        [total_edited_gRNA,total_gRNA-total_edited_gRNA],
        [total_edited_control,total_control-total_edited_control]
                                ])
    except:
        return 1
    return p

for label in [design_label]:
	gRNA = out_df[label].gRNA.unique()
	df_out2 = out_df[label].copy()
	for g in gRNA:
		tmp = df_out2[df_out2.gRNA==g]
		order_lst = ["#Reads", "%Reads", "#Reads_other", "%Reads_other", "total_indel", "indel_frequency", "Reads_total"]
		tmp = tmp.pivot(index=['Sample','is_in_CHANGE_seq_BE','is_in_DiGenome','gRNA'],values=order_lst,columns=['condition_rep'])
		sorted_columns = sorted(
			tmp.columns, 
			key=lambda x: (x[1], order_lst.index(x[0]))  # Custom sort based on your rules
		)
		tmp = tmp[sorted_columns]
		tmp.columns = tmp.columns.reorder_levels([1, 0])
		for c in ['mRNA','Control']:
			tmp[("STATS",f'gRNA_vs_{c}.P_value')] = tmp.apply(lambda r:fisher_exact(r,g,c),axis=1)
			tmp[("STATS",f'gRNA_vs_{c}.FDR')] = multipletests(pvals=tmp[("STATS",f'gRNA_vs_{c}.P_value')].tolist(), alpha=0.05, method="fdr_bh")[1]
		tmp[('STATS','min_FDR')]=tmp[[("STATS",f'gRNA_vs_mRNA.FDR'),("STATS",f'gRNA_vs_Control.FDR')]].min(axis=1)
		tmp[('STATS','total_reads_treated')]=tmp[[(f"{g}_1","Reads_total"),(f"{g}_2","Reads_total")]].sum(axis=1)
		tmp[('STATS','total_reads_control')]=tmp[[("Control_1","Reads_total"),("Control_2","Reads_total"),("mRNA_1","Reads_total"),("mRNA_2","Reads_total")]].sum(axis=1)
		total = tmp.shape[0]
		passed = tmp[(tmp[('STATS','total_reads_treated')]>=1000)&(tmp[('STATS','total_reads_control')]>=1000)].shape[0]
		tmp[('STATS','read_count_FLAG')] = (tmp[('STATS','total_reads_treated')]>=1000)&(tmp[('STATS','total_reads_control')]>=1000)
		print (g,passed,total,passed/total*100)
		tmp[('STATS','Significance')] = tmp[('STATS','min_FDR')]<=0.05    
		tmp.to_csv(f"CBE.hybrid_capture.{g}.pivot_tabe.add_chi_square_stats.csv")



"""






		