

import sys
import pandas as pd
import glob
# exec(open("calculate_PE.py").read())
files = glob.glob("*/*/Nucleotide_frequency_table.txt")

df = pd.read_csv("PE_info.tsv",sep="\t",header=None,index_col=0)

index_list = df.index.tolist()
uid = []
ref_list = []
alt_list = []
ref_reads = []
alt_reads = []
eff = []
import re
def check_match(x,y):
    # x is cdd4
    # y is asd_cdd4_dfdf
    for i in re.split("-|_",y):
        if x == i:
            return True
    return False
    
for f in files:
    for i in index_list:
        if check_match(i,f.split("/")[0]):
            df2 = pd.read_csv(f,sep="\t",index_col=0)
            seq = [x.split(".")[0] for x in df2.columns]
            seq = "".join(seq)
            gRNA_seq,ref,alt,rel_pos = df.loc[i].tolist()
            try:
                gRNA_start = seq.index(gRNA_seq)
            except:
                print (seq)
                print (f)
                print (gRNA_seq)
            # check ref
            if seq[gRNA_start+rel_pos] != ref:
                print (f,ref,seq[gRNA_start+rel_pos],"something is wrong")
            # print ()
            ref_count = df2[df2.columns[gRNA_start+rel_pos]].loc[ref]
            alt_count = df2[df2.columns[gRNA_start+rel_pos]].loc[alt]
            total = df2[df2.columns[gRNA_start+rel_pos]].sum()
            uid.append(f.split("/")[0])
            ref_list.append(ref)
            alt_list.append(alt)
            ref_reads.append(ref_count)
            alt_reads.append(alt_count)
            eff.append(alt_count/float(total))
            continue

df3 = pd.DataFrame()
df3['file'] = uid
df3['ref'] = ref_list
df3['alt'] = alt_list
df3['ref_count'] = ref_reads
df3['alt_count'] = alt_reads
df3['eff'] = eff
df3.to_csv("editing_efficiency.csv",index=False)
