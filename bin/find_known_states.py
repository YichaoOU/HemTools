#!/usr/bin/env python

import sys
import os

import datetime
import getpass
import uuid
import argparse
import pandas as pd
import scipy
from scipy.spatial.distance import pdist
from scipy.spatial.distance import cdist
from scipy.spatial.distance import squareform
import numpy as np
# find_known_states.py {{known_association}} emissions_{{number_states}}.txt {{chromatin_state_info}} reordered_row_annotation.txt

# label	r	g	b	chromHMM_col_order
# Active Promoter	255	0	0	6
# Transcribed Region	0	128	0	7
# Poised Promoter	112	48	160	4
# Weak Promoter	255	153	115	5
# Polycomb Repressed	128	128	128	3
# Open Chromatin	244	166	235	10
# Low Signal	255	255	255	2
# Low Signal	255	255	255	8
# Low Signal	255	255	255	9
# Heterochromatin	128	128	128	1



# known_association = "chromHMM_known_associations.tsv"
known_association = sys.argv[1]
# emission_df = "emissions_10.txt"
emission_df = sys.argv[2]
# color_df = "chromatin_state_info.tsv"
color_df=sys.argv[3]
known = pd.read_csv(known_association,sep="\t",index_col=0)
df = pd.read_csv(emission_df,sep="\t",index_col=0)

color = pd.read_csv(color_df,sep="\t")
out = sys.argv[4]

## find overlap columns
known.columns = [x.upper() for x in known.columns.tolist()]
df.columns = [x.upper() for x in df.columns.tolist()]
overlaps = list(set(known.columns).intersection(df.columns))
df = df[overlaps]
known = known[overlaps]
known = known[known.sum(axis=1)>0]
df2 = pd.concat([df,known])
df3 = pd.DataFrame(squareform(pdist(df2,metric="cosine")))
df3.index = df2.index.tolist()
df3.columns = df2.index.tolist()
df4 = df3.loc[df.index][known.index]
df5 = pd.DataFrame(df4.idxmin(axis=1))
df5 = df5.reset_index()
df5.columns = ["chromHMM_col_order",0]
df6 = pd.merge(df5,color,left_on=0,right_on="label")
df6 = df6[color.columns.tolist()+['chromHMM_col_order']]
df6.to_csv(out,sep="\t",index=False)
