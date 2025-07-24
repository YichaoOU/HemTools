#!/usr/bin/env Rscript
library(ArchR)

args <- commandArgs(trailingOnly=TRUE)
bam = args[1]
label = args[2]



addArchRGenome("hg38")


ArrowFiles <- createArrowFiles(
  inputFiles = bam,
  sampleNames = label,
  minTSS = 1, #Dont set this too high because you can always increase later
  minFrags = 1000,
  bcTag = "CB",
  addTileMat = TRUE,
  addGeneScoreMat = TRUE
)

bam10x <- getFragmentsFromArrow(ArrowFile = ArrowFiles)


projHeme1 <- ArchRProject(
  ArrowFiles = ArrowFiles, 
  outputDirectory = "HemeTutorial",
  copyArrows = TRUE #This is recommened so that if you modify the Arrow files you have an original copy for later usage.
)

getAvailableMatrices(projHeme1)


df <- getCellColData(projHeme1, select = c("log10(nFrags)", "TSSEnrichment"))
p <- ggPoint(
    x = df[,1], 
    y = df[,2], 
    colorDensity = TRUE,
    continuousSet = "sambaNight",
    xlabel = "Log10 Unique Fragments",
    ylabel = "TSS Enrichment",
    xlim = c(log10(500), quantile(df[,1], probs = 0.99)),
    ylim = c(0, quantile(df[,2], probs = 0.99))
) + geom_hline(yintercept = 4, lty = "dashed") + geom_vline(xintercept = 3, lty = "dashed")

ggsave(paste0(label,".TSS_fragment.scatter.pdf"),plot=p,height=7,width=7)

p1 <- plotFragmentSizes(ArchRProj = projHeme1)
ggsave(paste0(label,".plotFragmentSizes.pdf"),plot=p1,height=7,width=7)


p2 <- plotTSSEnrichment(ArchRProj = projHeme1)
ggsave(paste0(label,".plotTSSEnrichment.pdf"),plot=p2,height=7,width=7)


pathToMacs2 <- findMacs2()


library("Seurat")
library("Signac")
library("stringr")

library(ArchRtoSignac)



projHeme1 <- addGroupCoverages(ArchRProj = projHeme1, groupBy = "Sample")


projHeme1 <- addReproduciblePeakSet(
    ArchRProj = projHeme1, 
    groupBy = "Sample", 
    pathToMacs2 = pathToMacs2
)


projHeme1 <- addPeakMatrix(projHeme1)


pkm <- getPeakMatrix(projHeme1) # proj is an ArchRProject




df <- as.data.frame(bam10x)


df2=df %>% 
  dplyr::count(seqnames,start,end, RG)
ATAC_fragments = paste0(label,".fragment.tsv")

write.table(df2, ATAC_fragments, sep="\t", col.names=FALSE, row.names = FALSE, append = TRUE, quote = FALSE) 

save.image(file = paste0(label,".RData"))
command = paste0("module load htslib;bgzip ",ATAC_fragments,";tabix -p bed ",ATAC_fragments,".gz")
print (command)
system(command)
