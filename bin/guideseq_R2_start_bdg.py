#!/usr/bin/env python

import sys

import os
import pandas as pd

R2_bed = sys.argv[1]
label = R2_bed.replace(".bed","")

t = pd.read_csv(R2_bed,sep="\t",header=None)
t.head()

def get_start_position(r):
    if r[5]=="+":
        start= r[1]
    else:
        start= r[2]-1
    end = start+1
    r['start'] = start
    r['end'] = end
    r['primer_type'] = r[3].split("_")[1]
    return r
t2 = t.apply(get_start_position,axis=1)
t3 = t2.groupby([0,'start','end',5,'primer_type']).size()
t3 = pd.DataFrame(t3)
t3.columns = ['RC']
t3 = t3.reset_index()
for s,d in t3.groupby(['primer_type',5]):
    if s[1]=="+":
        file = f"{label}.{s[0]}.plus.bdg"
    else:
        file = f"{label}.{s[0]}.minus.bdg"
    d = d.sort_values([0,'start'])
    d[[0,"start","end",'RC']].to_csv(file,sep="\t",header=False,index=False)
