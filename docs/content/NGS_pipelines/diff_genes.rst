RNA-seq: differential gene expression analysis
==============================================

::

	usage: diffGenes.py [-h] [-j JID] -f FASTQ_TSV -d DESIGN_MATRIX
	                    [--strandness STRANDNESS] [--paired] [-g GENOME]
	                    [--nfcore_genome NFCORE_GENOME] [-i INDEX_FILE]
	                    [--gene_info GENE_INFO]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        diffGenes_yli11_2022-11-29)
	  -f FASTQ_TSV, --fastq_tsv FASTQ_TSV
	                        TSV file, 4 columns, read 1, read 2, UID, group ID
	                        (default: None)
	  -d DESIGN_MATRIX, --design_matrix DESIGN_MATRIX
	                        TSV file, 3 columns, group ID, group ID, output_prefix
	                        (default: None)
	  --strandness STRANDNESS
	                        fr: first read forward or rf: first read reverse
	                        (default: None)
	  --paired              if paired is used, then user should only have 2 groups
	                        in the design matrix file and the paired info is
	                        automatically extracted from fastq.tsv based on
	                        ordered group sample list (default: False)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10 (default: hg19)
	  --nfcore_genome NFCORE_GENOME
	                        genome version: hg19, hg38, mm9, mm10 (default: hg38)
	  -i INDEX_FILE, --index_file INDEX_FILE
	                        Kallisto index file (default:
	                        /home/yli11/Data/Human/hg19/index/kallisto/hg19.idx)
	  --gene_info GENE_INFO
	                        gene info t2g file for sleuth (default: /home/yli11/Da
	                        ta/Human/hg19/index/kallisto/hg19.ensembl_v75.t2g)



Summary
^^^^^^^

This pipeline is based on Kallisto - Sleuth.


11/29/2022 Updates: added ``--paired`` for paired test


Input
^^^^^

**1. fastq tsv**

This file contains 4 columns. The first 3 columns are read1.fastq.gz, read2.fastq.gz, and a UID for output. The 4th column is a group ID, which is used for differential gene expression analysis between any two groups.

You can use ``run_lsf.py --guess_input`` to generate the first 3 columns and then add the 4th column manually.

An example is shown below.

::

	1000004_RFR005_S5_R1.fastq.gz	1000004_RFR005_S5_R2.fastq.gz	1000004_RFR005_S5	h1
	1000002_RFR003_S3_R2.fastq.gz	1000002_RFR003_S3_R1.fastq.gz	1000002_RFR003_S3	h1
	1000000_RFR001_S1_R2.fastq.gz	1000000_RFR001_S1_R1.fastq.gz	1000000_RFR001_S1	h1
	1000003_RFR004_S4_R2.fastq.gz	1000003_RFR004_S4_R1.fastq.gz	1000003_RFR004_S4	h2
	1000005_RFR006_S6_R1.fastq.gz	1000005_RFR006_S6_R2.fastq.gz	1000005_RFR006_S6	h2
	1000001_RFR002_S2_R1.fastq.gz	1000001_RFR002_S2_R2.fastq.gz	1000001_RFR002_S2	h2

Paired test
-----------

If user added ``--piared``, then the paired info is assumed to be the sample list in ``fastq.tsv``. In the above example, ``1000004_RFR005_S5`` and ``1000003_RFR004_S4`` will be the same replicate (e.g., ``replicate0``) and ``1000002_RFR003_S3,1000005_RFR006_S6`` is ``replicate1``


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

RNA-seq QC
------

We use ``nf-core/rnaseq`` (https://nf-co.re/rnaseq/usage) for RNA-seq QC. This pipeline provides a very comprehensive QC checks for sequencing quality (fastqc), mapping quality (STAR, RSEM), and gene library quality (pre-seq for library complexity, mapped read category, e.g., exon% vs intron%, visualization of gene qualityfication, heatmaps and PCA plots). Please check out ``{{jid}}/nfcore_RNA_seq_results/multiqc/star_rsem/multiqc_report.html``

Differential gene analysis results
-----------------------------

We generate ``_sleuth`` folder for each comparison specified in the ``design matrix``.

``_sleuth`` contains differential analysis and normalized TPM/read count (ext_count) information for both transcript-level and gene-level.

Fold change is calculated based on both TPM and ext_count, but they should be very similar to each other. TPM is recommended.

Use ``{{output_name}}.transcript.final.combined.tpm.csv`` for transcript level estimation.

Use ``{{output_name}}.gene.final.combined.tpm.csv`` for gene level estimation. Gene level is more accurate.

For volcano plot of differential genes, see :doc:`volcano <../Visualization/volcano_plot>`

For replicate correlation, see ``replicate_correlation`` folder. Pairwise replicate scatter plots based on log2TPM is provided as the pdf files. PCA plot can be found in the html file.

For GO enrichment, pathway analysis, go to ``GO_pathway_analysis`` folder. Enrichment analysis is based on |logFC|>=1 and fdr<=0.05. 

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

Now, there is a much easier way to build index:

::

	(captureC) [yli11@noderome146 gencodev42]$ kb ref ~/Data/Human/hg38/fasta/hg38.main.fa gencode.v42.annotation.gtf.gz -i hg38.gencode42.idx -g hg38.gencode42.t2g -f1 hg38.gencode42.cDNA.fa
	[2022-11-29 11:18:17,508]    INFO [ref] Preparing /home/yli11/Data/Human/hg38/fasta/hg38.main.fa, gencode.v42.annotation.gtf.gz
	[2022-11-29 11:19:34,163]    INFO [ref] Splitting genome /home/yli11/Data/Human/hg38/fasta/hg38.main.fa into cDNA at /research/rgs01/home/clusterHome/yli11/Data/Human/hg38/index/kallisto/gencodev42/tmp/tmpxqkzsshb
	[2022-11-29 11:20:20,737]    INFO [ref] Concatenating 1 cDNAs to hg38.gencode42.cDNA.fa
	[2022-11-29 11:20:21,428]    INFO [ref] Creating transcript-to-gene mapping at hg38.gencode42.t2g
	[2022-11-29 11:20:23,994]    INFO [ref] Indexing hg38.gencode42.cDNA.fa to hg38.gencode42.idx
	(captureC) [yli11@noderome146 gencodev42]$ ll -rht
	total 3.7G
	-rwxr-x--- 1 yli11 chenggrp  48M Oct 19 07:39 gencode.v42.annotation.gtf.gz
	-rwxr-x--- 1 yli11 chenggrp 450M Nov 29 11:20 hg38.gencode42.cDNA.fa
	-rwxr-x--- 1 yli11 chenggrp  20M Nov 29 11:20 hg38.gencode42.t2g
	-rwxr-x--- 1 yli11 chenggrp 3.2G Nov 29 11:28 hg38.gencode42.idx



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

.. code:: bash

	diffGenes.py -f fastq.tsv -d design.matrix -g custom -i /home/yli11/dirs/hgcOPT_insulator/Data/Kallisto_index_add_IL2RG/hg19_hgcOPT.idx --gene_info /home/yli11/dirs/hgcOPT_insulator/Data/Kallisto_index_add_IL2RG/hg19.ensembl_v75.t2g


Reference
^^^^^^

https://chipster.csc.fi/manual/library-type-summary.html

Tutorial
^^^^^^^

.. raw:: html

  <video controls width="690" src="../../_static/diffGenes.mp4#t=0.3"></video>



Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



