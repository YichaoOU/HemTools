Convert MaGeCK RRA sgRNA results to bw tracks
==========================


::

	usage: cas_offinder.py [-h] [-j JID] -f INPUT [-n NUM_MISMATCHES] [--add_PAM]
	                       [--PAM_seq PAM_SEQ] [-g GENOME] [--chr_fa CHR_FA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        cas_offinder_yli11_2019-07-17)
	  -f INPUT, --input INPUT
	                        a list of gRNA sequences (default: None)
	  -n NUM_MISMATCHES, --num_mismatches NUM_MISMATCHES
	                        Number of allowed mis-matches in the gRNA, excluding
	                        PAM sequence (default: 2)
	  --add_PAM             if PAM sequence is not included in your gRNA, please
	                        add this option. (default: False)
	  --PAM_seq PAM_SEQ     specify the PAM sequence, e.g., NGG. (default: NGG)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. currently, only
	                        hg19 is available (default: hg19)
	  --chr_fa CHR_FA       This will be automatically changed with -g option
	                        (default: /home/yli11/Data/Human/hg19/fasta/chr)

Summary
^^^^^^^

Generate LFC and FDR tracks.


Input
^^^^^

1. Mageck RRA sgRNA results

2. gRNA bed file


Usage
^^^^^


.. code:: bash

	Mageck2bw.py -f HbF_RRA_results.sgrna_summary.txt -b gRNA.loci307.bed --cas9 -o HbF


Output
^^^^^^


::

	-rwxrwx--- 1 yli11 chenggrp  254K Mar 10 16:48 HbF.FDR.bdg
	-rwxrwx--- 1 yli11 chenggrp  205K Mar 10 16:48 HbF.LFC.bdg
	-rwxrwx--- 1 yli11 chenggrp  152K Mar 10 16:48 HbF.FDR.bw
	-rwxrwx--- 1 yli11 chenggrp  158K Mar 10 16:48 HbF.LFC.bw



Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



























