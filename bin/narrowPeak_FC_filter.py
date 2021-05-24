#!/usr/bin/env python
import pandas as pd

import sys

file = sys.argv[1]
FC = float(sys.argv[2])
try:
	logFDR = float(sys.argv[3])
except:
	logFDR = None

df = pd.read_csv(file,sep="\t",header=None)
df = df[df[6]>=FC]

if logFDR:
	df = df[df[8]>=logFDR]
	df.to_csv(file+".filter.FC%s.logFDR%s.bed"%(FC,logFDR),sep="\t",header=False,index=False)
	exit()
df.to_csv(file+".filter.FC%s.bed"%(FC),sep="\t",header=False,index=False)
