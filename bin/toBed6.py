#!/hpcf/apps/python/install/2.7.13/bin/python
import pandas as pd
import sys
import numpy as np
output = sys.argv[2]
input = sys.argv[1]

df = pd.read_csv(input,sep="\t",header=None)
# df[4]=df[4].apply(lambda x:np.log10(x))
df[6]=1
df[7]=1
df[8]=1
df[df.columns[:9]].to_csv(output,sep="\t",header=False,index=False)






