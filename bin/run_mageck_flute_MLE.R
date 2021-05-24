#!/usr/bin/env Rscript
library(MAGeCKFlute)
args <- commandArgs(trailingOnly=TRUE)

mle.gene_summary = read.table(args[1],header=T)

FluteMLE(mle.gene_summary, ctrlname=args[2], treatname=args[3], prefix=args[4], organism=args[5])





