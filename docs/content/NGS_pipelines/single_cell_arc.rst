Single-cell multiomc analysis
============================



Input
^^^^

Create ``library.csv`` for each sample like below. The 3 columns are ``fastqs,sample,library_type``. The first column is the path. The 2nd column is the fastq file prefix. The last column is library type.

::

	==> PD1.csv <==
	fastqs,sample,library_type
	/home/yli11/dirs/hem_seq/chenggrp/pdoerfler_single-cell/pdoerfler_10XscRNAseq/weissgrp_286254_10XscRNAseq-1,PD1,Gene Expression
	/home/yli11/dirs/hem_seq/chenggrp/pdoerfler_single-cell/pdoerfler_10XscATACseq/weissgrp_286255_10x_Other_workflows-1,PD1,Chromatin Accessibility

	==> PD2.csv <==
	fastqs,sample,library_type
	/home/yli11/dirs/hem_seq/chenggrp/pdoerfler_single-cell/pdoerfler_10XscRNAseq/weissgrp_286254_10XscRNAseq-1,PD2,Gene Expression
	/home/yli11/dirs/hem_seq/chenggrp/pdoerfler_single-cell/pdoerfler_10XscATACseq/weissgrp_286255_10x_Other_workflows-1,PD2,Chromatin Accessibility

	==> PD3.csv <==
	fastqs,sample,library_type
	/home/yli11/dirs/hem_seq/chenggrp/pdoerfler_single-cell/pdoerfler_10XscRNAseq/weissgrp_286254_10XscRNAseq-1,PD3,Gene Expression
	/home/yli11/dirs/hem_seq/chenggrp/pdoerfler_single-cell/pdoerfler_10XscATACseq/weissgrp_286255_10x_Other_workflows-1,PD3,Chromatin Accessibility

	==> PD4.csv <==
	fastqs,sample,library_type
	/home/yli11/dirs/hem_seq/chenggrp/pdoerfler_single-cell/pdoerfler_10XscRNAseq/weissgrp_286254_10XscRNAseq-1,PD4,Gene Expression
	/home/yli11/dirs/hem_seq/chenggrp/pdoerfler_single-cell/pdoerfler_10XscATACseq/weissgrp_286255_10x_Other_workflows-1,PD4,Chromatin Accessibility


Create input.list as sample name list

::

	PD1
	PD2
	PD3
	PD4

Note that ``PD1`` correspond to the file ``PD1.csv``.



Code to automatically generate ``input.list``.
--------------------------------------

Usually the data given to us is seprated into different folders for different samples. To use our code, you need to put all the RNA fastq in one folder and all the ATAC fastq in one folder. This can be done using ``ln -s``.

::

	mkdir pdoerfler_10XscRNAseq_rep2

	cd pdoerfler_10XscRNAseq_rep2

	ln -s ../weissgrp_298284_10XscRNAseq-*/*/*gz .

	ls *L001_I1*gz

Create sample ID to sample table tsv file like below using sublime text

::

	2593900	PD1
	2593903	PD5
	2593906	PD_PBMC1
	2593901	PD2
	2593904	PD_thal1
	2593907	PD_PBMC2
	2593902	PD3
	2593905	PD_thal2

Then

::

	module load python/3.7.0

	cellranger_rename_fastq.py label.tsv > run.sh

	bash run.sh

	ll -rht

	RNA=$PWD

You will find the fastq files are renamed. Do the same thing for the ATAC library. Save the ATAC data directory as ``DNA=$PWD``

Create a working directory ``rep2_data_analysis``.

::

	mkdir rep2_data_analysis

	cd  rep2_data_analysis

	cp $DNA/label.tsv .

	cellranger_create_library.py $RNA $DNA label.tsv


Usage
^^^^^


::

	module remove python/3.7.0

	module load python/2.7.13
	
	run_lsf.py -f input.list -p single_cell_arc



Default genome
^^^^^^^^^^^^^^

``GRCh38_HBG1_mask``

The HBG1 gene body and 400bp promoter is masked in the default hg38 genome because ATAC-seq pipeline removes multi-mapped reads

