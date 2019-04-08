args <- commandArgs(trailingOnly=TRUE)
count_table = args[1]
library(DESeq2)
df=read.table(count_table,header=1,sep="\t")
row.names(df)=df$sgRNA
gfp=df[,c(3:8)]
head(gfp)
apc=df[,c(9:14)]
head(apc)
names(apc)=c("neg.r1","neg.r2","neg.r3","pos.r1","pos.r2","pos.r3")
names(gfp)=c("neg.r1","neg.r2","neg.r3","pos.r1","pos.r2","pos.r3")
coldf=data.frame(t(data.frame(strsplit(names(apc),"\\.")))[,1])
 row.names(coldf)=names(apc)
names(coldf)=c("condition")

dds=DESeqDataSetFromMatrix(countData = apc, colData = coldf,design= ~ condition)
dds=DESeq(dds)
res=results(dds)
write.table(data.frame(res),file="apc_deseq.result.txt",sep="\t",quote=FALSE)


dds2=DESeqDataSetFromMatrix(countData = gfp, colData = coldf,design= ~ condition)
dds2=DESeq(dds2)
res2=results(dds2)
write.table(data.frame(res2),file="gfp_deseq.result.txt",sep="\t",quote=FALSE)
