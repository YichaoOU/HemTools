#!/usr/bin/env python
import pandas as pd
import sys
output = sys.argv[2]
# df = pd.read_csv(sys.argv[1],sep="\s",header=None)

lines = []
with open(sys.argv[1]) as f:
	for line in f:
		line = line.strip().split()
		lines.append(line)
df = pd.DataFrame(lines)
# df[1] = df[1].astype(int)
# df[2] = df[2].astype(int)
df.to_csv(output,sep="\t",header=False,index=False)