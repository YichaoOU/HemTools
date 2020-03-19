CaptureC data analysis pipeline
===================================

::

	usage: captureC.py [-h] [-j JID] (--guess_input | -f FASTQ_TSV) [-t TARGET]
	                   [-g GENOME] [-i INDEX_FILE] [-d DPNII_COORDINATES]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        captureC_yli11_2019-10-28)
	  --guess_input         Let the program generate the input files for you.
	                        (default: False)
	  -f FASTQ_TSV, --fastq_tsv FASTQ_TSV
	                        3 columns (default: None)
	  -t TARGET, --target TARGET
	                        9 columns (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -i INDEX_FILE, --index_file INDEX_FILE
	                        BWA index file (default: /home/yli11/Data/Human/hg19/i
	                        ndex/bowtie_1.2.2_CapC_index)
	  -d DPNII_COORDINATES, --dpnII_coordinates DPNII_COORDINATES
	                        Blacklist file (default: /home/yli11/Data/Human/hg19/a
	                        nnotations/hg19_dpnII_coordinates.txt


Summary
^^^^^^^

Pipeline adopted from https://github.com/Hughes-Genome-Group/captureC

Only work for hg19 right now.

Input
^^^^^

1. fastq.tsv

Use ``--guess_input`` to automatically generate this.

::

	Banana_R1.fastq.gz	Banana_R2.fastq.gz	Banana_lovers
	Orange_R1.fastq.gz	Orange_R2.fastq.gz	Orange_lovers

2. Target bait file (MUST end with ``.txt``)

``Need absolute path to this file``

Columns are: Name, chr, target_start, target_end, chr, exclusion_start, exclusion_end, 1, A.

The last two columns are almost always 1 A, which means that I don't have a SNP defined.

Make sure there's no empty row in this file.

::

	HS3	11	5305797	5306271	11	5304797	5307271	1	A


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	captureC.py -f fastq.tsv -t /path/to/HS3_Coordinate_File.txt


Others
^^^^^^

To make a list of dpnII cut sites:

.. code:: bash
	module load ucsc

	oligoMatch dpnII.fa chr11.fa dpnII_chr11.bed

Reference
^^^^^^^^^

https://github.com/Hughes-Genome-Group/captureC/releases


















