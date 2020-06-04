LiftOverVCF
=========


module load picard/2.9.4



java -jar /hpcf/apps/picard/install/2.9.4/picard.jar LiftoverVcf I=hbf.annotated.noSamples.epi.vcf.gz O=hbf.annotated.noSamples.epi.hg19.vcf.gz CHAIN=~/Data/chain_files/hg38ToHg19.over.chain.gz REJECT=rejected_variants.vcf R=~/Data/Human/hg19/fasta/samtools/hg19.fa

I found picard/2.21.2 has problem.

300MB vcf gz needs about 20G memory, very fast, 4 min


sub-set vcf
^^^^^^^^^^

::

	=cut vcf 1

	# this program doesn't require much memory

	ncore=1
	mem=4000 
	q=rhel7_priority

	module load vcftools/0.1.16


	vcftools --gzvcf sgp884.snpEff.gnomad.clinvar.LanceAnno.vcf.gz --recode-INFO-all --out sgp884.snpEff.gnomad.clinvar.LanceAnno.loci.vcf --recode --bed loci.bed



ref
^^^

https://www.biostars.org/p/46331/

