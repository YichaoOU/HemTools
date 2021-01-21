Boxplots to compare signal differences between overlap and non-overlap regions
=====================================

Motivation
^^^^^^^^^^

In a project, we found a TF ChIP-seq signal is much more stronger in closed chromatin than in open chromatin and only 50% IDR peaks overlap with ATAC-seq peaks.

Summary
^^^^^^^

This analysis aims to make a boxplot to show if there is a significant differences between overlap regions (e.g., peaks in open chromatin) and non-overlap regions (e.g., peaks in closed chromatin).

Usage
^^^^^

.. code:: bash

	run_lsf.py -f input.tsv -p bed_overlap_signal


Input
^^^^^

copy all input files (narrowPeak and bw files) into your working dir.

4 columns tsv file: chip-seq narrowPeak file, baseline bed file (e.g., ATAC-seq peak file), chip-seq bw file, sample name

Examples:

::

	1047954_Hudep2_CTCF_IP.vs.1047955_Hudep2_input.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	Hudep2_ATAC.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	1047954_Hudep2_CTCF_IP.vs.1047955_Hudep2_input.rmdup.uq.rmchrM_FE.bw
	H2_CTCF
	1151778_Hudep2_GATA1.vs.1047955_Hudep2_input.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	Hudep2_ATAC.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	1151778_Hudep2_GATA1.vs.1047955_Hudep2_input.rmdup.uq.rmchrM_FE.bw
	H2_GATA1_rep1
	H2A_nfix.vs.H2A_input.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	Hudep2_ATAC.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	H2A_nfix.vs.H2A_input.rmdup.uq.rmchrM_FE.bw
	H2_NFIX
	1151779_Hudep2_GATA1.vs.1047955_Hudep2_input.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	Hudep2_ATAC.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	1151779_Hudep2_GATA1.vs.1047955_Hudep2_input.rmdup.uq.rmchrM_FE.bw
	H2_GATA1_rep2
	HUDEP2_LRF.vs.HUDEP2_input.markdup.uq_peaks.rmblck.narrowPeak
	Hudep2_ATAC.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	HUDEP2_LRF.vs.HUDEP2_input.markdup.uq_FE.bw
	H2_LRF
	1678570_MW119_P8_NFIX.vs.1678571_MW119_P8_Input.markdup.uq_peaks.rmblck.narrowPeak
	HPC5_ATAC.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	1678570_MW119_P8_NFIX.vs.1678571_MW119_P8_Input.markdup.uq_FE.bw
	HPC5_NFIX_rep1
	1678572_MW120_P13_NFIX.vs.1678573_MW120_P13_Input.markdup.uq_peaks.rmblck.narrowPeak
	HPC5_ATAC.rmdup.uq.rmchrM_peaks.rmblck.narrowPeak
	1678572_MW120_P13_NFIX.vs.1678573_MW120_P13_Input.markdup.uq_FE.bw
	HPC5_NFIX_rep2



Output
^^^^^^

each row produces a boxplot and a csv file contaning the signal values for each peak.

.. image:: ../../images/signal_test.PNG
	:align: center

