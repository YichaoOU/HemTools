LiftOverVCF
=========


module load picard/2.9.4



java -jar /hpcf/apps/picard/install/2.9.4/picard.jar LiftoverVcf I=hbf.annotated.noSamples.epi.vcf.gz O=hbf.annotated.noSamples.epi.hg19.vcf.gz CHAIN=~/Data/chain_files/hg38ToHg19.over.chain.gz REJECT=rejected_variants.vcf R=~/Data/Human/hg19/fasta/samtools/hg19.fa

I found picard/2.21.2 has problem.
