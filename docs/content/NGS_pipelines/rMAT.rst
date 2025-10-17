Differential RNA splicing analysis using rMAT
==================================================

Summary
^^^^^^^

Differential splicing analysis using rMAT, one of the best tools.

Only works hg38.


Input
^^^^^

Example data dir: Projects/Siqi_data/RNAseq_data/Differential_Exon_Analysis/test

1. bam.tsv
----------

3-col tsv, col1 is group1 bam files, seperated by commna. col2 is group2 bam files. col3 is comparison label.

::

	GFP_pos_S2.markdup.uq.bam,GFP_pos_S3.markdup.uq.bam,GFP_pos_S8.markdup.uq.bam	GFP_neg_S18.markdup.uq.bam,GFP_neg_S19.markdup.uq.bam,GFP_neg_S20.markdup.uq.bam	GFP_pos_neg
	H1_S1.markdup.uq.bam,H1_S3.markdup.uq.bam,H1_S5.markdup.uq.bam	H2_S2.markdup.uq.bam,H2_S4.markdup.uq.bam,H2_S6.markdup.uq.bam	H1_H2
	SRR5890882_Fetal_d11.markdup.uq.bam,SRR5890883_Fetal_d11.markdup.uq.bam	SRR5890878_Adult_d11.markdup.uq.bam,SRR5890879_Adult_d11.markdup.uq.bam	FA11
	SRR5890884_Fetal_d14.markdup.uq.bam,SRR5890885_Fetal_d14.markdup.uq.bam	SRR5890880_Adult_d14.markdup.uq.bam,SRR5890881_Adult_d14.markdup.uq.bam	FA14


Usage
^^^^^

make sure your readlength match ``--readLength 101``.


.. code:: bash

	hpcf_interactive

    module load python/2.7.13

    run_lsf.py -f bam.tsv --readLength 101 -p rMAT

Output
^^^^^^

Results are stored in the $jid folder. Both paired-test (folder ``$COL3.RMATS.paired``) and unpaired-test (folder ``$COL3.RMATS.unpaired``) results are generated. If your data is unpaired, ignore it. Main result is ``*.MATS.JC.txt``


