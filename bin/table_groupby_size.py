#!/usr/bin/env python


import sys
import pandas as pd

file = sys.argv[1]
col=int(sys.argv[2])

df = pd.read_csv(file,sep="\t",header=None)
print (df.groupby(col).size())


