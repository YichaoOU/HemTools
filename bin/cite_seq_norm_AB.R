#!/usr/bin/env Rscript


library(Seurat)
library(dplyr)
library(ggplot2)
args <- commandArgs(trailingOnly=TRUE)


s = args[1]
output = args[2]
wt_10x = Read10X(s)
# rownames(x = wt_10x[["Antibody Capture"]]) <- gsub(pattern = "_[control_]*[TotalA|TotalB]", replacement = "", x = rownames(x = wt_10x[["Antibody Capture"]]))
tmp <- CreateSeuratObject(counts = wt_10x[["Gene Expression"]], min.cells = 0, min.features = 0)
tmp[["ADT"]] <- CreateAssayObject(wt_10x[["Antibody Capture"]][, colnames(x = tmp)])
tmp <- NormalizeData(tmp, assay = "ADT", normalization.method = "CLR")
# write.table(as.matrix(GetAssayData(object = tmp@assays$ADT , slot = "data")), 'WT_ADT_CLR_norm.csv', sep = ',', row.names = T, col.names = T, quote = F)
write.table(as.matrix(GetAssayData(object = tmp@assays$ADT , slot = "data")), output, sep = ',', row.names = T, col.names = T, quote = F)

# PNG("test.png")
# FeatureScatter(wt_10_filter, feature1 = "adt_CD34", feature2 = "adt_Sca1", pt.size = 5,cols = c("#FF000032"))

