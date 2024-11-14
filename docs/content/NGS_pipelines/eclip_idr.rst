IDR peak for eCLIP-seq
===================================

Summary
^^^^^^^

Pipeline adopted from https://github.com/YeoLab/merge_peaks

Assumming R1 reads, which captures the reverse of the actual gene strand 



Input
^^^^^

input.tsv
-------

7 columns tsv.

Rep1 bam, and clipper peak

Rep2 bam, and clipper peak

Input 1 and Input 2 bam file, can be the same

last column is sample label

::

	MBNL1_IP_1_S36.dedup.bam        MBNL1_IP_1_S36.dedup.clipper.default.bed        MBNL1_IP_2_S37.dedup.bam        MBNL1_IP_2_S37.dedup.clipper.default.bed        3162889_Hudep2_Input_S27.dedup.bam      3162889_Hudep2_Input_S27.dedup.bam      Hudep2_eclip


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	run_lsf.py -f input.tsv -p eclip_idr -g hg19

	run_lsf.py -f input.tsv -p eclip_idr -g mm10


Output
^^^^^^

1. pyGREAT html report
-----------------

Please check your email for link.

2. peak annotation
----------------------

idr_peaks.rmblck.homer.annotated.tsv

3. annotation pie chart
---------------

A simplified pie chart where priority is Exon,Promoter,5UTR,3UTR,Intron,Intergenic

4. homer motif discovery (top 1k peaks used)
---------------

1. default parameter output: ``homer_motifs_result``

2. short motif output: ``homer_motifs_result_short``



TODO
----


https://github.com/YeoLab/rbp-maps
https://github.com/Xinglab/rmats-turbo/blob/v4.3.0/README.md
https://rnaseq-mats.sourceforge.io/

create a figure similar to fig 5: https://www.nature.com/articles/s41586-020-2077-3#MOESM1