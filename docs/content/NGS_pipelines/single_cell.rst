Single-cell RNA-seq analysis
============================

:: 

	usage: single_cell.py [-h] [-j JID] -f INPUT_LIST [--atac] [-g GENOME]
	                      [--genes GENES]
	                      [--cellranger_refdata CELLRANGER_REFDATA]
	                      [--cellranger_atac_refdata CELLRANGER_ATAC_REFDATA]

	perform 10X single-cell RNA-seq analysis

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        single_cell_yli11_2022-11-21)
	  -f INPUT_LIST, --input_list INPUT_LIST
	                        A list of group name (fastq file prefix). (default:
	                        None)
	  --atac                run atac pipeline (default: False)
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm10. (default: hg38)
	  --genes GENES         Genes to inspect, use Ensembl ID, separated by ,.
	                        (default: ENSG00000213934,ENSG00000196565)
	  --cellranger_refdata CELLRANGER_REFDATA
	                        Not for end-user (default: /research/rgs01/application
	                        s/hpcf/authorized_apps/rhel7_apps/cellranger/refdata
	                        /refdata-cellranger-GRCh38-3.0.0/)
	  --cellranger_atac_refdata CELLRANGER_ATAC_REFDATA
	                        Not for end-user (default: /research/dept/hem/common/s
	                        equencing/chenggrp/pipelines/hg38/cellranger/GRCh38-20
	                        20-A_build/refdata-cellranger-arc-
	                        GRCh38-2020-A-2.0.0.tar.gz)



Summary
^^^^^^^

This pipeline performs gene expression quantification (``cellranger count``) and basic QC. For data integration, see ``scJupyter.py`` 


Input
^^^^^

Put all fastq files in the same working dir.

10X Genomics single-cell RNA-seq data contains ``R1`` and ``R2`` reads. ``R1`` is the barcode information. ``R2`` is the actual 3-end mRNA sequencing result, 90bp.

Your working directory should contain all input fastq files. For example:

::

	Chicken_S4_L001_R1_001.fastq.gz
	Chicken_S4_L001_R2_001.fastq.gz
	Chicken_S4_L002_R1_001.fastq.gz
	Chicken_S4_L002_R2_001.fastq.gz
	Chicken_S4_L003_R1_001.fastq.gz
	Chicken_S4_L003_R2_001.fastq.gz
	Chicken_S4_L004_R1_001.fastq.gz
	Chicken_S4_L004_R2_001.fastq.gz
	Orange_S1_L001_R1_001.fastq.gz
	Orange_S1_L001_R2_001.fastq.gz
	Orange_S1_L002_R1_001.fastq.gz
	Orange_S1_L002_R2_001.fastq.gz
	Orange_S1_L003_R1_001.fastq.gz
	Orange_S1_L003_R2_001.fastq.gz
	Orange_S1_L004_R1_001.fastq.gz
	Orange_S1_L004_R2_001.fastq.gz
	Apple_S2_L001_R1_001.fastq.gz
	Apple_S2_L001_R2_001.fastq.gz
	Apple_S2_L002_R1_001.fastq.gz
	Apple_S2_L002_R2_001.fastq.gz
	Apple_S2_L003_R1_001.fastq.gz
	Apple_S2_L003_R2_001.fastq.gz
	Apple_S2_L004_R1_001.fastq.gz
	Apple_S2_L004_R2_001.fastq.gz
	Banana_S3_L001_R1_001.fastq.gz
	Banana_S3_L001_R2_001.fastq.gz
	Banana_S3_L002_R1_001.fastq.gz
	Banana_S3_L002_R2_001.fastq.gz
	Banana_S3_L003_R1_001.fastq.gz
	Banana_S3_L003_R2_001.fastq.gz
	Banana_S3_L004_R1_001.fastq.gz
	Banana_S3_L004_R2_001.fastq.gz

.. tip:: If you have the fastq files stored in different folders, you can use ``ln -s path_to_fastq_folder/ .`` to create soft links to your fastq files. Do it for each folder, so that you have all fastq files in your working directory.

**input.list**

In the above example, you have 4 groups/patients, namely: Chicken, Orange, Apple, Banana. Then you just have to create an ``input.list`` and put the group name (Case sensitive! Make sure the names are exactly the same as in your fastq files!) line by line, like below:

::

	Chicken
	Orange
	Apple
	Banana


Usage
^^^^^

.. code:: bash

    module load python/2.7.13

    single_cell.py -f input.list

    # for quantify HBG1/HBG2 (100% accurate is not possible)
    single_cell.py -f input.list -g custom --cellranger_refdata /research/dept/hem/common/sequencing/chenggrp/pipelines/hg38/cellranger_arc/hg38_rmHBGnoise

    # HBG1 mask
    single_cell.py -f input.list -g custom --cellranger_refdata /research/dept/hem/common/sequencing/chenggrp/pipelines/hg38/cellranger_arc/GRCh38_HBG1_mask


For single-cell ATAC data, add ``--atac``, only available in hg38:

::

	single_cell.py -f input.list --atac

Output
^^^^^^

cellranger output, see results in the jodID folder. ``*_results``

Report bug
^^^^^^^^^^

.. code:: bash

    $ HemTools report_bug



Old notes
^^^^^




This pipeline generates gene expression table and several figures described as below:

 - Processing single-cell RNA-seq data and quantifying gene expression using ``cellRanger``
 - Removing genes with all zeros

The following are not included in the pipeline yet:

 - plot read cound density for all input samples
 - identify genes with mean read count above a cutoff
 - identify genes with X% of cells containing read count above a cutoff
 - clustermap with gene names (by default cellRanger is Ensembl ID)
 - plot pair-wise gene correlation
 - top expression plot , as well as other plots generated by ``scater``: http://bioconductor.org/packages/release/bioc/vignettes/scater/inst/doc/vignette-qc.html
 - plot mean-variance for all cells and all samples, and put label for user input gene names
 - PCA plot (not implemented), T-SNE plot, UMAP plot (not implemented) (shape by k-means) (not implemented) with color intensity using expression values of a user input gene


Note that Single-cell differential expression analysis is not implemented yet.

.. note:: Available genomes are hg19, hg38, mm10. hg38 and mm10 supports lateset Chromium 3' gene expression library, including V3, V3.1 and V3.2. Hg19 only works with V2. Default genome is hg38.

QC
^^^^^

https://academic.oup.com/bioinformatics/article/35/24/5306/5542946



Gene density plot
^^^^^^^^^




Ribosomal protein reads
^^^^^^^^^^^^^^^^

https://kb.10xgenomics.com/hc/en-us/articles/218169723-What-fraction-of-reads-map-to-ribosomal-proteins-

We have a recent blood scRNA-seq data where the RP reads% is about 30-40% and most DEGs are actually RP proteins.

::

		RP	non-RP
	all genes (count>20)	67	20
	all DEG (count>20)	23	6
	as a percentage	0.343283582	0.3



Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines




















