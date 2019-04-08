library(EnhancedVolcano)
args <- commandArgs(trailingOnly = TRUE)

input_table = args[1]
seperator = args[2]
LFC_column = args[3]
LFC_cutoff = as.numeric(args[4])
LFC_axis_name = args[5]
FDR_column = args[6]
FDR_cutoff = as.numeric(args[7])
FDR_axis_name = args[8]
Title = args[9]
output_figure = args[10]

# FC_cutoff = 1
# FDR_cutoff = 0.01
# locus = args[1]
# output_file = args[2]

res <- read.table(input_table, header=TRUE,sep=",")

keyvals <- rep('black', nrow(res))

names(keyvals) <- rep('Not Significant', nrow(res))

keyvals[which(res$gfp.logFC > FC_cutoff & res$gfp.padj < FDR_cutoff)] <- 'red'
names(keyvals)[which(res$gfp.logFC > FC_cutoff & res$gfp.padj < FDR_cutoff)] <- 'Increased'


keyvals[which(res$gfp.logFC < -FC_cutoff & res$gfp.padj < FDR_cutoff)] <- 'blue'
names(keyvals)[which(res$gfp.logFC < -FC_cutoff & res$gfp.padj < FDR_cutoff)] <- 'Decreased'


 EnhancedVolcano(res,
    lab = rownames(res),
    selectLab =c(""),
    x = 'gfp.logFC',
    y = 'gfp.padj',
    title = paste(locus,'gfp','Number of sgRNA:',dim(res)[1],sep=" "),
    colOverride = keyvals,
    colConnectors = 'grey50',
    pCutoff = FDR_cutoff,
    FCcutoff = FC_cutoff,
    transcriptPointSize = 1.5,
    transcriptLabSize = 3.0)

ggsave(paste("gfp",output_file,sep=""),dpi=300)

# keyvals <- rep('black', nrow(res))

# names(keyvals) <- rep('Not Significant', nrow(res))

# keyvals[which(res$apc.logFC > FC_cutoff & res$apc.padj < FDR_cutoff)] <- 'red'
# names(keyvals)[which(res$apc.logFC > FC_cutoff & res$apc.padj < FDR_cutoff)] <- 'Increased'


# keyvals[which(res$apc.logFC < -FC_cutoff & res$apc.padj < FDR_cutoff)] <- 'blue'
# names(keyvals)[which(res$apc.logFC < -FC_cutoff & res$apc.padj < FDR_cutoff)] <- 'Decreased'


#  EnhancedVolcano(res,
#     lab = rownames(res),
#     selectLab =c(""),
#     x = 'apc.logFC',
#     y = 'apc.padj',
#     title = paste(locus,'apc','Number of sgRNA:',dim(res)[1],sep=" "),
#     colOverride = keyvals,
#     colConnectors = 'grey50',
#     pCutoff = FDR_cutoff,
#     FCcutoff = FC_cutoff,
#     transcriptPointSize = 1.5,
#     transcriptLabSize = 3.0)

# ggsave(paste("apc",output_file,sep=""),dpi=300)

