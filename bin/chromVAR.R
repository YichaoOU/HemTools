#!/usr/bin/env Rscript


library(chromVAR)
library(motifmatchr)
library(Matrix)
library(SummarizedExperiment)
library(BiocParallel)
set.seed(2017)
register(MulticoreParam(16, progressbar = TRUE))

file=args[1] ## from diffPeak counts
peakfile=args[2]

# peak
peaks <- getPeaks(peakfile, sort_peaks = TRUE)
# count
df = read.table(file,header=TRUE)
df = subset(df, select = -c(Geneid,Chr,Start,End,Strand,Length) )
my_counts_matrix <- as.matrix(df)
rownames(my_counts_matrix)=NULL
# chromVar obj
print ("chromVar obj")
fragment_counts <- SummarizedExperiment(assays = list(counts = my_counts_matrix),rowRanges = peaks)

# add GC
print ("adding GC")
library(BSgenome.Hsapiens.UCSC.hg19)
fragment_counts <- addGCBias(fragment_counts, genome = BSgenome.Hsapiens.UCSC.hg19)
head(rowData(fragment_counts))

# filter peaks
print ("filter peaks")
counts_filtered <- filterPeaks(fragment_counts, non_overlapping = TRUE,min_fragments_per_peak =10)

# get motifs
print ("get motifs")
human_motifs <- getJasparMotifs()
library(motifmatchr)
motif_ix <- matchMotifs(human_motifs, counts_filtered, genome = BSgenome.Hsapiens.UCSC.hg19)






# calculate dev
print ("calculate dev")
dev <- computeDeviations(object = counts_filtered, annotations = motif_ix)

print ("plotVariability")
variability <- computeVariability(dev)
plotVariability(variability,n=15, use_plotly = FALSE) 
dev.off()

print ("Saving results to variability.tsv, deviation.tsv, z-score.tsv")


write.table(variability,"variability.tsv",sep="\t")

write.table(assays(dev)$deviations,"deviation.tsv",sep="\t")
write.table(assays(dev)$z,"z-score.tsv",sep="\t")










