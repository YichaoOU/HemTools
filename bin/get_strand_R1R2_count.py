#!/usr/bin/env python

import pandas as pd
import sys
import matplotlib
matplotlib.use('agg')
import os
import matplotlib as mpl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import argparse
import datetime
import getpass
import uuid
from scipy.interpolate import interp1d
import re, string
from matplotlib_venn import venn2
import subprocess
import pandas as pd
import seaborn as sns
# %matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import scipy
import seaborn as sns
import glob
from scipy.stats import gaussian_kde


def get_intersect(chr,start,end,all_reads,tmp1,tmp2):
	tmp = pd.DataFrame([chr,start-10,end+10])
	tmp.T.to_csv(tmp1,sep="\t",header=False,index=False)
	command="bedtools intersect -a %s -b %s -u > %s"%(all_reads,tmp1,tmp2)
	os.system(command)

def get_start_position(r):
	if r[5]=="-":
		return r[2]
	else:
		return r[1]+1
# bar = sns.barplot(x="sex", y="survived", hue="class", data=titanic);

# Define some hatches
# hatches = ['-', '+', 'x', '\\', '*', 'o']
order=['R1+','R1-','R2+','R2-']
# Loop over the bars
# for i,thisbar in enumerate(bar.patches):
    # Set a different hatch for each bar
    # thisbar.set_hatch(hatches[i])
def count(f,title,output):
	df = pd.read_csv(f,sep="\t",header=None)
	df[3] = "R"+df[3].apply(lambda x:x.split("/")[-1])
	df['hue'] = df[3]+df[5]
	df['pos'] = df.apply(get_start_position,axis=1)
	plot_df = df.groupby(['pos','hue']).size()
	
	plot_df = plot_df.reset_index()
	plot_df = plot_df.sort_values('pos')
	# print (plot_df)
	plot_df.columns = ['position','R1_R2_strand','count']
	if plot_df.shape[0]<2:
		return 1
	plt.figure(figsize=(10,5))
	bar = sns.barplot(data=plot_df,x='position',y="count",hue="R1_R2_strand",hue_order=order)
	# for i,thisbar in enumerate(bar.patches):
		
		# if i%4<=1:
			# print (i,thisbar)
			# thisbar.set_hatch("+")
	plt.title(title)
	plt.xticks(rotation=90)

	plt.savefig(output,bbox_inches='tight')
import sys
import uuid

addon_string = str(uuid.uuid4()).split("-")[-1]
read_bed = sys.argv[1] # from bam to bed
tmp1 = "%s_tmp1.bed"%(addon_string)
tmp2 = "%s_tmp2.bed"%(addon_string)
# reads_bed_list=["CRL2076_MKSR_ExoIII.bed","CRL2078_MKSR_PCR_method_rep1.bed","CRL2079_MKSR_PCR_method_rep2.bed","CRL2081_MKSR_PCR_method_test2_rep1.bed","CRL2082_MKSR_PCR_method_test2_rep2.bed"]

reads_bed_list=[read_bed]
identified_bed = sys.argv[2]
# identified_bed = "identified/CRL2078_MKSR_PCR_method_rep1_identified_matched.txt"
target = pd.read_csv(identified_bed,sep="\t")
target = target.sort_values("Nuclease_Read_Count",ascending=False)
target.index = target['Genomic Coordinate']+"("+target['Strand']+")"+target['Nuclease_Read_Count'].astype(str)

target = target.head(n=5)
# os.path.basename(path)
for reads_bed in reads_bed_list:
	for i, r in target.iterrows():
		if "#Chromosome" in r:
			get_intersect(r['#Chromosome'],r['Start'],r['End'],reads_bed,tmp1,tmp2)
		else:
			get_intersect(r['Chromosome'],r['Start'],r['End'],reads_bed,tmp1,tmp2)
		try:
			count(tmp2,i,"%s.%s.png"%(reads_bed,i))
		except Exception as e:
			print (reads_bed,e)
			print (r)
			continue

os.system("rm %s*"%(addon_string))

