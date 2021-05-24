import sys
import pandas as pd

inputFile=sys.argv[1]
outFile=sys.argv[2]
sizeFile=sys.argv[3]

df = pd.read_csv(inputFile,sep="\t",header=None)
df[1] = df[1].astype(int)
df[2] = df[2].astype(int)
df[3] = df[0]+":"+df[1].astype(str)+"-"+df[2].astype(str)
df[4] = df[2]-df[1]
df[5] = "+"

df[[0,1,2,3,4,5]].to_csv(outFile,sep="\t",header=False,index=False)

df[[3,4]].to_csv(sizeFile,sep="\t",header=False,index=False)

