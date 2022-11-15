#!/usr/bin/env python
import sys
import os
import argparse


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	requiredNamed = mainParser.add_argument_group('required named arguments')
	requiredNamed.add_argument('-f',"--input_tsv",  help="count table, each row is a feature, each column is a sample",required=True)
	requiredNamed.add_argument("-s","--sample_names",help="2 column tsv, first column, sample name matched to input_tsv column names, second column is the group name",required=True)
	requiredNamed.add_argument("-t","--treatment",help="treatment group name, must match group names specified in sample_names",required=True)
	requiredNamed.add_argument("-c","--control",help="control group name, must match group names specified in sample_names",required=True)

	mainParser.add_argument('-o',"--output",default="auto",help="output prefix")
	mainParser.add_argument("--count_cutoff",default=0,help="usually it's better for prefilter out some low-count genes/peaks")
	mainParser.add_argument("--N_sample_cutoff",default=0,help="usually it's better for prefilter out some low-count genes/peaks")

	mainParser.add_argument('--control_samples',  help=argparse.SUPPRESS)
	mainParser.add_argument('--treatment_samples',  help=argparse.SUPPRESS)
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

deseq2_template="""

library("DESeq2")
infile="{{input_tsv}}" # {{input_tsv}}
countData = read.csv(infile,sep="\\t")
mat <- countData[,-1]
rownames(mat) <- countData[,1]
head(mat)
g2="{{control_samples}}" #{{control_samples}}
g1="{{treatment_samples}}" #{{treatment_samples}}
group1 <- as.character(unlist(strsplit(g1, ","))) ## treatment
group2 <- as.character(unlist(strsplit(g2, ","))) ## control
group_label <- c(rep("treatment", length(group1)), rep("control", length(group2)))
outfile = "{{output}}"#{{output}}
sample_info <- data.frame(sampleName=c(group1, group2), Group=group_label)
dds <- DESeqDataSetFromMatrix(countData=mat[c(group1,group2)], colData=sample_info, design=~Group)
dds <- estimateSizeFactors(dds)
idx <- rowSums( counts(dds, normalized=TRUE) >= {{count_cutoff}} ) >= {{N_sample_cutoff}} ## 
dds <- dds[idx,]
dds <- DESeq(dds)
res=results(dds,pAdjustMethod="BH",cooksCutoff=FALSE)
raw_count = counts(dds)
norm_count = counts(dds,normalized=TRUE)
colnames(norm_count) = paste(colnames(norm_count),".norm",sep="")
d <- data.frame(raw_count,norm_count, res)
d <- d[order(d[,"pvalue"]),]
write.table(d, file=paste(outfile, ".deseq2_result.tsv", sep=""), sep="\t", quote=FALSE, row.names=TRUE)

pdf(paste(outfile, ".plotMA.pdf", sep=""))
threshold_OE <- d$pvalue < 0.01
length(which(threshold_OE))
d$threshold <- threshold_OE 
ma <- d[, c("baseMean", "log2FoldChange", "threshold")]
plotMA(ma,cex=1)
dev.off()

pdf(paste(outfile, ".plotDispEsts.pdf", sep=""))
plotDispEsts( dds )
dev.off()

pdf(paste(outfile, ".pvalue_hist.pdf", sep=""))
hist( res$pvalue, breaks=40, col="grey" )
dev.off()

pdf(paste(outfile, ".cooks_distance.pdf", sep=""))
boxplot(log10(assays(dds)[["cooks"]]), range=0, las=2)
dev.off()


"""


def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		if myDict[k] == None:
			value = ""
		else:
			value = myDict[k]
		myString = str(myString).replace("{{"+str(k)+"}}",str(value))
	return myString

def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()
def main():

	args = my_args()
	if args.output =="auto":
		args.output = "%s.vs.%s"%(args.treatment,args.control)
	import pandas as pd
	sample = pd.read_csv(args.sample_names,sep="\t",header=None)
	args.treatment_samples = ",".join(sample[sample[1]==args.treatment][0].tolist())
	args.control_samples = ",".join(sample[sample[1]==args.control][0].tolist())
	# args.control_samples = sample[sample[1]==args.control][0].tolist()
	if len(args.treatment_samples) == 0 or len(args.control_samples) == 0:
		print ("can't match treatment or control samples in your %s"%(args.sample_names))
		exit()
	deseq2 = multireplace(deseq2_template, vars(args))
	write_file("%s.R"%(args.output),deseq2)
	import os
	os.system("Rscript %s.R"%(args.output))
	os.system("mkdir {0} 2>/dev/null;mv {0}* {0} 2>/dev/null".format(args.output))
	
if __name__ == "__main__":
	main()

























