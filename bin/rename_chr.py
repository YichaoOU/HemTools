#!/hpcf/apps/python/install/2.7.13/bin/python

import pandas as pd
import sys

bed = sys.argv[1]
mapping = sys.argv[2]
out = sys.argv[3]

df = pd.read_csv(bed,sep="\t",header=None)
m = pd.read_csv(mapping,sep="\t",header=None,index_col=0)

df[0] = df[0].astype(str)
m.index = [str(x) for x in m.index]
df[0] = df[0].map(m[1].to_dict())
df.to_csv(out,sep="\t",header=False,index=False)

