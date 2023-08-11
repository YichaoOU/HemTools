#!/usr/bin/env python
import os
import sys

countFile=sys.argv[1]
minCounts=sys.argv[2]
annoCols=4
#countFile="\\jude.stjude.org\groups\weissgrp\projects\Erythropoiesis\common\Bhoopalan\DBA\WEISS-292866-STRANDED_RSEM_gene_count.2023-03-27_18-51-53.txt"
COUNTS=open(countFile)
header=COUNTS.readline()
header=header.rstrip()
headerSplit=header.split("\t")
columns={}

RESULTS=open("counts.txt",'w')
SAMPLES=open("samples.txt",'w')

for i in range(len(headerSplit)):
    col=headerSplit[i]
    columns[i]=col

numCols=len(headerSplit)
results={}
numSamples=numCols-4

for line in COUNTS:
    #print(line)
    line=line.rstrip()
    lineSplit=line.split("\t")
    #print(lineSplit)
    ensembl=lineSplit[0]
    gene=lineSplit[1]
    if gene not in results:
        results[gene]=[]
    countsArray=[]
    for i in range(4,numCols):
        #print(i,lineSplit[i])
        val=int(round(float(lineSplit[i]),0))
        countsArray.append(val)
    results[gene].append(countsArray)

out=["Gene"]

for j in range(numSamples):
    cnum=j+annoCols
    sampleName=columns[cnum]
    if sampleName[0].isdigit():
        sampleName="X"+sampleName
    out.append(sampleName)
    SAMPLES.write(sampleName+"\t\n")

RESULTS.write("\t".join(out)+"\n")

for gene in results.keys():

    countTotals=[]
    numGeneResults=len(results[gene])

    for i in range(numGeneResults):
        sumT=sum(results[gene][i])
        if sumT<int(minCounts):
            continue
        countTotals.append([i,sumT,])
    if len(countTotals)==0:
        continue
    countTotals.sort(key=lambda x: x[1], reverse=True)
    outList=[gene]
   # print(countTotals)

    topResults=countTotals.pop(0)
    out=[gene]
    topG=topResults[0]
    for j in range(numSamples):
        val=str(results[gene][topG][j])
        out.append(val)
    RESULTS.write("\t".join(out)+"\n")

    gNum=2
    if len(countTotals)>0:
        for k in range(len(countTotals)):
            useName=gene+"_"+str(gNum)
            out=[useName]
            res=countTotals[k]
            useG=countTotals[k][0]
            for j in range(numSamples):
                val = str(results[gene][useG][j])
                out.append(val)
            RESULTS.write("\t".join(out)+"\n")
            gNum+=1



