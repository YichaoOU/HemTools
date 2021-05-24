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

This output can be uploaded to protein paint using the following command:

::

	module load htslib

	bed_to_bedjs_withName_Color.py match.bed.sorted 1

The associated json file will look like below:

::

	{
	"type":"bedj",
	"name":"GATA_Ebox(8-9) motif",
	"file":"PATH/match.bed.sorted.bedjs.sorted.gz",
	"stackheight":20,
	"stackspace":1
	},



Usage
^^^^^


.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	cas_motif.py -f CAGGTGNNNNNNNNGATA -j gap8


Advanced usage: similar to BLAT, find location for any sequence
^^^^^^^^^^^^^

Save your sequence in a file (e.g., ``input.list``), one sequence per line.


.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	for i in `cat input.list`;do cas_motif.py -f $i -g custom --chr_fa $PWD/chr11_INS7_paternal.fa;done

The ``matches.bed.sorted`` is the output bed file. ``test.fa`` is a double check for the location using bedtools.




