Sequencing-depth and fragment-length normalized bigwiggle track
==========================

::

	usage: normalize_bw.py [-h] [-j JID] [-f BAM_LIST] [-g GENOME]
	                       [-s GENOME_CHROM_SIZE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        normalize_bw_yli11_2019-08-12)
	  -f BAM_LIST, --bam_list BAM_LIST
	                        tsv 2 columns, output_filename & input bam file(s).
	                        Note that multiple bam files can be merged, if
	                        multiple files are given, they should be separated by
	                        space (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        chrom size. (default: hg19)
	  -s GENOME_CHROM_SIZE, --genome_chrom_size GENOME_CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Human/hg19/anno
	                        tations/hg19.chrom.sizes)

Summary
^^^^^^^

Generate sequencing-depth normalized (wrt. 1e7) and fragment-length normalized (wrt. 100bp) bigwiggle tracks given a list of bam files using Homer. By default, all reads in your bam files are used.

Ref: http://homer.ucsd.edu/homer/ngs/ucsc.html


Input
^^^^^

A 2-column tsv file. First column is output file name, Second column is bam file(s) with absolute path or without. Note that multiple bam files can be merged. If multiple bam files are given, they should be separated by ``space`` in the second column (see below line 1).

::

	output_filename	GATA1_S10.markdup.bam GATA1_S9.markdup.bam
	Banana	GATA1_S6.markdup.bam
	ABC	GATA1_S11.markdup.bam

Usage
^^^^^


.. code:: bash
	
	hpcf_interactive

	module load python/2.7.13

	normalize_bw.py -f bam.list


Output
^^^^^^

Once finished, you will be notified by email. All generated bw files are located in the job ID folder.



















