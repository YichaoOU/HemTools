Demultiplexing fastq files
=========================

::

	usage: demultiplexing_index.py [-h] -f INPUT -b BARCODE

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT, --input INPUT
	                        input undetermined fastq.gz (default: None)
	  -b BARCODE, --barcode BARCODE
	                        barcode file in fasta format (default: None)


Input
^^^^^

Barcode file
--------

Please specify the barcode sequence as a fasta file. The name will be used as the output fastq file name.

::

	>ABE8NG_posrep1
	TAAGGCGA
	>ABE8NG_posrep2
	CGTACTAG
	>ABE8NG_posrep3
	AGGCAGAA
	>ABE8NG_negrep1
	TCCTGAGC
	>ABE8NG_negrep2
	GGACTCCT
	>ABE8NG_negrep3
	TAGGCATG
	>ABE8NG_ALL
	CTCTCTAC

Undetermined fastq file
-------------------

This program only works for single-end data. Usually for sgRNA deep sequencing, you will use the R1 read.

Output
^^^^^

Demultiplexed fastq files will be named using the barcode file. Unmatched reads will be outputed to ``unmatched.fastq.gz``

Usage
^^^^^

::
	
	hpcf_interactive

	module load python/2.7.13

	# run interactively
	demultiplexing_index.py -f Undetermined_S0_R1_001.fastq.gz -b barcode.fa

	# submit job to HPC
	bsub -P dx -q priority -R rusage[mem=8000] demultiplexing_index.py -f Undetermined_S0_R1_001.fastq.gz -b barcode.fa -n 2


