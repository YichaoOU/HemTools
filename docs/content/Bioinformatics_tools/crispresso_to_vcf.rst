Convert CRISPResso allele frequency table to vcf-like table
======================


::

	usage: crispresso_to_vcf.py [-h] [-f INPUT] [-o OUTPUT] [-g GENOME]
	                            [--fasta FASTA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT, --input INPUT
	                        file name like:Alleles_frequency_table_around_sgRNA_CT
	                        TGTCAAGGCTATTGGTCA (default: None)
	  -o OUTPUT, --output OUTPUT
	                        output file (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg38)
	  --fasta FASTA         fasta (default:
	                        /home/yli11/Data/Human/hg38/fasta/hg38.fa)






Input
^^^^^

Allele frequency table, the file name is like ``Alleles_frequency_table_around_sgRNA_CTTGTCAAGGCTATTGGTCA.txt``


Output
^^^^^^

A vcf-like table file:

1. chromosome, ``chr``

2. position, ``coord``

3. reference allele ``ref``

4. variant allele ``variant``

5. ``var_type``

6. ``variant_size``

7. Variant Frequency (%) ``%Reads``

8. Reads or Signal for Variant ``#Reads``

To get total reads, just sum up the ``#Reads`` column.

Note that vcf file assumes ref/var sequence is positive strand, but CRISPResso allele table (the ``Aligned_Sequence`` and ``Reference_Sequence``) makes no assumption, which all depends on user's input amplicon sequence.


Usage
^^^^^


::

	module load python/2.7.13

	crispresso_to_vcf.py -f Alleles_frequency_table_around_sgRNA_CTTGTCAAGGCTATTGGTCA.txt -o vcf.csv


