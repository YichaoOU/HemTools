### get parameters
args = commandArgs(trailingOnly=TRUE)

pval_bedgraph_file = args[1]
qval_bedgraph_file = args[2]
method = args[3]

d = read.table(pval_bedgraph_file, header=F)
p = 10^(-d[,4])
q = -log10(p.adjust(p, method))
dq = cbind(d[,1:3], q)

write.table(dq, qval_bedgraph_file, quote=F, col.names=F, row.names=F, sep='\t')
