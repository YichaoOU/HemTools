#!/usr/bin/env Rscript

# r_env
args <- commandArgs(trailingOnly=TRUE)
infile <- args[1]
library(dupRadar)
bamDuprm=infile
# gtf="gencode.vM1.annotation.gtf"
gtf=args[2]
paired=TRUE
stranded=0
threads=8
dm <- analyzeDuprates(bamDuprm,gtf,stranded,paired,threads)

pdf(paste(infile, ".dup.plot.pdf", sep=""))
duprateExpDensPlot(DupMat=dm)       
title(infile)
dev.off()


