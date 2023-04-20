Homer motif enrichment analysis
========================

::

	usage: homer_motif_scanning.py [-h] [-j JID] -f PEAK_LIST [-m MOTIF_FILE]
	                               [-sub MOTIF_SUBSET] [-g GENOME]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        homer_motif_scanning_yli11_2020-07-28)
	  -f PEAK_LIST, --peak_list PEAK_LIST
	                        peak_list relative or abs path (default: None)
	  -m MOTIF_FILE, --motif_file MOTIF_FILE
	                        homer motif file (default: /home/yli11/Data/Motif_data
	                        base/Human/homer_format_all.motifs)
	  -sub MOTIF_SUBSET, --motif_subset MOTIF_SUBSET
	                        subset motifs to annotate (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. currently, only
	                        hg19 is available (default: hg19)


Summary
^^^^^^^

Motif enrichment analysis by Homer.

Default is to use all homer motif (very large collection). You can also use a subset by: (1) provide your own motif file (2) or do a string match in all motifs (see usage)


Input
^^^^^

A list of bed files.

::

	[yli11@nodecn126 gain]$ ls
	B_cell_gain.bed  Ery_cell_gain.bed  mono_cell_gain.bed  T_cell_gain.bed
	[yli11@nodecn126 gain]$ ls *.bed > peak.list

Usage
^^^^

.. code:: bash
	
	hpcf_interactive

	module load python/2.7.13

	homer_motif_scanning.py -f peak.list -sub MA0139.1,MA0652.1,MA0597.1,MA0080.4,MA0035.3,MA0140.2,MA0694.1,GATA:SCL -g hg19

Output
^^^^^^

The output is the same to homer motif discovery.

Summary files
-------------


Please find ``nlogP.summary.csv`` for log P-value table and ``Target_percent.summary.csv`` for %Target.

