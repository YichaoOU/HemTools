library("DESeq2")
library("edgeR")
library("plyr")

args <- commandArgs(trailingOnly=TRUE)
group1 <- as.character(unlist(strsplit(args[3], ",")))
group2 <- as.character(unlist(strsplit(args[4], ",")))
group_label <- c(rep(args[1], length(group1)), rep(args[2], length(group2)))
cutoff <- args[5]
working_dir <- args[6]
count_table_file <- args[7]
count_table <- read.table(count_table_file, sep="\t", header=TRUE, check.names=FALSE, skip=0)
region_info <- count_table[,c(1,2,3,4,6)]
if(!all(c(group1, group2) %in% colnames(count_table))){
	group1 <- paste("X", group1, sep="")
	group2 <- paste("X", group2, sep="")
}
count_table <- count_table[,c(group1, group2)]
sample_info <- data.frame(sampleName=c(group1, group2), Group=group_label)
dds <- DESeqDataSetFromMatrix(countData=count_table, colData=sample_info, design = ~ Group)
# sizeFactors(dds) <- calcNormFactors(count_table, method="TMM") 
# dds <- estimateDispersions(dds)
# dds <- nbinomWaldTest(dds)
dds = DESeq(dds)

# res <- results(dds, contrast = c("Group", args[1], args[2]))
res <- results(dds, contrast = c("Group", args[2], args[1]))

raw_count = counts(dds)
norm_count = counts(dds,normalized=TRUE)
colnames(norm_count) = paste(colnames(norm_count),".norm",sep="")
d <- data.frame(region_info,raw_count,norm_count, logFC=res[,"log2FoldChange"], AveExpr=res[,"baseMean"], t=res[,"stat"], P.Value=res[,"pvalue"], adj.P.Val=res[,"padj"])

# d <- data.frame(region_info, logFC=res[,"log2FoldChange"], AveExpr=res[,"baseMean"], t=res[,"stat"], P.Value=res[,"pvalue"], adj.P.Val=res[,"padj"])
d <- d[order(d[,"adj.P.Val"]),]
write.table(d, file=paste(working_dir, "/", args[1], "-", args[2], ".diffRegions.txt", sep=""), sep="\t", quote=FALSE, row.names=FALSE)




pdf(paste(working_dir, "/", args[1], "-", args[2], ".plotMA.pdf", sep=""))
DESeq2::plotMA(res)
dev.off()

pdf(paste(working_dir, "/", args[1], "-", args[2], ".plotDispEsts.pdf", sep=""))
plotDispEsts( dds )
dev.off()

pdf(paste(working_dir, "/", args[1], "-", args[2], ".pvalue_hist.pdf", sep=""))
hist( res$pvalue, breaks=40, col="grey" )
dev.off()

pdf(paste(working_dir, "/", args[1], "-", args[2], ".cooks_distance.pdf", sep=""))
boxplot(log10(assays(dds)[["cooks"]]), range=0, las=2)
dev.off()