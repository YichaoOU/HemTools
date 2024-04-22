nfcore pipelines for CUT-RUN, CUT-Tag, and TIPseq 
===================================

Summary
^^^^^^^

Perform cut-run analysis using the nf-core pipeline.

ref: https://nf-co.re/cutandrun/3.2.2


Input
^^^^^

You will need to create a ``input.csv`` file with information about the samples in your experiment before running the pipeline. Keep the header, see the example below.

::

	group,replicate,fastq_1,fastq_2,control
	h3k27me3,1,READ1_FASTQ.gz,READ2_FASTQ.gz,igg_ctrl
	h3k27me3,2,READ1_FASTQ.gz,READ2_FASTQ.gz,igg_ctrl
	h3k4me3,1,READ1_FASTQ.gz,READ2_FASTQ.gz,igg_ctrl
	h3k4me3,2,READ1_FASTQ.gz,READ2_FASTQ.gz,igg_ctrl
	igg_ctrl,1,READ1_FASTQ.gz,READ2_FASTQ.gz,
	igg_ctrl,2,READ1_FASTQ.gz,READ2_FASTQ.gz,

+-----------+--------------------------------------------------------------------------------------------------------------+--+--+--+--+
| Column    | Description                                                                                                  |  |  |  |  |
+===========+==============================================================================================================+==+==+==+==+
| group     | Group identifier for sample. This will be identical for replicate samples from the same experimental group.  |  |  |  |  |
+-----------+--------------------------------------------------------------------------------------------------------------+--+--+--+--+
| replicate | Integer representing replicate number.                                                                       |  |  |  |  |
+-----------+--------------------------------------------------------------------------------------------------------------+--+--+--+--+
| fastq_1   | Full path to FastQ file for read 1. File has to be zipped and have the extension ".fastq.gz" or ".fq.gz".    |  |  |  |  |
+-----------+--------------------------------------------------------------------------------------------------------------+--+--+--+--+
| fastq_2   | Full path to FastQ file for read 2. File has to be zipped and have the extension ".fastq.gz" or ".fq.gz".    |  |  |  |  |
+-----------+--------------------------------------------------------------------------------------------------------------+--+--+--+--+
| control   | String representing the control group in the `group` column to which this replicate is assigned to.          |  |  |  |  |
+-----------+--------------------------------------------------------------------------------------------------------------+--+--+--+--+

Usage
^^^^^

::

	hpcf_interactive # login to compute node

	module load python/2.7.13

	run_lsf.py -f input.csv -p cut_run_nfcore -g hg19 --addon_parameters "  --max_cpus 5 --max_memory 50GB --peakcaller macs2 --normalisation_mode Spikein -resume"

Output
^^^^^^

See results in the ``$jobID`` folder.

