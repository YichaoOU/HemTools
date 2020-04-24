Motif scanning using consensus sequence
======================


::

	usage: cas_motif.py [-h] [-j JID] -f INPUT [-n NUM_MISMATCHES] [-g GENOME]
	                    [--chr_fa CHR_FA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        cas_motif_yli11_2020-04-23)
	  -f INPUT, --input INPUT
	                        one motif sequence (default: None)
	  -n NUM_MISMATCHES, --num_mismatches NUM_MISMATCHES
	                        Number of allowed mis-matches in the gRNA, excluding
	                        PAM sequence (default: 0)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. currently, only
	                        hg19 is available (default: hg19)
	  --chr_fa CHR_FA       This will be automatically changed with -g option
	                        (default: /home/yli11/Data/Human/hg19/fasta/chr)



Summary
^^^^^^^

Motif scanning using consensus sequence, e.g., ``CAGGTGNNNNNNNNGATA``

I found cas-offinder is the fastest and most accurate patter matching tool.

I used to use PatScan, but it can miss some matches (for many years, I thought it was an accurate tool).



Output
^^^^^^

match.bed.sorted


Usage
^^^^^


.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	cas_motif.py -f CAGGTGNNNNNNNNGATA -j gap8

