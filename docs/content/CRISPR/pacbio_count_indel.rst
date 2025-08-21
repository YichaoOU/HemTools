Long-read sequencing to quantify large indels
==========================


Input
^^^^^

input.tsv to specify input files and sample names
-----------

::

	# head input.tsv 
	m84246_250731_201925_s2.hifi_reads.bc1001.bam	E26_x
	m84246_250731_201925_s2.hifi_reads.bc1002.bam	E26_y
	m84246_250731_201925_s2.hifi_reads.bc1003.bam	E26_yKO

amplicon primer and gRNA cut positions
-----------

Use IGV BLAT to find your forward and reverse primers start and end locations. ``--left_primer_start 25234753 --left_primer_end 25236753 --right_primer_start 25242609 --right_primer_end  25244609 ``. Make sure left primer start is the smallest value and right primer end is the largest value. Usually I add +/- 1kb to the primer position. Also your gRNA cut position, ``--gRNA1_cut_pos 25240396 --gRNA2_cut_pos 25240396 --gRNA_cut_flank 2``. Here gRNA1 and gRNA2 pos should be the same. This program is designed for HBG promoters that's why we have 2 gRNA cut sites.

which chr fasta?
-----------

just map the targeted sequencing data to one chr for faster speed. The location is ``/research_jude/rgs01_jude/dept/HEM/common/sequencing/chenggrp/pipelines/hg38/fasta/chr_fasta/``. In the usage example, it is chr2.

Usage
^^^^^

Submit job

::

	run_lsf.py -f input.tsv -p pacbio_count_indel --chr_fasta /research_jude/rgs01_jude/dept/HEM/common/sequencing/chenggrp/pipelines/hg38/fasta/chr_fasta/chr2.fa --left_primer_start 25234753 --left_primer_end 25236753 --right_primer_start 25242609 --right_primer_end  25244609 --gRNA1_cut_pos 25240396 --gRNA2_cut_pos 25240396 --gRNA_cut_flank 2


