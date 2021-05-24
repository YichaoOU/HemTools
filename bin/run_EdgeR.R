#!/hpcf/authorized_apps/rhel7_apps/R/install/3.5.1/bin/Rscript

library("edgeR")

# Rscript run_DESEQ2.R test.DNA.count_table.tsv 064_064_gen2_1_S57_L001 064_gen1_1_S6_L001 test
args <- commandArgs(trailingOnly=TRUE)
# args[1]="test.DNA.count_table.tsv"
# args[2]="064_064_gen2_1_S57_L001"
# args[3]="064_gen1_1_S6_L001"
# args[4]="test"
infile = args[1]
group1 <- as.character(unlist(strsplit(args[2], ","))) ## treatment
group2 <- as.character(unlist(strsplit(args[3], ","))) ## control
group_label <- c(rep("treatment", length(group1)), rep("control", length(group2)))
outfile = args[4]



countData = read.csv(infile,sep="\t")
mat <- countData[,-1]
rownames(mat) <- countData[,1]
# head(mat)


group <- factor(group_label)
# print (head(mat))
# print (group_label)
# print (group)



y <- DGEList(counts=mat,group=factor(group_label))
# colnames(y)
# y$samples
# keep <- filterByExpr(y,min.count=5)

# y <- y[keep,,keep.lib.sizes=FALSE]

# y <- calcNormFactors(y,method="none")
y <- calcNormFactors(y)

design <- model.matrix(~group)

# y <- estimateDisp(y,design,trend.method="locfit")
y <- estimateDisp(y,design)

# y <- estimateCommonDisp(y,verbose=TRUE)
# y <- estimateTrendedDisp(y)
# y <- estimateTagwiseDisp(y,verbose=T)
pdf(paste(outfile, ".plotBCV.pdf", sep=""))
plotBCV(y)
dev.off()
# y$common.dispersion
#[1] 0.0001005378
# summary(y$tagwise.dispersion)


fit <- glmQLFit(y,design)
# fit <- glmFit(y,design,dispersion=0)
# fit <- glmFit(y,design)
pdf(paste(outfile, ".plotQLDisp.pdf", sep=""))
plotQLDisp(fit)
dev.off()
qlf <- glmQLFTest(fit)


# qlf <- glmLRT(fit)

res=topTags(qlf,n=Inf)

write.table(res, file=paste(outfile, ".edgeR_result.tsv", sep=""),sep="\t",quote=FALSE, row.names=TRUE)


