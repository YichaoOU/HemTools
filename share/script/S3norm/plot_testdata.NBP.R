library(LSD)
### read ref
d1 = read.table('average_ref_bedgraph/average_ref.bedgraph')[,4]
### read s3norm
for (i in 1:3){
for (j in 1:3){
if (i<j){
print(paste(i,'-',j))
### read NBP
dr = read.table(paste('S3norm_rc_bedgraph/sig', i,'.bedgraph.s3norm.bedgraph', sep=''))[,4]
dt = read.table(paste('S3norm_rc_bedgraph/sig', j,'.bedgraph.s3norm.bedgraph', sep=''))[,4]
### read NBP
dr_NBP = read.table(paste('NBP_bedgraph/sig', i,'.bedgraph.s3norm.NB.neglog10p.bedgraph', sep=''))[,4]
dt_NBP = read.table(paste('NBP_bedgraph/sig', j,'.bedgraph.s3norm.NB.neglog10p.bedgraph', sep=''))[,4]
### read NBP S3norm
dr_NBP_S3 = read.table(paste('S3norm_NBP_bedgraph/sig', i,'.bedgraph.NBP.s3norm.bedgraph', sep=''))[,4]
dt_NBP_S3 = read.table(paste('S3norm_NBP_bedgraph/sig', j,'.bedgraph.NBP.s3norm.bedgraph', sep=''))[,4]
### read raw
dr0 = read.table(paste('sig', i,'.bedgraph', sep=''))[,4]
dt0 = read.table(paste('sig', j,'.bedgraph', sep=''))[,4]
set.seed(2018)
lim_used_raw = c(1e-0, 1e+6)
lim_used = c(-log10(0.5), 323)
used_id = sample(length(d1), 100000)
png(paste('heatscatter.', i, '.', j, '.s3norm.NB.neglog10p.png', sep=''), width=1800)
par(mfrow=c(1,4))
heatscatter(dr0[used_id], dt0[used_id], log='xy', xlim=lim_used_raw, ylim=lim_used_raw)
abline(0,1,col='red')
heatscatter(dr[used_id], dt[used_id], log='xy', xlim=lim_used_raw, ylim=lim_used_raw)
abline(0,1,col='red')
heatscatter(dr_NBP[used_id], dt_NBP[used_id], log='xy', xlim=lim_used, ylim=lim_used)
abline(0,1,col='red')
heatscatter(dr_NBP_S3[used_id], dt_NBP_S3[used_id], log='xy', xlim=lim_used, ylim=lim_used)
abline(0,1,col='red')
dev.off()
}
}
}

#paste windowsNoBlack.bed B_B15_50.ATAC.B15_50.signal CMP_cmp.ATAC.cmp.signal LSK_lsk.ATAC.lsk.signal GMP_gmp.ATAC.gmp.signal ERY_S002R5.ATAC.S002R5.signal | shuf -n 100000 > test.txt
#cut -f1,2,3,4 test.txt | awk -F '\t' -v OFS='\t' '{if ($4>=1) print $1,$2,$3,$4; else print $1,$2,$3,0}' > sig1.bedgraph 
#cut -f1,2,3,5 test.txt | awk -F '\t' -v OFS='\t' '{if ($4>=1) print $1,$2,$3,$4; else print $1,$2,$3,0}' > sig2.bedgraph 
#cut -f1,2,3,6 test.txt | awk -F '\t' -v OFS='\t' '{if ($4>=1) print $1,$2,$3,$4; else print $1,$2,$3,0}' > sig3.bedgraph 
#cut -f1,2,3,7 test.txt | awk -F '\t' -v OFS='\t' '{if ($4>=1) print $1,$2,$3,$4; else print $1,$2,$3,0}' > sig4.bedgraph 
#cut -f1,2,3,8 test.txt | awk -F '\t' -v OFS='\t' '{if ($4>=1) print $1,$2,$3,$4; else print $1,$2,$3,0}' > sig5.bedgraph 
