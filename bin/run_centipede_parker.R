#!/hpcf/authorized_apps/rhel7_apps/R/install/3.5.1/bin/Rscript
cut_file<-commandArgs(trailingOnly = T)[1]
anno_file<-commandArgs(trailingOnly = T)[2]
png_file<-commandArgs(trailingOnly = T)[3]
mlen<-commandArgs(trailingOnly = T)[4]

mlen<-as.integer(mlen)
out_prefix<-strsplit(png_file, "\\.png$")[[1]]
liyc="/home/yli11/R/3.5.1"
#library(Rsamtools)
library(CENTIPEDE,lib.loc=liyc)

#library(CENTIPEDE.tutorial)
scores<-5
cuts<-read.table(file=cut_file, colClasses = 'integer', nrows=-1)
anno<-read.table(file=anno_file, nrows=-1)
head(cbind(rep(1,dim(anno)[1]), anno[,5]))

# fit<-fitCentipede(Xlist=list(DNase=as.matrix(cuts)),Y=cbind(rep(1, dim(anno)[1]), anno[,scores]))
fit<-fitCentipede(Xlist=list(DNase=as.matrix(cuts)),Y=cbind(rep(1, dim(anno)[1]), anno[,scores]),DampLambda=0.01, DampNegBin=0.001)
#sum(fit$PostPr==1)
#sum(fit$PostPr>0.95)
write.table(fit$LambdaParList[[1]], paste(out_prefix, ".lambda.txt", sep=""), sep="\t", col.names=F, row.names=F)
write.table(fit$PostPr, paste(out_prefix, ".postpr.txt", sep=""), sep="\t", col.names=F, row.names=F)
write.table(fit$LogRatios, paste(out_prefix, ".logratio.txt", sep=""), sep="\t", col.names=F, row.names=F)

png(png_file, type="cairo")
plotProfile(fit$LambdaParList[[1]], Mlen=mlen) #changed
dev.off()
