#!/usr/bin/env python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
import glob
import sys
import argparse
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import warnings
warnings.filterwarnings("ignore")

def plot_scatter_correlation_XY_ax(X,Y,X_label,Y_label,ax):
	"""scatter plot with X,Y and a continouse value C for color
	
	X,Y: <list>
	X_label,Y_label,outfile: <str>
	
	diagnal line is draw
	
	if N>1000, then plot is raterized
	
	R is spearman R
	
	r is pearson R
	
	"""
	linewidth=3
	# plot data
	plot_df = pd.DataFrame()
	
	plot_df['X'] = X
	plot_df['Y'] = Y
	# for diagnal line
	# xseq = np.linspace(0, plot_df[['X','Y']].max().max(), num=100)

	# correlation
	r,p = scipy.stats.pearsonr(X,Y)
	sr,p = scipy.stats.spearmanr(X,Y)
	

	# diagnal line
	# ax.plot(xseq, 1 * xseq, label='R=%.2f\nr=%.2f'%(sr,r), linestyle='-',c="grey",linewidth=linewidth,alpha=0.7)
	# scatter plot
	if plot_df.shape[0]<1000:
		rasterized=False
	else:
		rasterized=True
	g=sns.scatterplot(plot_df,x="X",y="Y",alpha=0.5,s=20,linewidth=0,rasterized=rasterized,ax=ax,label='R=%.2f\nr=%.2f'%(sr,r))
	plt.legend()
	sns.move_legend(g, "upper left", bbox_to_anchor=(1, 1))
	ax.set_xlabel(X_label)
	ax.set_ylabel(Y_label)
	ax.spines[['right', 'top']].set_visible(False)

def one_feature_cor_plot(df,myFeature,col_names):
    import math
    n_plots = len(col_names)
    ncols = 3
    nrows = math.ceil(n_plots / ncols)
    # Create subplots
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 4))
    axes = axes.flatten()  # Flatten in case we have a multi-dimensional array
    
    # Loop over each column and plot its value counts on the corresponding subplot
    for i, col in enumerate(col_names):
        plot_scatter_correlation_XY_ax(df[myFeature].tolist(),df[col].tolist(),myFeature,col,axes[i])   
    # Remove any empty subplots if the number of plots doesn't fill the grid completely
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    plt.tight_layout(h_pad=1)
    return fig


input=sys.argv[1]
label=sys.argv[2]
df = pd.read_csv(input,sep="\t")
# df = pd.read_csv("20241014_C552_P3/2_18_new_run/identified/C552.identified.unfiltered.final.tsv",sep="\t")
df.head()
cols=["total.nuclease.rev.plus","total.nuclease.fwd.plus","total.nuclease.fwd.minus","total.nuclease.rev.minus",]

df2 = df[df[cols].astype(bool).astype(int).sum(axis=1)>1]
print ("filtering out",(df.shape[0]-df2.shape[0])/df.shape[0])
df2.to_csv(f"{label}.guide_seq_pool.matched.final.csv",index=False)
# QC plot

mdf = df2[df2.site_distance==0]
def value_counts_plot(df,col_names):
    import math
    n_plots = len(col_names)
    ncols = 3
    nrows = math.ceil(n_plots / ncols)
    # Create subplots
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 4))
    axes = axes.flatten()  # Flatten in case we have a multi-dimensional array
    
    # Loop over each column and plot its value counts on the corresponding subplot
    for i, col in enumerate(col_names):
        counts = df[col].value_counts()
        if len(counts.index)<10:
            sns.barplot(ax=axes[i], x=counts.index, y=counts.values, palette="viridis")
            axes[i].set_title(f'Value Counts for {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Count')
        else:
            sns.histplot(ax=axes[i], data=df, x=col, kde=False, color='skyblue')
            axes[i].set_title(f'Histogram for {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')            
    
    # Remove any empty subplots if the number of plots doesn't fill the grid completely
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    plt.tight_layout(h_pad=1)
    return fig
my_features = ['Site_SubstitutionsOnly.distance_between_cas9_cut_and_most_frequent_guideseq_read_start','site_strand',       'total_guideseq_reads', 'total_control_reads',
       'total_guideseq_non_dsODN_reads', 'total_control_non_dsODN_reads',
       'total.nuclease.rev.plus', 'total.nuclease.fwd.plus',
       'total.nuclease.fwd.minus', 'total.nuclease.rev.minus',
       'total.control.rev.plus', 'total.control.fwd.plus',
       'total.control.fwd.minus', 'total.control.rev.minus',
       'total.nuclease.mispriming.plus', 'total.nuclease.mispriming.minus',
       'total.control.mispriming.plus', 'total.control.mispriming.minus','min_cas9_cut_distance','Number_assignments']
fig=value_counts_plot(mdf,my_features)
plt.savefig(f"{label}.QC.barplots.png")
sns.clustermap(mdf[[       'total.nuclease.rev.plus', 'total.nuclease.fwd.plus',
       'total.nuclease.fwd.minus', 'total.nuclease.rev.minus',]].T,z_score=1,cmap="viridis",figsize=(6,4))
plt.title("on-target")
plt.savefig(f"{label}.on_target.G4_heatmap.png")
sns.clustermap(df2[[       'total.nuclease.rev.plus', 'total.nuclease.fwd.plus',
       'total.nuclease.fwd.minus', 'total.nuclease.rev.minus',]].sample(n=4000).T,z_score=1,cmap="viridis",figsize=(6,4))
plt.title("all-target")
plt.savefig(f"{label}.all.G4_heatmap.png")
my_features = ['Site_SubstitutionsOnly.distance_between_cas9_cut_and_most_frequent_guideseq_read_start',       'total_guideseq_reads', 'total_control_reads',
       'total_guideseq_non_dsODN_reads', 'total_control_non_dsODN_reads',
       'total.nuclease.rev.plus', 'total.nuclease.fwd.plus',
       'total.nuclease.fwd.minus', 'total.nuclease.rev.minus',
       'total.control.rev.plus', 'total.control.fwd.plus',
       'total.control.fwd.minus', 'total.control.rev.minus',
       'total.nuclease.mispriming.plus', 'total.nuclease.mispriming.minus',
       'total.control.mispriming.plus', 'total.control.mispriming.minus','min_cas9_cut_distance','Number_assignments']
fig=one_feature_cor_plot(df2,"site_distance",my_features)
plt.savefig(f"{label}.QC.scatterplot.png")
