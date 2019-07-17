Call IDR peaks given bam files from two replicates
==================================================

::

	usage: idr_peaks.py [-h] [-j JID] -r1 R1_INPUT -r2 R2_INPUT
	                    [--merged_input MERGED_INPUT] [-g GENOME]
	                    [--macs_genome MACS_GENOME]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        idr_peaks_yli11_2019-07-17)
	  -r1 R1_INPUT, --R1_input R1_INPUT
	                        TSV file, 2 columns, treatment, control files for
	                        replicate 1 (default: None)
	  -r2 R2_INPUT, --R2_input R2_INPUT
	                        TSV file, 2 columns, treatment, control files for
	                        replicate 2 (default: None)
	  --merged_input MERGED_INPUT
	                        Not for end-user anymore (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, mm10, mm9 (default: hg19)
	  --macs_genome MACS_GENOME
	                        genome version: hs, mm (default: hs)


Summary
^^^^^^^

IDR peaks are conserved binding peaks that usually can boost motif enrichment. Note that peaks called from individual replicate can be still useful.

In the output, you will receive two emails. One is the link to the GREAT analysis (i.e., peak annotations). The other one is a notification of job completion.

Flowchart
^^^^^^^^^

.. image:: ../../images/idr.png
	:align: center

Input
^^^^^

Please provide the file location to bam files. For single-end data, please use raw bam file (e.g., *.markdup.bam). For paired-end data, please use uniquely mapped de-duplicated bam file (e.g., *.rmdup.uq.bam).

.. note:: Currently, this pipeline doesn't support running multiple samples at the same time. If you have multiple samples, you need to provide the following input files seperately.

**R1 Input**

This is a two-column tsv file (treatment R1 and contol R1). An example is shown below:

::

	/path_to_file/1047954_Hudep2_CTCF_IP_50bp.markdup.bam	/path_to_file/1047955_Hudep2_input_50bp.markdup.bam

**R2 Input**

This is a two-column tsv file (treatment R2 and contol R2). An example is shown below:

::

	/path_to_file/1047954_Hudep2_CTCF_IP_50bp_R2.markdup.bam	/path_to_file/1047955_Hudep2_input_50bp_R2.markdup.bam


Usage
^^^^^

.. code:: bash

	idr_peaks.py -r1 R1_input -r2 R2_input -g hg19 --macs_genome hs


Note that if you are working on mouse genome, you have to change both ``-g`` and ``--macs_genome`` options, for example:

.. code:: bash

	idr_peaks.py -r1 R1_input -r2 R2_input -g mm9 --macs_genome mm

Output
^^^^^^

IDR peaks is shown in ``idr_peaks.bed``

You can also find outputs from homer analysis: ``homer_motifs_result`` and ``idr_peaks.annotated.tsv``




Ref: https://hbctraining.github.io/Intro-to-ChIPseq/lessons/07_handling-replicates-idr.html



