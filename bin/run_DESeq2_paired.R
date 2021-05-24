#!/hpcf/authorized_apps/rhel7_apps/R/install/3.5.1/bin/Rscript

library("DESeq2")
library(gplots)

# Rscript run_DESEQ2.R test.DNA.count_table.tsv 064_064_gen2_1_S57_L001 064_gen1_1_S6_L001 test
args <- commandArgs(trailingOnly=TRUE)
# args[1]="test.DNA.count_table.tsv"
# args[2]="064_064_gen2_1_S57_L001"
# args[3]="064_gen1_1_S6_L001"
# args[4]="test"
infile = args[1]
group1 <- as.character(unlist(strsplit(args[2], ","))) ## treatment
group2 <- as.character(unlist(strsplit(args[3], ","))) ## control

# group1=c(1,2)
# group2=c(1,2)
group_label <- c(rep("treatment", length(group1)), rep("control", length(group2)))
pair_label <- c(seq(1:length(group1)), seq(1:length(group2)))
outfile = args[4]



countData = read.csv(infile,sep="\t")
mat <- countData[,-1]
rownames(mat) <- countData[,1]
head(mat)

sample_info <- data.frame(sampleName=c(group1, group2), Group=factor(group_label),Rep=factor(pair_label))

head(sample_info)

dds <- DESeqDataSetFromMatrix(countData=mat, colData=sample_info, design=~Group+Rep)

dds = DESeq(dds)
res=results(dds)
raw_count = counts(dds)
norm_count = counts(dds,normalized=TRUE)
colnames(norm_count) = paste(colnames(norm_count),".norm",sep="")
d <- data.frame(raw_count,norm_count, logFC=res[,"log2FoldChange"], AveExpr=res[,"baseMean"], t=res[,"stat"], P.Value=res[,"pvalue"], adj.P.Val=res[,"padj"])
d <- d[order(d[,"P.Value"]),]
write.table(d, file=paste(outfile, ".deseq2_result.tsv", sep=""), sep="\t", quote=FALSE, row.names=TRUE)

pdf(paste(outfile, ".plotMA.pdf", sep=""))
plotMA(res)
dev.off()

pdf(paste(outfile, ".plotDispEsts.pdf", sep=""))
plotDispEsts( dds )
dev.off()

pdf(paste(outfile, ".pvalue_hist.pdf", sep=""))
hist( res$pvalue, breaks=40, col="grey" )
dev.off()

pdf(paste(outfile, ".cooks_distance.pdf", sep=""))
boxplot(log10(assays(dds)[["cooks"]]), range=0, las=2)
dev.off()