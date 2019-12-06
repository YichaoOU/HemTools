Generate new genome given vcf file
==================================


::

	##fileformat=VCFv4.2
	##fileDate=20090805
	##source=myImputationProgramV3.1
	##reference=file:///seq/references/1000GenomesPilot-NCBI36.fasta
	##contig=<ID=liyc,length=13,assembly=B36,md5=f126cdf8a6e0c7f379d618ff66beb2da,species="Homo sapiens",taxonomy=x>
	##phasing=partial
	##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">
	##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
	##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
	##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">
	##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">
	##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">
	##FILTER=<ID=q10,Description="Quality below 10">
	##FILTER=<ID=s50,Description="Less than 50% of samples have data">
	#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
	liyc    3       .       A       CCC     .       .       .


Option 1: GATK
-------------

Only work for SNPs.


.. code:: bash

	module load samtools/1.7
	module load java

	nano ref.fa
	samtools faidx ref.fa
	java -jar /hpcf/apps/picard/install/2.9.4/picard.jar CreateSequenceDictionary -R ref.fa -o ref.dict


	nano input.vcf
	java -jar /hpcf/apps/gatk/install/3.5/GenomeAnalysisTK.jar -T FastaAlternateReferenceMaker  -R ref.fa -o output.fa -V input3.vcf

Option 2: vcftools
------------------

is it easy to convert back to hg19?


.. code:: bash

	module load vcftools
	vcf-consensus -h
	module load htslib

	bgzip input3.vcf
	tabix input3.vcf.gz
	cat ref.fa | vcf-consensus input3.vcf.gz


Option 3: AlleleSeq
------------------


http://info.gersteinlab.org/AlleleSeq

Minimal format for vcf input. Ref base doesn't have to be correct!

::

	##fileformat=VCFv4.0
	#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	NA12878
	20	1	.	A	TTT	.	.	.	GT	1|1
	20	2	.	A	CCC	.	.	.	GT	1|1

::

	>chr20
	AAAAAAAAAA


.. code:: bash

	java -jar ../vcf2diploid.jar -id NA12878 -chr ref.fa -vcf test5.vcf -outDir .

