#!/usr/bin/env Rscript
library(MAGeCKFlute)
args <- commandArgs(trailingOnly=TRUE)

mle.gene_summary = read.table(args[1],header=T)

# FluteMLE(mle.gene_summary, ctrlname=args[2], treatname=args[3], prefix=args[4], organism=args[5])
FluteMLE(mle.gene_summary, ctrlname=args[2], treatname=args[3], proj=args[4], organism=args[5])

# FluteMLE(file3, treatname="plx", ctrlname="dmso", proj="Test", organism="hsa")




