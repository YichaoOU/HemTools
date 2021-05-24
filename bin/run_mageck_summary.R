#!/usr/bin/env Rscript
library(MAGeCKFlute)
args <- commandArgs(trailingOnly=TRUE)

countsummary = read.table(args[1],header=T,sep="\t")

outFile=args[2]

pdf(paste(outFile,".MapRatesView.pdf",sep=""))
MapRatesView(countsummary)
dev.off()

pdf(paste(outFile,".Evenness.BarView.pdf",sep=""))
IdentBarView(countsummary, x = "Label", y = "GiniIndex", ylab = "Gini index", main = "Evenness of sgRNA reads")
dev.off()

pdf(paste(outFile,".Zerocounts.BarView.pdf",sep=""))
countsummary$Missed = log10(countsummary$Zerocounts)
IdentBarView(countsummary, x = "Label", y = "Missed", fill = "#394E80",ylab = "Log10 missed gRNAs", main = "Missed sgRNAs")			 
dev.off()
