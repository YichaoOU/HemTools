Generate new genome given vcf file
==================================

::

	usage: vcf2fasta.py [-h] [-j JID] [--label LABEL]
	                    (--vcf_file VCF_FILE | --mutation_list MUTATION_LIST)
	                    [-g GENOME] [-b BLACK_LIST] [-fa GENOME_FA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        vcf2fasta_yli11_2020-04-28)
	  --label LABEL         required if --vcf_file is used (default: label)
	  --vcf_file VCF_FILE   a single vcf file containing all the mutation to be
	                        added to the fasta (default: None)
	  --mutation_list MUTATION_LIST
	                        a list of mutations, each mutation makes a new genome
	                        (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. input of hg19custom will replace
	                        anything that is supplied by user and use the default
	                        if not supplied (default: hg19)
	  -b BLACK_LIST, --black_list BLACK_LIST
	                        Blacklist file (default: None)
	  -fa GENOME_FA, --genome_fa GENOME_FA
	                        genome fasta file (default: None)


Summary
^^^^^

Generate new genome sequence and BWA (v0.7.17a) index and black_list.bed given a vcf file.

The tool is allele seq (see option 3 in **Old notes**)

Input
^^^^

We need a vcf file. A minimal working vcf file example is shown below:

::

	##fileformat=VCFv4.0
	#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	NA12878
	20	1	.	G	TTT	.	.	.	GT	1|1
	20	2	.	GGGGGGGG	CCC	.	.	.	GT	1|1

Let say we want to generate a 13bp deletion (GTCAAGGCTATTG). The coordinate is:

::

	chr11	5276112	5276125

The corresponding vcf file looks like:

::

	##fileformat=VCFv4.0
	#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	d13nt
	chr11	5276112	d13nt	TGTCAAGGCTATTG	T	.	.	.	GT	1|1

Note that bed file is 0-index but vcf file is 1-index. Since this is a deletion, the ref allele length is actually 14 bp, (including one bp on the 5' end)

1/29/2021 Update
----------------

Specifically designed for provirus insertion. The script will generate the vcf given an insertion map bed file.

::

	bed_to_allele_seq_vcf.py -bed d3.bed -fa dCTCF.fa -o d3.vcf


Usage
^^^^

::

	hpcf_interactive

	module load python/2.7.13

	vcf2fasta.py -g hg19custom -fa /research/dept/hem/common/sequencing/chenggrp/pipelines/hg19/masked_genome/hg19.chr11.HBG1-HBG2.masked.fa --vcf_file 13nt.vcf --label d13nt -j d13nt_custom_genome

The example command is a special case, where we have a HBG2-masked hg19 genome. We want to install the deletion on top of it, but keep using the hg19 black list file. So we use ``-g hg19custom`` option. Similar, one can have ``mm9custom`` or ``hg38custom``. The ``custom`` keyword will recognize related parameters such as ``-fa`` or ``--black_list``, so that user can input their own files for one of them and keep the default for others.

``--label`` is required. It needs to match the name in the last column of the vcf file.

-j is the jobID, the output folder.

Output
^^^^^^

``$label.fasta`` is the new genome fasta

BWA index is also generated for this fasta

black list for the new genome is also generated.




Old notes
^^^^


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
	20	1	.	G	TTT	.	.	.	GT	1|1
	20	2	.	GGGGGGGG	CCC	.	.	.	GT	1|1

::

	>chr20
	AAAAAAAAAA


.. code:: bash

	java -jar ../vcf2diploid.jar -id NA12878 -chr ref.fa -vcf test5.vcf -outDir .

output:

::

	>chr20_paternal
	TTTCCCA

::

	-rwxr-x--- 1 yli11 chenggrp  43 Apr 28 16:11 chr20_NA12878.map
	-rwxr-x--- 1 yli11 chenggrp  31 Apr 28 16:11 chr20_NA12878_paternal.fa
	-rwxr-x--- 1 yli11 chenggrp  31 Apr 28 16:11 chr20_NA12878_maternal.fa
	-rwxr-x--- 1 yli11 chenggrp 109 Apr 28 16:11 paternal.chain
	-rwxr-x--- 1 yli11 chenggrp 109 Apr 28 16:11 maternal.chain

Note:

1. ``NA12878`` has to match.

2. #CHROM column can be 20 or chr20.