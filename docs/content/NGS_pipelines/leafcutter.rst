Differential RNA splicing analysis
==================================================

Summary
^^^^^^^

Differential splicing analysis using leafcutter, one of the best tools.

Only works for hg19.

Only works for paired-end RNA-seq data.


Input
^^^^^

Example data dir: Projects/Siqi_data/RNAseq_data/Differential_Exon_Analysis/test

1. fastq.tsv
----------

Use ``run_lsf.py --guess_input`` to generate.


2. design.tsv
----------------

Two columns. First column should match to the labels in ``fastq.tsv``. Second col is the group. Only pairwise. From leafcutter: ``Additional columns can be used to specify confounders, e.g. batch/sex/age. Numeric columns will be treated as continuous, so use e.g. batch1, batch2, batch3 rather than 1, 2, 3 if you a categorical variable.``

::

	2393110_Nontarget_Hudep2_2	WT
	2393109_Nontarget_Hudep2_1	WT
	2393111_Nontarget_Hudep2	WT
	2393114_M1_Hudep2	sgRNA
	2393113_M1_2_Hudep2_2	sgRNA
	2393112_M1_2_Hudep2_1	sgRNA


Usage
^^^^^

.. code:: bash

	hpcf_interactive

    module load python/2.7.13

    run_lsf.py -f fastq.tsv -p leafcutter -g hg19 --design_matrix $PWD/design.tsv

Output
^^^^^^

Results are stored in the $jid folder. 


