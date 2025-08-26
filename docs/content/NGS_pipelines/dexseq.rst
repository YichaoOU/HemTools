Differential exon analysis
==================================================

::

	usage: DEXseq.py [-h] [-j JID] -f BAM_TSV -d DESIGN_MATRIX [--paired] [-g GENOME] [--gtf GTF]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory. Every output will be moved into this folder. (default:
	                        DEXseq_yli11_2025-08-26)
	  -f BAM_TSV, --bam_tsv BAM_TSV
	                        TSV file, 3 columns, bam file, sample name, group name (default: None)
	  -d DESIGN_MATRIX, --design_matrix DESIGN_MATRIX
	                        TSV file, 3 columns, group ID, group ID, output_prefix (default: None)
	  --paired              if input samples are paired, note, paired and unpared samples comparisons can't run together (default: False)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10 (default: hg19)
	  --gtf GTF             DEXseq gff file (default: /home/yli11/Data/Human/hg19/annotations/hg19.ncbiRefSeq.gtf)


Summary
^^^^^^^

Differential exon analysis to identify exon skip events.


**8/26/2025**

Only works for hg19/hg38.

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

    DEXseq.py -f bam.tsv -d design.tsv -g hg38

Output
^^^^^^

Results are stored in the $jid folder. Each comparison has their own result folder.

``DEXseq.result.csv`` is the differential exon usage result. 

``.pdf`` files are plots for HBG related genes.



