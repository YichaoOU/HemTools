#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
import glob
import sys
import argparse
import os
from Levenshtein import distance

font = {'family' : 'normal',
        'size'   : 15}
import matplotlib
matplotlib.rc('font', **font)
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-i',"--input", help="input tsv file with header", required=True)
	mainParser.add_argument('-o',"--outLabel", help="output label", required=True)
	mainParser.add_argument("-rc", help="read count column name", default="Nuclease_Read_Count")
	mainParser.add_argument("-off", help="off-target sequence column name", default="off_seq")
	mainParser.add_argument("-on", help="on-target sequence column name", default="on_seq")


	# mainParser.add_argument('--softlinks',  help=argparse.SUPPRESS,default="")
	# mainParser.add_argument('--treatment_bam',  help=argparse.SUPPRESS)
	# mainParser.add_argument('--port',  help=argparse.SUPPRESS)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args



def barplot(df,x,y,estimator,order,outLabel):
	fig, ax = plt.subplots(figsize=(8,4))
	sns.barplot(data=df,x=x,y=y,estimator=estimator,order=order,palette ="viridis",capsize=0.3,errorbar="sd")
	plt.xticks(rotation=35)
	ax.spines[['right', 'top']].set_visible(False)
	plt.savefig(f"{outLabel}.PAM_read_percent.pdf",bbox_inches='tight')


def violinplot(df,x,y,outLabel):
	fig, ax = plt.subplots(figsize=(6,4))
	sns.violinplot(data=df,x=x,y=y,cut=0,scale="width",inner="quartile",palette ="summer")
	plt.yscale("log")
	ax.spines[['right', 'top']].set_visible(False)
	plt.savefig(f"{outLabel}.Number_mismatches.pdf",bbox_inches='tight')


# not exactly sure how the original paper calculated the enrichment score, but here, the enrichment is the read count for that off-target base divided by the total reads
def calculate_enrichment_ratio(df,args):
	df2 = df.copy()
	df2['ot_length'] = df2[args.off].str.len()
	# only keep off-target length = 23
	df2=df2[df2.ot_length==23]
	# remove on-target reads
	df2 = df2[df2["#Mismatches"]!=0]
	total_reads = df2[args.rc].sum()
	df2['bases'] = df2.apply(lambda r:get_base(r,args),axis=1)
	df2 = df2.explode('bases')
	df2 = df2[~df2.bases.isnull()]
	df2 = df2.reset_index(drop=True)
	df3 = pd.DataFrame(df2.bases.tolist())
	df4 = pd.concat([df2,df3],axis=1)
	# columns 0,1,2 and position, ref, and alt bases
	plot_df = pd.DataFrame(df4[df4[1]!=df4[2]].groupby([0,2])[args.rc].sum())
	plot_df = plot_df.reset_index()
	plot_df['Enrichment_ratio'] = plot_df[args.rc]/total_reads
	lineplot_df = plot_df.copy()

	plot_df = pd.DataFrame(df4[df4[1]!=df4[2]].groupby([0,1,2])[args.rc].sum())
	plot_df = plot_df.reset_index()
	plot_df[3] = plot_df[1]+">"+plot_df[2]
	plot_df = plot_df.pivot(index=0,columns=3,values=args.rc).T
	plot_df = plot_df/total_reads
	plot_df = plot_df.sort_index(ascending=True)

	heatmap_df = plot_df.copy()
	return lineplot_df,heatmap_df

def get_base(r,args):
    seq = r[args.off]
    out = []
    if r["#Mismatches"]==0:
        return out
    on_target = r[args.on]
    for i in range(23):
        current_bp = seq[i]
        if current_bp=="-":
            continue
        if on_target[i]=="N":
            continue
        # only mismatch base is counted
        out.append([i+1,on_target[i],current_bp])
    return out

def enrich_lineplot(plot_df,outLabel):
	fig, ax = plt.subplots(figsize=(8,4))
	sns.lineplot(data = plot_df,x=0,y="Enrichment_ratio",hue=2,err_style="bars", errorbar=("se", 2),markersize=10,marker= 'h',hue_order=['A','C','G','T'],palette=sns.color_palette("hls", 4))
	plt.ylabel("Enrichment ratio")
	plt.xlabel("Position")
	ax.spines[['right', 'top']].set_visible(False)
	plt.savefig(f"{outLabel}.Enrichment_bases.lineplot.pdf",bbox_inches='tight')

def enrich_heatmap(plot_df,outLabel):
	fig, ax = plt.subplots(figsize=(10,4))
	sns.heatmap(plot_df,cmap="viridis",linewidth=0.0)
	plt.xticks(rotation=0)
	plt.xlabel("Position")
	plt.ylabel("Enrichment ratio")
	plt.savefig(f"{outLabel}.Enrichment_bases.heatmap.pdf",bbox_inches='tight')

def display_logo(myList,n,out):
    pd.DataFrame(myList[:n]).to_csv("tmp.txt",index=False,header=False)
    os.system(f"weblogo --units probability -c classic --format pdf < tmp.txt > {out}.top{n}.pdf")


def main():

	args = my_args()
	df = pd.read_csv(args.input,sep="\t")
	# calculate read_percent
	df['read_percent'] = df[args.rc]/df[args.rc].sum()*100
	df['PAM'] = ["N"+x.replace("-","")[-2:] for x in df[args.off]]
	df['protospacer_mismatch'] = df.apply(lambda r:distance(r[args.off][:-3].replace("-",""),r[args.on][:-3]),axis=1)
	df['PAM_mismatch'] = df.apply(lambda r:distance(r[args.off][-2:].replace("-",""),r[args.on][-2:]),axis=1)
	df['#Mismatches'] = df.protospacer_mismatch+df.PAM_mismatch
	# plots
	barplot(df,"PAM","read_percent","sum",sorted(df.PAM.unique()),args.outLabel)
	violinplot(df,"#Mismatches",args.rc,args.outLabel)
	lineplot_df,heatmap_df = calculate_enrichment_ratio(df,args)
	enrich_lineplot(lineplot_df,args.outLabel)
	enrich_heatmap(heatmap_df,args.outLabel)
	
	# seqlogo
	seqlogo = df[df["#Mismatches"]!=0].sort_values(args.rc,ascending=False).drop_duplicates(args.off)[args.off].tolist()
	seqlogo = [x.replace("-","")[:20] for x in seqlogo]
	display_logo(seqlogo,10,args.outLabel)
	display_logo(seqlogo,20,args.outLabel)
	display_logo(seqlogo,30,args.outLabel)

	
	



if __name__ == "__main__":
	main()




































