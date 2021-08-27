Differential Peaks
==================

::

	usage: diffPeaks.py [-h] [-j JID] -f INPUT_TSV -d DESIGN_MATRIX
	                    [--guess_input] [--MAnorm_PE_flag] [--continue_homer_diff]
	                    [-g GENOME] [-s GENOME_CHROM_SIZE]
	                    [--skip_chrom_size SKIP_CHROM_SIZE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        diffPeaks_yli11_2020-10-18)
	  --guess_input         Let the program generate the input files for you,
	                        won't be correct, but should be helpful (default:
	                        False)
	  --MAnorm_PE_flag      whether input is paired-end data (default: False)
	  --continue_homer_diff
	                        Not for end-user. If homer tag is available, just run
	                        homer diff (default: False)

	required named arguments:
	  -f INPUT_TSV, --input_tsv INPUT_TSV
	                        4 column tsv, bam file, peak file, sample name, sample
	                        group (default: None)
	  -d DESIGN_MATRIX, --design_matrix DESIGN_MATRIX
	                        3 column tsv for design matrix (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        chrom size. (default: hg19)
	  -s GENOME_CHROM_SIZE, --genome_chrom_size GENOME_CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Human/hg19/anno
	                        tations/hg19.chrom.sizes.sorted)
	  --skip_chrom_size SKIP_CHROM_SIZE
	                        for homer chrom error, not for end-user. chrome size
	                        (default: /home/yli11/Data/Human/hg19/annotations/hg19
	                        .chrom.sizes)



Get started
^^^^^^^^

1. Before start, check data quality and replicate correlation. Data quality is available is HemTools html or pdf report. Important metrics include number of mapped reads, mapping rate, number of peaks, FRiP, Qtag (chip-seq). Replicate correlation can be checked using :doc:`plot_bw_corr.py <../Visualization/bw_corr>`

2. Follow the instructions below to perform differential peak analysis. This pipeline uses multiple tools to call differential peaks. ``DESEQ2`` tends to give the most stringent results (i.e., less differential peaks). This result is in ``homer_deseq2_results`` (output folder). 

3. Normalized signals for each sample and each group (bw files) are provided in the job id folder. 

4. (Visualization) Inside ``homer_deseq2_results``, you can use ``*_homer_deseq2.all.bed`` for volcano plot. Together with the signal files above, you can use :doc:`create_tracks.py <../Gallery/create_tracks>` to automatically upload these bed files and bw files to protein paint.


Summary
^^^^^^^

As of 9/14/2020, tested the following tools

1. our own diff pipeline based on DESEQ2
2. Homer getDifferentialPeaksReplicates.pl DESEQ2 or EdgeR
3. MAnorm
4. Homer getDifferentialPeaks
5. MACS2 bdgdiff
6. Thor/ODIN

These tools or pipelines are ranked by their stringency (i.e. number of reported diff peaks). The DESEQ2 based pipelines are the most stringent. The least strigent or the most sensitive tools are MACS2 or Thor/ODIN. We provide all the results, depends on how many diff peaks you expect to see, you can select the results from that tool.

(1) and (2) tools requires replicates, these are the most strigent probably because the variance within replicate can significantly affect the results. All other tools will merge the replicates. 

Make sure the input data are in high quality. Low quality data is OK, then diffpeaks should only be applied to the called peaks, not whole genome wide.

Our ensemble diff peak calling pipeline integrates: homer deseq2, homer diffpeak, MAnorm, and Thor.


Input
^^^^^

Usually people use markdup.uq bam for differential analysis. You can also use rmdup.uq bam.

Please copy (or ``ln -s``) all input bam and .bai (index files) and peak files to a working directory. Peak files have to be at least 4 columns (narrowPeak format is one of the examples.)

.. note:: DO NOT use absolute path in the input.tsv. Just use file name.

** 1. input.tsv **

A tsv file containing 4 columns: bam file, peak file, sample name, group name. ``Sample name should start with group name``. This requirement helps the program to perform sample-level and group-level comparison in case you only have one sample in a group. Sample name should be unique. Sample name can be the same as group name. 



::

	A.rmdup.uq.bam	A.rmdup.uq.rmblck.narrowPeak	WT_rep1	WT
	B.rmdup.uq.bam	B.rmdup.uq.rmblck.narrowPeak	WT_rep2	WT
	C.rmdup.uq.bam	C.banana.narrowPeak	KO_abc	KO
	D.rmdup.uq.bam	D.rmdup.uq.rmblck.narrowPeak	KO_xxx	KO



** 2. design matrix**

A tsv file containing three columns specifying comparisons. You could do group level comparison or just one sample vs another sample, the comparison name (3rd column) should be unique.

.. code:: bash

	WT_rep1	WT_rep2	non_sense
	WT_rep1	KO_xxx	example1
	WT	KO	WT_vs_KO


Usage
^^^^^


.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	diffPeaks.py -f input.tsv -d design.tsv -g mm9 --MAnorm_PE_flag 

Paired-end data needs to add ``--MAnorm_PE_flag`` option. 

PE data can be analyzed together with SE data.

.. code:: bash

	diffPeaks.py -f input.tsv -d design.txt -g hg19 --merge_distance "-1"


Output
^^^^^^

Inside the jid folder, results are provided under each tool's name.

::

	homer_deseq2_results
	THOR_results
	homer_diff_results
	MAnorm_results
	*.bw

``*bw`` the bw files inside the jid folder is homer sequencing depth normalized bw files, consistent with homer results.

BW file is normalized to #reads per 10 million reads.

::

	-norm <#> : Normalize the total number of reads to this number, default 1e7.  This means that tags from an experiment with only 5 million mapped tags will count for 2 tags apiece.


homer_deseq2_results
^^^^^^^^^^^^^^

4th column is LFC
5th column is FDR

``*.all.bed`` contains the all the peaks.

``*LFC_1.FDR_05.bed`` contains the peaks with LFC>=1 and FDR<=0.05

Sign of LFC is based on the input design file (first column vs second column). 


Other Tools (old notes)
^^^^^

Parameter: with/w.o. replicates

::
	Baseline – unique peaks
	macs2 bdgdiff
	DESEQ2, edgeR-robust
	MAnorm
	ODIN (is replaced by THOR)
	Homer
	Epic2
	THOR
	MultiGPS
	RSEG

The following tools are only applicable with replicates:
::
	diffBind
	Csaw
	ChIPComp

Not tested
::
	GenoGAM
	diffReps



Video tutorial
^^^^^^^^^^^^^


In the video, I forgot to copy .bai files. 

.. raw:: html

  <video controls width="690" src="../../_static/diffPeaks_usage.mp4#t=0.3"></video>






