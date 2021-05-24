BedGraph to BigWiggle
======================


::

	usage: bdg_to_bw.py [-h] [-j JID] -f BDG_FILES [--data_frame] [-g GENOME]
	                    [-s CHROM_SIZE]

	bdg to bw

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        bdg_to_bw_yli11_2019-10-10)
	  -f BDG_FILES, --bdg_files BDG_FILES
	                        bdg file list (default: None)
	  --data_frame          The input is a table, not bdg file list, index and
	                        header are required in this data frame (default:
	                        False)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -s CHROM_SIZE, --chrom_size CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Human/hg19/anno
	                        tations/hg19.chrom.sizes)



Summary
^^^^^^^

Convert bedGraph files to bigWiggle files given genome version. Default is hg19.

Input
^^^^^

A list of bdg files.

::

	input.list
	----------

	CADD.norm.bdg
	DeepSEA.norm.bdg
	EBM_FDR.norm.bdg

Output
^^^^^^

BigWiggle files will be generated in the jid folder.

Usage
^^^^^


.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	bdg_to_bw.py -f input.list

















