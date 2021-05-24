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

if (seperator == "\\t"){
    res <- read.csv(input_table, header=TRUE,sep="\t")
}else{
    res <- read.csv(input_table, header=TRUE,sep=seperator)
}

print (head(res))
rownames(res) = res[,1]
keyvals <- rep('black', nrow(res))

names(keyvals) <- rep('Not Significant', nrow(res))


keyvals[which(res[LFC_column] > LFC_cutoff & res[FDR_column] < FDR_cutoff)] <- 'red'
names(keyvals)[which(res[LFC_column] > LFC_cutoff & res[FDR_column] < FDR_cutoff)] <- 'Increased'


keyvals[which(res[LFC_column] < -LFC_cutoff & res[FDR_column] < FDR_cutoff)] <- 'blue'
names(keyvals)[which(res[LFC_column] < -LFC_cutoff & res[FDR_column] < FDR_cutoff)] <- 'Decreased'

f <- function(y) seq(floor(min(y)), ceiling(max(y)))
EnhancedVolcano(res,
    lab = rownames(res),
    selectLab =c(""),
    x = LFC_column,
    y = FDR_column,
    xlab = LFC_axis_name,
    ylab = FDR_axis_name,
    title = Title,
    colOverride = keyvals,
    colConnectors = 'grey50',
    pCutoff = FDR_cutoff,
    FCcutoff = LFC_cutoff,
    transcriptPointSize = 3,
    transcriptLabSize = 3.0)+ scale_y_continuous(breaks = f)+ scale_x_continuous(breaks = f)

ggsave(output_figure,dpi=600,device ="pdf")
dev.off()
EnhancedVolcano(res,
    lab = rownames(res),
    selectLab =rownames(res)[which(names(keyvals) %in% c("Increased","Decreased"))][1:10],
    x = LFC_column,
    y = FDR_column,
    xlab = LFC_axis_name,
    ylab = FDR_axis_name,
    title = Title,
    colOverride = keyvals,
    colConnectors = 'grey50',
    pCutoff = FDR_cutoff,
    FCcutoff = LFC_cutoff,
    transcriptPointSize = 3,
    transcriptLabSize = 3.0)+ scale_y_continuous(breaks = f)+ scale_x_continuous(breaks = f)

ggsave(paste(output_figure,".withNames.pdf",sep=""),dpi=600,device ="pdf")
dev.off()

