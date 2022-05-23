Differential exon analysis
==================================================

::

	usage: DEXseq.py [-h] [-j JID] -f BAM_TSV -d DESIGN_MATRIX [--cores CORES]
	                 [--src SRC] [--count_cutoff COUNT_CUTOFF] [-g GENOME]
	                 [-gff GFF]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        DEXseq_yli11_2022-05-20)
	  -f BAM_TSV, --bam_tsv BAM_TSV
	                        TSV file, 3 columns, bam file, sample name, group name
	                        (default: None)
	  -d DESIGN_MATRIX, --design_matrix DESIGN_MATRIX
	                        TSV file, 3 columns, group ID, group ID, output_prefix
	                        (default: None)
	  --cores CORES         Number of CPUs (default: 10)
	  --src SRC             DEX src (default:
	                        /home/yli11/Programs/DEXSeq/inst/python_scripts)
	  --count_cutoff COUNT_CUTOFF
	                        filter exons by sum read count, more samples should
	                        increase this cutoff (default: 10)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10 (default: hg19)
	  -gff GFF              DEXseq gff file (default: /home/yli11/Programs/DEXSeq/
	                        inst/python_scripts/gencode.v30.hg19.noagg.gff)


Summary
^^^^^^^

Differential exon analysis to identify exon skip events.


**5/20/2022**

Only works for hg19.

Only works for paired-end RNA-seq data.




Input
^^^^^

Example data dir: Projects/Siqi_data/RNAseq_data/Differential_Exon_Analysis/test

1. bam.tsv
----------

Please copy (or softlink) position sorted and indexed bam files into your working dir. Prepare ``bam.tsv`` as a 3-column tsv file: bam_file_name, sample_name, group_name. Example shown below:

::

	2393109_Nontarget_Hudep2_1_S140_L003.markdup.bam.chr21.bam	C1	control
	2393111_M1_1_Hudep2_S142_L003.markdup.bam.chr21.bam	K1	KO
	2393113_M1_2_Hudep2_2_S144_L003.markdup.bam.chr21.bam	K2	KO
	2393110_Nontarget_Hudep2_2_S141_L003.markdup.bam.chr21.bam	C2	control


2. design matrix
----------------

This is similar to peak_call.tsv. The columns are group 1, group 2, output prefix.

::

	KO	control	myOut

Each line will be used as a comparison. For example, if you have three groups and possibly 3 comparisons (e.g., 1 vs 2, 1 vs 3, and 2 vs 3), then you can write down the comparisons in three lines. Again, this is same as the peak_call.tsv.



Usage
^^^^^

.. code:: bash

	hpcf_interactive

    module load python/2.7.13

    DEXseq.py -f bam.tsv -d design.tsv

Output
^^^^^^

Results are stored in the $jid folder. 

``.out`` files are exon read counts; these are inputs to DEXseq program.

``.png`` files showing mean-variance, MA plot, and p-value distribution.

``.csv`` files are the final outputs, containing p-value and fold change, just as different gene expression data.

``_results`` folder contains some HTML results summary.



