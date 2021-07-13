Across cell type NGS data normalization
===================================

::

	usage: S3norm.py [-h] [-j JID] -f INPUT (-bam | -bw | -bdg) [-g GENOME]
	                 [-s CHROM_SIZE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        S3norm_yli11_2020-03-19)
	  -f INPUT, --input INPUT
	                        TSV file, 1 or 2 columns. If the 2nd col is available,
	                        it will be used as control. (default: None)
	  -bam                  input files are bam, bam need index (default: False)
	  -bw                   input files are bigwig (default: False)
	  -bdg                  input files are bedgraph (default: False)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -s CHROM_SIZE, --chrom_size CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Human/hg19/anno
	                        tations/hg19.chrom.sizes)

Summary
^^^^^^^

S3norm can perform read counts normalization across different cell types. It uses a monotonic nonlinear data transformation method to match signals in both the peak regions and the background regions differently, such that both sequencing depth and signal-to-noise ratio between data sets can be simulatenously normalized. 

Ref:

https://github.com/guanjue/S3norm 

https://github.com/YichaoOU/S3norm 

Input
^^^^^

A 1 column or 2 columns tsv file containing your signal data with or without control data.

For example

::

	chip_seq_1	control_1
	chip_seq_2	control_2
	chip_seq_3	control_1
	atac_seq_1

Input files can be one of the 3 types, but not mixed types:

1. Bam (with .bai index file in the same dir)

2. bigwig

3. bedgraph

Usage
^^^^^

Put all your input data in the same working directory and inside this dir, do the following:

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	S3norm.py -f input.list -bam

To make S3norm run faster, we can only normalize signals around the peak region:

.. code:: bash

	S3norm.py -f v15input.list --peak_dir ../cut_run_rfeng_2021-05-20/peak_files -bam



Output
^^^^^^

The output files are S3norm-normalized bigwig files, located at ``$jid/S3norm_NBP_bedgraph/*.bw``


Common problems
^^^^^^

1. no outputs. 
---------


This could be caused by out of memory error if you have many files to be normalized at the same time. It also depends on number of entries (i.e., resolution, binsize) in your bedgraph file. In one example I have, 6 files with hg19 binsize=100bp, took almost 50G memory to run and finish in about 3 hours. 

You shouldn't have this problem if your data looks similar to the example above because by default, we  require 80G memory.

2. input bw or bdg
-----

not implemented. If you inputs are bigwig, use ``S3norm.py -f input.list -bw``, similarly, if inputs are bedgraph, use ``-bdg``

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines

