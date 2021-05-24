#!/usr/bin/env Rscript
library(Biobase)
library(limma)
library(gCrisprTools)

args <- commandArgs(trailingOnly=TRUE)

## input files
count_table = args[1] # raw count table from Mageck Count
sample_info = args[2] # fastq.tsv: fastq_R1, sample_name, group_name
gRNA_info = args[3] # raw gRNA specification file, mageck format
alignment_info = args[4] # raw count summary file from Mageck Count
control_group_name = args[5] # name of the control group
treatment_group_name = args[6] # name of the control group
contrast_name = paste("V2",treatment_group_name, " - V2",control_group_name, sep="")
control_gene_name = args[7] # name of the control gene
output_label = args[8]


## create expressionSet object
exp = read.table(count_table,header=T,sep="\t",row.names=1,as.is=T)
exp = exp[,!(names(exp) %in% c("Gene"))]
exp = as.matrix(exp)
pData = read.table("fastq.tsv",row.names=1)
pData = new("AnnotatedDataFrame",data=pData)
exp = exp[,rownames(pData)]
es = ExpressionSet(exp,pData)

## sample key
sk <- relevel(as.factor(pData(es)$V2), control_group_name)
names(sk) <- row.names(pData(es))

## gRNA annotation
ann = read.table(gRNA_info,sep=",",header=T,row.names=1)
ann[,'geneID'] = ann[,'geneSymbol']
colnames(ann)=c('target','geneSymbol','geneID')

## alignment info
d = read.table(alignment_info,header=T,row.names=1)
d[,'nomatch'] = d$Reads - d$Mapped
d[,'targets'] = d$Mapped
d[,'rejections']=0
d[,'double_match']=0
d = d[,c('targets','nomatch','rejections','double_match')]
aln=as.data.frame(t(d))





pdf(paste(output_label, ".filterReads_cutoff20.pdf", sep=""))
es_floor <- ct.filterReads(es, read.floor=20, sampleKey = sk)
dev.off()


##Convenience function for conforming the annotation object to exclude the trimmed gRNAs
ann <- ct.prepareAnnotation(ann, es, controls = control_gene_name)


pdf(paste(output_label, ".controlSpline_norm.pdf", sep=""))
es_norm <- ct.normalizeGuides(es_floor, 'controlSpline', annotation = ann, sampleKey = sk, plot.it = TRUE, geneSymb = control_gene_name)
dev.off()

pdf(paste(output_label, ".viewControls_raw.pdf", sep=""))
ct.viewControls(es, ann, sk, normalize = FALSE, geneSymb = control_gene_name)

dev.off()

pdf(paste(output_label, ".viewControls_control_spline_norm.pdf", sep=""))
ct.viewControls(es_norm, ann, sk, normalize = FALSE, geneSymb = control_gene_name)

dev.off()


write.csv(exprs(es_norm),paste(output_label, ".normalized_count.csv", sep=""))



design <- model.matrix(~ 0 + V2, pData(es))
contrasts <-makeContrasts(contrast_name, levels = design)
vm <- voom(exprs(es_norm), design)
fit <- lmFit(vm, design)
fit <- contrasts.fit(fit, contrasts)
fit <- eBayes(fit)

resultsDF <-
  ct.generateResults(
    fit,
    annotation = ann,
    RRAalphaCutoff = 0.1,
    permutations = 1000,
    scoring = "combined"
  )

write.csv(resultsDF,paste(output_label, ".resultsDF.csv", sep=""))


pdf(paste(output_label, ".Enriched.topTargets.pdf", sep=""))
ct.topTargets(fit,
              resultsDF,
              ann,
              targets = 20,
              enrich = TRUE)
dev.off()

pdf(paste(output_label, ".Depleted.topTargets.pdf", sep=""))
ct.topTargets(fit,
              resultsDF,
              ann,
              targets = 20,
              enrich = FALSE)
dev.off()


path2report <-
  ct.makeReport(fit = fit,
                eset = es,
                sampleKey = sk,
                annotation = ann,
                results = resultsDF,
                aln = aln,
                identifier=paste(output_label, ".raw_es", sep=""),
                outdir = ".")

path2report <-
  ct.makeReport(fit = fit,
                eset = es_norm,
                sampleKey = sk,
                annotation = ann,
                results = resultsDF,
                aln = aln,
                identifier=paste(output_label, ".spline_norm_es", sep=""),
                outdir = ".")

