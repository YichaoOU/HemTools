#!/hpcf/apps/python/install/2.7.13/bin/python


import pandas as pd
import sys

input = sys.argv[1]
value = float(sys.argv[2])

df = pd.read_csv(input,sep="\t")
df=df[df.tpm>value]
print (df.shape)

out = "read.cutoff.%s.list"%(value)

df['target_id'].to_csv(out,index=False,header=False)



