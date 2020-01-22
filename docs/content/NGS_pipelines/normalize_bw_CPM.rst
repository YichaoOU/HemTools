Sequencing-depth and fragment-length normalized bigwiggle track
==========================

::

	usage: normalized_bw_CPM.py [-h] [-j JID] -f BAM_LIST

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        normalized_bw_CPM_yli11_2020-01-22)
	  -f BAM_LIST, --bam_list BAM_LIST
	                        tsv 2 columns, output_filename & input bam file(s)
	                        (default: None)

Summary
^^^^^^^

Normalize by CPM.

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



















