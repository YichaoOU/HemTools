Differential Peaks
==================




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

Please copy (or ``ln -s``) all input bam and peak files to a working directory.

**1. input.tsv **

A tsv file containing 4 columns: bam file, peak file, sample name, group name. ``Group name should always be a substring of sample name.``

::

	A.rmdup.uq.bam	A.rmdup.uq.rmblck.narrowPeak	WT_rep1	WT
	B.rmdup.uq.bam	B.rmdup.uq.rmblck.narrowPeak	WT_rep2	WT
	C.rmdup.uq.bam	C.banana.narrowPeak	KO_abc	KO
	D.rmdup.uq.bam	D.rmdup.uq.rmblck.narrowPeak	KO_xxx	KO



**2. design matrix**

A tsv file containing three columns specifying comparisons. You could do group level comparison or just one sample vs another sample.

.. code:: bash

	WT_rep1	WT_rep2	non_sense
	WT_rep1	KO_xxx	example1
	WT	KO	WT_vs_KO


Usage
^^^^^






Output
^^^^^^

Inside the jid folder, results are provided under each tool's name.



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







