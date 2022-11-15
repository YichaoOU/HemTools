#!/home/yli11/.conda/envs/captureC/bin/Rscript

###############################################
#
# Run using 
#   Rscript evaluate_catchitt.R <Labels.tsv.gz> <Predictions.tsv.gz> <chrosomomes>
# where <chromosomes> is a list of chromosomes considered for evaluation, separated
# by commas, e.g., chr8,chr21,chr1
###############################################
if(!require(package="PRROC",quietly = TRUE,character.only = TRUE)){
	install.packages("PRROC")
	library(package="PRROC",quietly = TRUE,character.only = TRUE)
}

args = commandArgs(trailingOnly=TRUE)

# could also be set manually
lab.file<-args[1]
pred.file<-args[2]
chrs<-strsplit(x = args[3],split = ",")[[1]]

labs<-read.table(lab.file, sep="\t")

preds<-read.table(pred.file, sep="\t")

preds.chr<-as.character(unique(preds[,1]))
labs.chr<-as.character(unique(labs[,1]))

if( sum(!chrs %in% labs.chr)>0 ){
	warning("Chromosome(s) ",chrs[!chrs %in% labs.chr]," not found in Labels")
}

if( sum(!chrs %in% preds.chr)>0 ){
	warning("Chromosome(s) ",chrs[!chrs %in% preds.chr]," not found in Predictions.")
}

labs<-labs[labs[,1]%in%chrs,]
preds<-preds[preds[,1]%in%chrs,]

if( sum( as.character(labs[,1])!=as.character(preds[,1]) ) > 0 | sum( labs[,2]!=preds[,2] ) > 0 ){
	stop("Labels.tsv.gz and Predictions.tsv.gz not in same order.")
}

pos<-preds[ labs[,3]=="S"|labs[,3]=="B" ,3]
negs<-preds[ labs[,3]=="U",3]

auc.roc<-roc.curve(pos,negs)$auc
auc.pr<-pr.curve(pos,negs)$auc.integral

cat(auc.roc,auc.pr,"\n")


