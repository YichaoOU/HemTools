GWAS and ClinVar data
====================













Notes on extract ref/alt info from dbSNP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The most efficient way I found is to use vcftools. Extracting all GWAS SNPs (114K) only takes 25 mins, while extract 1 SNP is about 20 mins.

::

	module load vcftools/0.1.16

	time vcftools --gzvcf GCF_000001405.25.bgz --snps ~/Data/Human/hg38/GWAS/gwas.v1.2020.5.5.snp.list --out gwas.v1.2020-5-3 --recode

