Differential Methylated region analysis
==================================================

::

	usage: DMR.py [-h] [-j JID] -f METHYLKIT_TSV -d DESIGN_MATRIX [-g GENOME]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        DMR_yli11_2025-08-29)
	  -f METHYLKIT_TSV, --methylKit_tsv METHYLKIT_TSV
	                        TSV file, 3 columns, methylKit file, sample name,
	                        group name (default: None)
	  -d DESIGN_MATRIX, --design_matrix DESIGN_MATRIX
	                        TSV file, 3 columns, group ID, group ID, output_prefix
	                        (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10 (default: hg19)



Summary
^^^^^^^

DMR analysis using methylKit. https://www.bioconductor.org/packages/devel/bioc/vignettes/methylKit/inst/doc/methylKit.html


Input
^^^^^

1. input.tsv
----------

Please copy (or softlink) methylKit files (e.g.,  ``.markdup.sorted_CpG.methylKit`` from the :doc:`DNA methylation analysis pipeline <../NGS_pipelines/methyseq>`) and make a typical input.tsv of 3 columns: File name, Sample name, Group name.

::

	==> input.tsv <==
	PB_AAVS_rep1.markdup.sorted_CpG.methylKit	PB_AAVS_rep1	Control
	PB_AAVS_rep2.markdup.sorted_CpG.methylKit	PB_AAVS_rep2	Control
	PB_g1617_rep1.markdup.sorted_CpG.methylKit	PB_g1617_rep1	BCL11Ako
	PB_g1617_rep2.markdup.sorted_CpG.methylKit	PB_g1617_rep2	BCL11Ako
	PB_ZBTB7Ag1_rep1.markdup.sorted_CpG.methylKit	PB_ZBTB7Ag1_rep1	ZBTB7Ako
	PB_ZBTB7Ag1_rep2.markdup.sorted_CpG.methylKit	PB_ZBTB7Ag1_rep2	ZBTB7Ako


2. design matrix
----------------

This is similar to peak_call.tsv. The columns are group 1, group 2, output prefix.

::

	==> design.tsv <==
	ZBTB7Ako	Control	ZBTB7Ako_vs_control
	BCL11Ako	Control	BCL11Ako_vs_control

Each line will be used as a comparison. For example, if you have three groups and possibly 3 comparisons (e.g., 1 vs 2, 1 vs 3, and 2 vs 3), then you can write down the comparisons in three lines. Again, this is same as the peak_call.tsv.



Usage
^^^^^

.. code:: bash

	hpcf_interactive

    module load python/2.7.13

    DMR.py -f input.tsv -d design.tsv -g hg19

Output
^^^^^^

DMR results (``.DMR_results.annot.csv``) are stored in the $jid folder. Gene annotation is done using homer. The ``Gene Name`` column can be then used to merge DNA methylation results with gene expression results. 


