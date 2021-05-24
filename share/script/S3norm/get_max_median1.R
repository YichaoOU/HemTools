### get parameters
args = commandArgs(trailingOnly=TRUE)

method = args[1]
file_list = args[2]
output_name = args[3]
input_filename_end = args[4]

get_frip = function(x){
	x = x[x>0]
	z = (x-mean(x))/sd(x)
	z_p = pnorm(-(z))
	z_fdr_p = p.adjust(z_p, 'fdr')
	pk_sig = x[z_fdr_p<0.05]
	frip = sum(pk_sig) / sum(x)
	return(frip)
}

get_snr = function(x){
	x = x[x>0]
	z = (x-mean(x))/sd(x)
	z_p = pnorm(-(z))
	z_fdr_p = p.adjust(z_p, 'fdr')
	pk_sig = x[z_fdr_p<0.05]
	bg_sig = x[z_fdr_p>=0.05]
	snr = mean(pk_sig) / mean(bg_sig)
	return(snr)
}

### read file list
filenames = read.table(file_list, header=F)[,1]

### get frip
frip_list = c()
filenames_new = c()
for (file in filenames){
	if (is.na(input_filename_end)){
		bedgraph_tmp = read.table(file, header=F)[,4]
	} else{
		bedgraph_tmp = read.table(paste(file, input_filename_end, sep=''), header=F)[,4]
	}
	frip_tmp = get_frip(bedgraph_tmp)
	print(paste(file, 'FRiP score:', as.character(frip_tmp)))
	frip_list = c(frip_list, frip_tmp)
	if (is.na(input_filename_end)){
		filenames_new = c(filenames_new, as.character(file))
	} else{
		filenames_new = c(filenames_new, paste(as.character(file), input_filename_end, sep=''))
	}
}

### get reference based on frip
if (method=='max1'){
	filenames_used = filenames_new[frip_list==max(frip_list)]
	frip_used = frip_list[frip_list==max(frip_list)]
} else if (method=='median1'){
	filenames_used = filenames_new[frip_list==quantile(frip_list, 0.5, type=1)]
	frip_used = frip_list[frip_list==quantile(frip_list, 0.5, type=1)]
}

print('Used reference')
print(method)
print(cbind(filenames_used, frip_used))

### write output
sig = read.table(filenames_used, header=F)[,4]
write.table(sig, output_name, quote=F, sep='\t', col.names=F, row.names=F)

