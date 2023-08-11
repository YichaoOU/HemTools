#!/hpcf/apps/python/install/2.7.13/bin/python
import os
import sys
import math

def sign(val):

    if val<0:
        return -1
    return 1

countFile=sys.argv[1]
gseaFile=sys.argv[2]
OUT=open(gseaFile,'w')
COUNTS=open(countFile)
header=COUNTS.readline()

header=header.rstrip()
headerCols=header.split("\t")
OUT.write("Gene\tRank\n")

for line in COUNTS:
    line=line.rstrip()
    data=line.split("\t")
    gene=data[0]
    rank=-math.log10(float(data[-2])+1e-300)*sign(float(data[-5]))
    OUT.write(gene+"\t"+str(rank)+"\n")

