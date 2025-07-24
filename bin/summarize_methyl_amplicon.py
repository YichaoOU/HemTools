#!/hpcf/apps/python/install/2.7.13/bin/python

import pandas as pd
import glob
import sys
chr=sys.argv[1]
start = int(sys.argv[2])
files = glob.glob("*/*/*Nucleotide_percentage_table*")
conversion_table = []
for f in files:
    tmp = {}
    df = pd.read_csv(f,sep="\t",index_col=0)
    label = f.split("/")[0]
    tmp['sample'] = label
    start=start
    count=0
    out = []
    for c in df.columns:
        count += 1
        if "C" in c:
            tmp["{0}:{1}-{2}".format("chr11",start+count,start+count+2)] = df.at["C",c]*100
            out.append(["chr11",start+count,start+count+2,df.at["C",c]*100])
    conversion_table.append(pd.DataFrame.from_dict(tmp,orient="index"))
    out = pd.DataFrame(out)
    out.to_csv(label+".bdg",sep="\t",header=False,index=False)
pd.concat(conversion_table,axis=1).to_csv("Methylation_percentage.csv",header=False)
files = glob.glob("*/*/*CRISPResso_mapping_statistics*")
df_list = []
for f in files:
    df = pd.read_csv(f,sep="\t")
    label = f.split("/")[0]
    df.index = [label]
    df_list.append(df)
df = pd.concat(df_list)
df.to_csv("QC.stats.csv")
