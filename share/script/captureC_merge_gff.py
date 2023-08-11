import pandas as pd
import glob
import sys
folder_name = sys.argv[1]
def parse_gff(f):
    df = pd.read_csv(f,sep="\t",header=None)
    df.index = df[0]+"_"+df[3].astype(str)+"_"+df[4].astype(str)
    return df[5]
df_list = []
sample_list = [x.split(".Combined_reads_REdig")[0] for x in glob.glob("%s/*gff"%(folder_name))]
sample_list = list(set(sample_list))
print (sample_list)
for s in sample_list:
    s = s.split("/")[-1]
    gff_list = [parse_gff(f) for f in glob.glob("%s/%s*gff"%(folder_name,s))]
#     print (gff_list)
    df = pd.concat(gff_list,axis=1).sum(axis=1)
#     print (df[df.index.str.contains("chr11_525")].head())
    df_list.append(df)
df = pd.concat(df_list,axis=1)
df.columns  = [s.split("/")[-1] for s in sample_list]
df = df.fillna(0)
for c in df.columns:
    df[c] = df[c].astype(int)
# df = df[df.index.str.contains("chr11_")]
df.to_csv("DESEQ2.input.tsv",sep="\t")    
print (df.shape)
df.head()