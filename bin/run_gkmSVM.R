#!/usr/bin/env Rscript

library(gkmSVM) 

args <- commandArgs(trailingOnly=TRUE)

pos_bed=args[1]
genomeVersion=args[2]

kmer_fasta=args[3]
ref=args[4]
alt=args[5]

prefix=strsplit(pos_bed, "\\.bed$")[[1]]
pos_fasta = paste(prefix, ".fa", sep="")
neg_bed = paste(prefix, ".neg.bed", sep="")
neg_fasta = paste(prefix, ".neg.fa", sep="")

kernel_out = paste(prefix, ".kernel.out", sep="")
model_out = paste(prefix, ".model.txt", sep="")
weights_out= paste(prefix, ".weights.out", sep="")
deltaSVM_out =  paste(prefix, ".deltaSVM.out", sep="")

# genNullSeqs(pos_bed,nMaxTrials=10,xfold=1,genomeVersion=genomeVersion,   outputPosFastaFN=pos_fasta, outputBedFN=neg_bed, outputNegFastaFN=neg_fasta)

## SVM train
command = gettextf("gkmtrain  %s %s %s -m 10000 -T 4",pos_fasta,neg_fasta,prefix)
print (command)
system(command)
## SVM predict
command = gettextf("gkmpredict -T 4 %s %s %s",kmer_fasta,model_out,weights_out)
print (command)
system(command)

## delta SVM
command = gettextf("deltasvm.pl %s %s %s %s",ref,alt,weights_out,deltaSVM_out)
print (command)
system(command)


# gkmsvm_kernel(pos_fasta,neg_fasta, kernel_out)

# gkmsvm_trainCV(kernel_out,pos_fasta,neg_fasta,svmfnprfx=prefix, outputCVpredfn=paste(prefix, ".cvpred.out", sep=""), outputROCfn=paste(prefix, ".roc.out", sep=""))

# gkmsvm_classify(kmer_fasta,svmfnprfx=prefix, weights_out)

# gkmsvm_delta(ref,alt,svmfnprfx=prefix, deltaSVM_out)




