#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)
## input the bamFile from the ATACseqQC package 

bamfile=args[1]
genome=args[2]

# bamfile="1631312_RFA007.rmdup.uq.bam"
# genome="hg19"


if (genome=="hg19"){
library(TxDb.Hsapiens.UCSC.hg19.knownGene)
txs <- transcripts(TxDb.Hsapiens.UCSC.hg19.knownGene)
}
if (genome=="hg38"){
library(TxDb.Hsapiens.UCSC.hg38.knownGene)
txs <- transcripts(TxDb.Hsapiens.UCSC.hg38.knownGene)
}
if (genome=="mm9"){
library(TxDb.Mmusculus.UCSC.mm9.knownGene)
txs <- transcripts(TxDb.Mmusculus.UCSC.mm9.knownGene)
}
if (genome=="mm10"){
library(TxDb.Mmusculus.UCSC.mm10.knownGene)
txs <- transcripts(TxDb.Mmusculus.UCSC.mm10.knownGene)
}

library(ATACseqQC)


## ---- eval=FALSE--------------------------------------------------------------
#  source(system.file("extdata", "IGVSnapshot.R", package = "ATACseqQC"))

## -----------------------------------------------------------------------------
a=bamQC(bamfile,outPath=NULL)

sink(paste(bamfile,".bam.stat.txt",sep=""))
print(a)
sink()

png(paste(bamfile,".LibComplexity.png",sep=""))
estimateLibComplexity(readsDupFreq(bamfile))
dev.off()

## -----------------------------------------------------------------------------
## generate fragement size distribution
png(paste(bamfile,".fragSizeDist.png",sep=""))
fragSize <- fragSizeDist(bamfile, bamfile)
dev.off()
## -----------------------------------------------------------------------------
## bamfile tags to be read in
possibleTag <- list("integer"=c("AM", "AS", "CM", "CP", "FI", "H0", "H1", "H2", 
                                "HI", "IH", "MQ", "NH", "NM", "OP", "PQ", "SM",
                                "TC", "UQ"), 
                 "character"=c("BC", "BQ", "BZ", "CB", "CC", "CO", "CQ", "CR",
                               "CS", "CT", "CY", "E2", "FS", "LB", "MC", "MD",
                               "MI", "OA", "OC", "OQ", "OX", "PG", "PT", "PU",
                               "Q2", "QT", "QX", "R2", "RG", "RX", "SA", "TS",
                               "U2"))
library(Rsamtools)
bamTop100 <- scanBam(BamFile(bamfile, yieldSize = 100),
                     param = ScanBamParam(tag=unlist(possibleTag)))[[1]]$tag
tags <- names(bamTop100)[lengths(bamTop100)>0]

## files will be output into outPath
# outPath <- "splited"
# dir.create(outPath)
## shift the coordinates of 5'ends of alignments in the bam file
# library(BSgenome.Hsapiens.UCSC.hg19)

gal <- readBamFile(bamfile, tag=tags, asMates=TRUE, bigFile=F,flag=scanBamFlag(isSecondaryAlignment = FALSE, isUnmappedQuery=FALSE, isNotPassingQualityControls = FALSE, isSupplementaryAlignment = FALSE))


 # for readBamFile in released version to overcome the issue of all(elementNROWS(gal) < 3) is not TRUE


gal1 <- shiftGAlignmentsList(gal)

pt <- PTscore(gal1, txs)
png(paste(bamfile,".PTscore.png",sep=""))
plot(pt$log2meanCoverage, pt$PT_score, 
     xlab="log2 mean coverage",
     ylab="Promoter vs Transcript")
dev.off()

## -----------------------------------------------------------------------------
nfr <- NFRscore(gal1, txs)
png(paste(bamfile,".NFRscore.png",sep=""))
plot(nfr$log2meanCoverage, nfr$NFR_score, 
     xlab="log2 mean coverage",
     ylab="Nucleosome Free Regions score",
     main="NFRscore for 200bp flanking TSSs",
     xlim=c(-10, 0), ylim=c(-5, 5))
dev.off()

## -----------------------------------------------------------------------------
tsse <- TSSEscore(gal1, txs)
tsse$TSSEscore
png(paste(bamfile,".TSS_enrichment.png",sep=""))
plot(100*(-9:10-.5), tsse$values, type="b", 
     xlab="distance to TSS",
     ylab="aggregate TSS score")
# plot(100*(-9:10-.5), tsse$TSS.mean, type="b", 
     # xlab="distance to TSS",
     # ylab="aggregate TSS score")
dev.off()

save.image("test.Rdata")
# png(paste(bamfile,".LibComplexity.png",sep=""))

fileConn<-paste(bamfile,".TSS_enrichment.tsv",sep="")
write(paste("# plot_type: 'table'"), fileConn,append=FALSE)
write(paste("# section_name: 'TSS enrichment (chr1)'"), fileConn,append=TRUE)
write(paste("Sample\tTSS_enrichment"), fileConn,append=TRUE)
write(paste(bamfile,tsse$TSSEscore,sep="\t"), fileConn,append=TRUE)



