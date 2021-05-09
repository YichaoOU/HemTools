FIMO motif scanning
========================

::

	usage: motif_scanning.py [-h] [-j JID] -f BED_FILE -m MOTIF_FILE -o OUTPUT
	                         [-p FIMO_CUTOFF] [--fimo_addon FIMO_ADDON]
	                         [-g GENOME] [--genome_fasta GENOME_FASTA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        motif_scanning_yli11_2021-05-06)
	  -f BED_FILE, --bed_file BED_FILE
	                        bed file (default: None)
	  -m MOTIF_FILE, --motif_file MOTIF_FILE
	                        bed file (default: None)
	  -o OUTPUT, --output OUTPUT
	                        output csv (default: None)
	  -p FIMO_CUTOFF, --fimo_cutoff FIMO_CUTOFF
	  --fimo_addon FIMO_ADDON

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, mm10, mm9, hg38 (default: hg19)
	  --genome_fasta GENOME_FASTA
	                        genome version: hs, mm (default:
	                        /home/yli11/Data/Human/hg19/fasta/hg19.fa)


Summary
^^^^^^^

FIMO motif scanning

Doc needs to be updated (5/6/2021)


Input
^^^^^

``FIMO`` requires two input files. 

The first is genome fasta or any fasta files, you can just use ``-g hg19``, the code will then match the corresponding fasta file.

The second input is the motif file in MEME format.


Usage
^^^^

.. code:: bash
	
	hpcf_interactive

	module load python/2.7.13


Output
^^^^^^

motif mapping bed file


