RNA-seq: differential gene expression analysis
==============================================

::

	usage: diffGenes.py [-h] [-j JID] -f FASTQ_TSV -d DESIGN_MATRIX [-g GENOME]
	                    [-i INDEX_FILE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        diffGenes_yli11_2019-07-03)
	  -f FASTQ_TSV, --fastq_tsv FASTQ_TSV
	                        TSV file, 4 columns, read 1, read 2, UID, group ID
	                        (default: None)
	  -d DESIGN_MATRIX, --design_matrix DESIGN_MATRIX
	                        TSV file, 3 columns, group ID, group ID, output_prefix
	                        (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10 (default: hg19)
	  -i INDEX_FILE, --index_file INDEX_FILE
	                        Kallisto index file (default:
	                        /home/yli11/Data/Human/hg19/index/kallisto/hg19.idx)


Summary
^^^^^^^

This pipeline is based on Kallisto - Sleuth.


Input
^^^^^

**1. fastq tsv**

This file contains 4 columns. The first 3 columns are read1.fastq.gz, read2.fastq.gz, and a UID for output. The 4th column is a group ID, which is used for differential gene expression analysis between any two groups.

You can use HemTools rna_seq --guess_input to generate the first 3 columns and then add the 4th column manually.

An example is shown below.

::

	1000004_RFR005_S5_R1.fastq.gz	1000004_RFR005_S5_R2.fastq.gz	1000004_RFR005_S5	h1
	1000002_RFR003_S3_R2.fastq.gz	1000002_RFR003_S3_R1.fastq.gz	1000002_RFR003_S3	h1
	1000000_RFR001_S1_R2.fastq.gz	1000000_RFR001_S1_R1.fastq.gz	1000000_RFR001_S1	h1
	1000003_RFR004_S4_R2.fastq.gz	1000003_RFR004_S4_R1.fastq.gz	1000003_RFR004_S4	h2
	1000005_RFR006_S6_R1.fastq.gz	1000005_RFR006_S6_R2.fastq.gz	1000005_RFR006_S6	h2
	1000001_RFR002_S2_R1.fastq.gz	1000001_RFR002_S2_R2.fastq.gz	1000001_RFR002_S2	h2


**2. design matrix**

This is similar to peak_call.tsv. The columns are group 1, group 2, output prefix.

::

	h1	h2	h1_vs_h2

Each line will be used as a comparison. For example, if you have three groups and possibly 3 comparisons (e.g., 1 vs 2, 1 vs 3, and 2 vs 3), then you can write down the comparisons in three lines. Again, this is same as the peak_call.tsv.

Usage
^^^^^

.. code:: bash

    module load python/2.7.13

    diffGenes.py -f fastq.tsv -d design.matrix -g hg19

Output
^^^^^^

Look for ``*final*.csv`` in ``_sleuth`` folder.

``_sleuth`` contains differential analysis and normalized TPM/read count (ext_count) information for both transcript-level and gene-level.

Fold change is calculated based on both TPM and ext_count, but they should be very similar to each other. TPM is recommended.

Use ``{{output_name}}.transcript.final.combined.tpm.csv`` for transcript level estimation.

Use ``{{output_name}}.gene.final.combined.tpm.csv`` for gene level estimation.

For volcano plot of differential genes, see :doc:`volcano <../Visualization/volcano_plot>`

A known problem
^^^^^^^^^^^^^^^

Unlikely to happend. This piece of information is not for end-user.

Calling ``Rscript`` from conda env will actually modify two files, namely ``ldpaths`` and ``Makeconf``. And there is no solution to let R not modifying these files, as discussed in https://github.com/conda-forge/r-base-feedstock/issues/67.

Since I give 777 permission to my R program, users using this pipeline will actually change the status of these file, which make it un-accessible to me or other users. One possible solution is to let the user gives 777 again to these files, so that other people can use it again. However, I predict that if ``multiple users run this pipeline at the same time, it can cause a permission error again``. 


Report bug
^^^^^^^^^^

.. code:: bash

    $ HemTools report_bug

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



