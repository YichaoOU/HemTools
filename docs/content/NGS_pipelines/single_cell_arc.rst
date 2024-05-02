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


HBG1 HBG2 quantification
^^^^^^^^^^^^^^^

Most RNA-seq pipeline discards multi-mapped reads, same in cellranger.

Accurate quatification of HBG1 and HBG2 using 90bp-length reads is impossible. Only about 50% of the reads can be uniquely assigned to HBG1 or HBG2. This number is based on a simple raw reads string match to HBG1/HBG2 cDNA. Interestingly, I found cellranger can still assign multi-mapped reads to either HBG1 or HBG2, suggesting these reads are uniquely mapped but in fact they are not (talked to their technical support, no clear answers). 

For our department usage, I suggest we mapped to both ``hg38_rmHBGnoise`` and ``GRCh38_HBG1_HBA1_mask`` reference. 

- ``hg38_rmHBGnoise``: removed 2 transcripts overlapped with HBG2 from the original cellranger index, causing multi-assigned reads to be discarded and thus, HBG2 expression dropped. This index should give you an ``accurate relative differences between HBG1 and HBG2`` (not sure about HBA1 and HBA2). But the sum ``HBG`` expression is not accurate because of discard of multi-mapped reads.

- ``GRCh38_HBG1_HBA1_mask``: masked HBG1 and HBG2 gene body (including 5- and 3-UTR), in order to re-use multi-mapped reads. But still a small amount of reads can be mapped to HBG1 or HBG2 (cellranger still assign nearby intergenic reads to HBG1 or HBA1). To get ``accurate quantificaiton of HBG and HBA expression``, analysis needs to add up HBG1 and HBG2, HBA1 and HBA2 read counts.

This pipeline automatically mapped data to the above two references, output folder contains the reference information.

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

