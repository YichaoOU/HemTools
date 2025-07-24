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
import os
from Bio.Seq import Seq
from Bio import SeqIO
import swifter
import sys
import plotly.express as px
from Levenshtein import distance
pd.options.display.max_columns = 100
pd.options.display.max_rows = 100
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

def plot_volcano_leafcutter(p_value,LFC,p_value_cutoff,LFC_cutoff,outfile,highlight_list_1,highlight_list_2,IL2RG_dict,xlabel="deltaPSI",ylabel="-log FDR",highlight_color_1="#fa9200",highlight_color_2="#4DBBD5"):
    # plot specs
    font = {'family' : 'normal',
            'size'   : 20}
    import matplotlib
    matplotlib.rc('font', **font)
    fig, ax = plt.subplots(figsize=(5,5))
    plot_df = pd.DataFrame()
    plot_df['LFC'] = LFC
    plot_df = plot_df.fillna(0)
    plot_df['p_value'] = p_value
    plot_df['highlight_list_1'] = highlight_list_1
    plot_df['highlight_list_2'] = highlight_list_2
    plot_df = plot_df.fillna(1)
    plot_df['-logP'] = [-np.log10(x) for x in p_value]
    if plot_df.shape[0] < 1000:
        rasterized = False
    else:
        rasterized = True
    plt.scatter(x=plot_df['LFC'], y=plot_df['-logP'], s=20, color="grey", rasterized=rasterized)

    # highlight down- or up-regulated genes
    down = plot_df[(plot_df['LFC'] <= -LFC_cutoff) & (plot_df['p_value'] <= p_value_cutoff)]
    up = plot_df[(plot_df['LFC'] >= LFC_cutoff) & (plot_df['p_value'] <= p_value_cutoff)]
    down = down[down['highlight_list_2']==False]
    up = up[up['highlight_list_2']==False]
    down = down[down['highlight_list_1']==False]
    up = up[up['highlight_list_1']==False]    
    highlight_1 = plot_df[plot_df.highlight_list_1 == True]
    highlight_2 = plot_df[plot_df.highlight_list_2 == True]
    plt.scatter(x=down['LFC'], y=down['-logP'], s=15, label="Decreased", color="#4DBBD5", rasterized=rasterized)
    plt.scatter(x=up['LFC'], y=up['-logP'], s=15, label="Increased", color="#E64B35", rasterized=rasterized)
    # plt.scatter(x=down['LFC'], y=down['-logP'], s=15, label="Decreased", color="grey", rasterized=rasterized)
    # plt.scatter(x=up['LFC'], y=up['-logP'], s=15, label="Increased", color="grey", rasterized=rasterized)    
    plt.scatter(x=highlight_1['LFC'], y=highlight_1['-logP'], s=20, label="BCL11A", color=highlight_color_1, rasterized=rasterized)
    # plt.scatter(x=down['LFC'], y=down['-logP'], s=20, color="grey", rasterized=rasterized)
    # plt.scatter(x=up['LFC'], y=up['-logP'], s=20, color="grey", rasterized=rasterized)    
    # plt.scatter(x=IL2RG_dict['x'], y=-np.log10(IL2RG_dict['y']), s=25, label="Insert", color="red")
    # plt.text(x=IL2RG_dict['x'], y=-np.log10(IL2RG_dict['y']), s="IL2RG")
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.axvline(x=-LFC_cutoff, linestyle="dashed", color="black")
    plt.axvline(x=LFC_cutoff, linestyle="dashed", color="black")
    plt.axhline(y=2, linestyle="dashed", color="black")
    plt.title(outfile.replace(".pdf", "").replace(".png", ""))
    plt.savefig(outfile, bbox_inches='tight')

df1 = pd.read_csv("leafcutter_ds_cluster_significance.txt",sep="\t").set_index('cluster')[['p','p.adjust','genes']]
df1 = df1[~df1.p.isnull()]
df1.head()


df2 = pd.read_csv("leafcutter_ds_effect_sizes.txt",sep="\t")
df2.index = df2.intron.apply(lambda x:x.split(":")[0]+":"+x.split(":")[-1])
df2 = df2.merge(df1,how="left",left_index=True,right_index=True)
df2




df2[df2.intron.str.contains("chr2:606")|df2.intron.str.contains("chr2:607")].to_csv("BCL11A.leafcutter.ds.csv",index=False)
b_index = df2[df2.intron.str.contains("chr2:606")|df2.intron.str.contains("chr2:607")].index.tolist()
b_index

df2.to_csv("leafcutter.ds.csv",index=False)

qval_col="p.adjust"
LFC_col="deltapsi"
df2['is_BCL11A'] = [x in b_index for x in df2.index]
plot_volcano_leafcutter(df2[qval_col].tolist(),df2[LFC_col].tolist(),0.01,0.2,"leafcutter_ds.volcano.pdf",df2['is_BCL11A'].tolist(),df2['is_BCL11A'].tolist(),{})








































































































