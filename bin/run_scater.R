#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)
sc_example_counts = read.csv(args[1])
rownames(sc_example_counts) = make.names(sc_example_counts$X, unique=TRUE)
sc_example_counts = subset(sc_example_counts, select = -c(X) )
head(sc_example_counts)
library(scater)


data_matrix = data.matrix(sc_example_counts)
head(data_matrix)
example_sce <- SingleCellExperiment(assays = list(counts = data_matrix))
example_sce <- calculateQCMetrics(example_sce)

g=plotHighestExprs(example_sce)
ggsave(paste("plotHighestExprs","_", args[1], ".pdf", sep=""),g)


g=plotExprsFreqVsMean(example_sce)
ggsave(paste("plotExprsFreqVsMean","_", args[1], ".pdf", sep=""),g)


g=plotScater(example_sce,nfeatures = 100)
ggsave(paste("plotScater","_", args[1], ".pdf", sep=""),g)


g=plotRowData(example_sce,x = "n_cells_by_counts", y = "mean_counts")
ggsave(paste("plotRowData","_", args[1], ".pdf", sep=""),g)


g=plotColData(example_sce,x = "total_counts", y = "total_features_by_counts")
ggsave(paste("plotColData","_", args[1], ".pdf", sep=""),g)
