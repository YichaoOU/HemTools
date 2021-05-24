#!/usr/bin/env Rscript
library(MAGeCKFlute)
args <- commandArgs(trailingOnly=TRUE)

rra_gene = read.table(args[1],header=T,sep="\t")
rra_sgRNA = read.table(args[2],header=T,sep="\t")
outFile=args[3]
organism=args[4]
FluteRRA(rra_gene, rra_sgRNA, prefix=outFile, organism=organism)

LFC_cut = subset(rra_sgRNA,LFC>=1 | LFC<=-1)
geneList= LFC_cut$LFC
names(geneList) = LFC_cut[,2]
enrich = EnrichAnalyzer(geneList = geneList, keytype = "Symbol", method = "GSEA", limit = c(3, 80),pvalueCutoff = 0.1, organism=organism)
pdf(paste(outFile,"_Flute_Results/EnrichedGeneView.pdf",sep=""))
EnrichedGeneView(slot(enrich, "result"), geneList, keytype = "Symbol",width=10)
dev.off()

pdf(paste(outFile,"_Flute_Results/EnrichedView.pdf",sep=""))
EnrichedView(slot(enrich, "result"))
dev.off()



