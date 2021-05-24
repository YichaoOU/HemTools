### get parameters
args = commandArgs(trailingOnly=TRUE)

signal_matrix = args[1]
mean_scale = args[2]
output = args[3]

signal_matrix = 'test.txt'
mean_scale = 'F'

d = read.table(signal_matrix, header=F)

if (mean_scale=='T'){
	col_means = colMeans(d)
	col_means_median = quantile(col_means, 0.5, type=1)
	mean_ref = mean(d[,col_means==col_means_median])
	dm = apply(d, 2, function(x) x/mean(x)*mean_ref)
} else{
	dm = rowMeans(d)
}

write.table(dm, output, quote=F, col.names=F, row.names=F, sep='\t')
