#!/hpcf/apps/python/install/2.7.13/bin/python

import pandas as pd
import sys
file=sys.argv[1]
df = pd.read_csv(file,sep="\t",header=None)
df[4] = df[0]+"."+df[1].astype(str)+"."+df[2].astype(str)
df = pd.DataFrame(df.groupby(4)[3].sum())
df = df.reset_index()
#print (df.head())
tmp = pd.DataFrame(df[4].apply(lambda x:x.split(".")).tolist())
tmp[1] = tmp[1].astype(int)
tmp[2] = tmp[2].astype(int)
df[[5,6,7]] = tmp[[0,1,2]]
df = df.sort_values([5,6])
df[[5,6,7,3]].to_csv(file,sep="\t",header=False,index=False)


