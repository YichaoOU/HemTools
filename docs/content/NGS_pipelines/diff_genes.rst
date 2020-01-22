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

You can use ``HemTools_dev rna_seq --guess_input`` to generate the first 3 columns and then add the 4th column manually.

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

A note on logFC
^^^^^^^^^^^^^^^

Sleuth uses `beta` from wald test as a biased estimator for logFC. It gives lower fold change for high variance transcript/gene. "For instance, if there is a very little variation for a transcript, the beta-value is very close to being the fold change measure. For a transcript with high variability, the beta will account for less of the estimated counts."

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

Reference
^^^^^^^^^

https://bl.ocks.org/jaquol/03f41f57dc6b0eacef101e9920f24d78

Using TPM to compare samples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See discuss here: https://groups.google.com/forum/#!topic/rsem-users/jJaeaSRG1eo

Basically, TPM is a technology-independent measurement because it is just a relative abundance, so it can be used to compare gene expression across different samples. However, in order to say a gene is truely differentially expressed, you have to have ``absolute`` gene expression, therefore, DESEQ2, EdgeR, sleuth, etc. need to be used for that purposes, they can give you a normalized TPM.

That means:

1. to get differentially expressed genes/transcripts, we need to apply statistical tests, e.g. using sleuth

2. for data visualization, e.g. heatmap, PCA, we can just use TPM and gene-level TPM (ref: Differential analyses for RNA-seq: transcript-level estimates improve gene-level inferences)




Build costum Kallisto index for human or mouse
^^^^^^^^^^^^^^^^^^^

Input
-----

1. cDNA.fa

2. your custom gene .fa

3. t2g gene transcript to gene name file

Human and Mouse cDNA.fa can be found below:

::

	/home/yli11/Data/Mouse/mm9/index/kallisto/Mus_musculus.NCBIM37.67.cdna.all.fa

	/home/yli11/Data/Mouse/mm10/index/kallisto/mus_musculus/Mus_musculus.GRCm38.cdna.all.fa

	/research/dept/hem/common/sequencing/chenggrp/pipelines/hg19/kallisto/release_75/Homo_sapiens.GRCh37.75.cdna.all.fa

	/research/dept/hem/common/sequencing/chenggrp/pipelines/hg38/kallisto/release_94/Homo_sapiens.GRCh38.cdna.all.fa

t2g file can be found at: https://hemtools.readthedocs.io/en/latest/content/Data/hemtools_data.html


Steps
-----

.. code:: bash

	cat your.fa cDNA.fa > custom_genome.fa

	module load kallisto/0.43.1

	kallisto index -i custom_genome.idx custom_genome.fa

For the t2g file, add a new line specifying your custom gene like below:

::

	target_id	ens_gene	ext_gene
	hgcOPT	hgcOPT	edited_IL2RG


Run diffGenes.py
----------------

diffGenes.py -f fastq.tsv -d design.matrix -g custom -i /home/yli11/dirs/hgcOPT_insulator/Data/Kallisto_index_add_IL2RG/hg19_hgcOPT.idx --gene_info /home/yli11/dirs/hgcOPT_insulator/Data/Kallisto_index_add_IL2RG/hg19.ensembl_v75.t2g


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



