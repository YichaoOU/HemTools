(TOBIAS) Footprint analysis for ATAC-seq data
===================================

Summary
^^^^^^^

This pipeline applies ``TOBIAS`` (v0.13.3) and output bias-corrected footprint bed files and cutsites bw files. 

Additionally, if ``-t`` and ``-c`` options are given, this program will perform differential footprint analysis.

As of 3/24/2023, the MACS2 and motif database are set for human, but should be good for mouse.

Input
^^^^^

The input file is a tsv format containing 2 columns: bam, sample name.

Output
^^^^^^

The ``job ID`` folder contains results for each sample and each sample result is in the sample name folder.

1. bias-corrected bigwig files

``*_corrected.bw`` 

2. called TF footprints

``all_bound.bed``

3. differential motifs (not implemented)


Usage
^^^^^

Copy your ``bam`` files together with their index files ``.bam.bai`` into your working directory.



.. code:: bash

	# if you haven't logged into compute node, please do hpcf_interactive

	module load python/2.7.13

	# generate input.tsv
	run_lsf.py --guess_input --general --file_pattern bam --replace_name ".bam"

	# submit jobs
	run_lsf.py -f input.tsv -p tobias_footprint

	# OR, you want to do differential footprint analysis, note that sample1 and sample2 should match to the input.tsv 2nd column
	# not implemented run_lsf.py -f input.tsv -p tobias_footprint_diff -t sample1 -c sample2

	# add -g hg19 to specificy genome version.



Reference
^^^^^^^^^

https://github.com/loosolab/TOBIAS



















