library("DESeq2")
library("edgeR")
library("plyr")

##---------------------- parameters ----------------------------

# group label 1,2
# samples 3,4
# numer of lines to skip 5
# readin count table 6

# ouput is 1-2.DESEQ2.txt

args <- commandArgs(trailingOnly=TRUE)
group1 <- as.character(unlist(strsplit(args[3], ",")))
group2 <- as.character(unlist(strsplit(args[4], ",")))
group_label <- c(rep(args[1], length(group1)), rep(args[2], length(group2)))
skiprows <- as.numeric(args[5])
count_table_file <- args[6]
count_table <- read.table(count_table_file, sep="\t", header=TRUE, check.names=FALSE, skip=skiprows)
region_info <- count_table[,c(1,2,3,4,6)]
if(!all(c(group1, group2) %in% colnames(count_table))){
	group1 <- paste("X", group1, sep="")
	group2 <- paste("X", group2, sep="")
}
count_table <- count_table[,c(group1, group2)]
sample_info <- data.frame(sampleName=c(group1, group2), Group=group_label)
dds <- DESeqDataSetFromMatrix(countData=count_table, colData=sample_info, design = ~ Group)
sizeFactors(dds) <- calcNormFactors(count_table, method="TMM") 
dds <- estimateDispersions(dds)
dds <- nbinomWaldTest(dds)
res <- results(dds, contrast = c("Group", args[1], args[2]))
d <- data.frame(region_info, logFC=res[,"log2FoldChange"], AveExpr=res[,"baseMean"], t=res[,"stat"], P.Value=res[,"pvalue"], adj.P.Val=res[,"padj"])
d <- d[order(d[,"adj.P.Val"]),]
write.table(d, file=paste(args[1], "-", args[2], ".DESEQ2.txt", sep=""), sep="\t", quote=FALSE, row.names=FALSE)
