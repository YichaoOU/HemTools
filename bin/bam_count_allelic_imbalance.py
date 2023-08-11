#!/usr/bin/env python


import pandas as pd
import sys

def parse_bam_readcount_no_indel_tsv(f,min_read=10):
    df = pd.read_csv(f,sep="\t",header=None,usecols=list(range(10)))
    
    df[2] = df[2].apply(lambda x:x.upper())
    # display(df.sample(n=2))
    df['A'] = [int(x.split(":")[1]) for x in df[5]]
    df['C'] = [int(x.split(":")[1]) for x in df[6]]    
    df['G'] = [int(x.split(":")[1]) for x in df[7]]    
    df['T'] = [int(x.split(":")[1]) for x in df[8]] 
    
    df = df[df[3]>=min_read]
    def get_ref_alt_ratio(r):
        ref = r[2]
        max_ratio = 0
        max_base = ""
        for b in ['A','C','G','T']:
            if b == ref:
                continue
            ratio = r[b]/r[3]
            if ratio > max_ratio:
                max_ratio = ratio
                max_base = b
        r['max_ratio'] = max_ratio
        r['max_base'] = max_base   
        return r
    df = df.apply(get_ref_alt_ratio,axis=1)
    df = df[df['max_ratio']>=0.2]
    return df
df = parse_bam_readcount_no_indel_tsv(sys.argv[1])
df.to_csv(sys.argv[1]+".imbalance.csv")

