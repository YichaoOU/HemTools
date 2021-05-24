Lift Over Bed or bigWiggle files
===================

::

	usage: liftover.py [-h] [-o OUTPUT] (--bed BED | --bw BW) [-g GENOME]
	                   [-s CHROM_SIZE] [-c CHAIN_FILE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -o OUTPUT, --output OUTPUT
	                        output file for liftover (default: liftover.bed)
	  --bed BED             input bed file (default: None)
	  --bw BW               Input bw file (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        Target genome version: hg19, mm10, mm9, hg38 (default:
	                        mm9)
	  -s CHROM_SIZE, --chrom_size CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Mouse/mm9/annot
	                        ations/mm9.chrom.sizes)
	  -c CHAIN_FILE, --chain_file CHAIN_FILE
	                        genome version: hg19, mm10, mm9, hg38 (default: /home/
	                        yli11/Data/Mouse/chain_files/mm10ToMm9.over.chain.gz)



Summary
^^^^^^^

Given a bed or a bw file, convert the genomic coordinates to a target genome version.

Note that ``-g`` is the **target genome version**. For example, ``-g mm9`` means covert ``mm10`` to ``mm9``.


Input
^^^^^

Bed or BW file.

You can have any number of columns in the bed file. Only chr, start, end columns will be used. Other columns will just stay as before in the output.

Usage
^^^^^

.. code:: bash

	hpcf_interactive.sh

	module load python/2.7.13 

	liftover.py --bw GSM1708658_Scl_416B.bw -o GSM1708658_Scl_416B.mm9.bw -g mm9

	liftover.py --bed GSM1708658_Scl_416B.bed -o GSM1708658_Scl_416B.mm9.bed -g mm9


For custom genome
^^^^^^^^

.. code:: bash

	hpcf_interactive.sh

	module load python/2.7.13 

	liftover.py --bw input.bw -o output.hg19.bw -g custom -c /research/dept/hem/common/sequencing/chenggrp/Phil_custom_genome/d13nt_custom_genome/back_to_hg19.chain -s hg19_main_chrom_size

	liftover.py --bed input.bed -o output.mm9.bed -g custom -c /PATH/TO/CUSTOM_CHAIN_file


``-s`` is not required for ``--bed`` option.




Liftover gff gtf
^^^^^^^^


	module load crossmap/0.2.4
	CrossMap.py gff ~/dirs/genome_browser/yli11/hg19_20copy/hg19_to_20copy.chain hg19.ncbiRefSeq.gtf hg19_20copy.refseq.gtf



	sed -i "s/;  /; /" hg19_20copy.refseq.gtf

	/research/rgs01/resgen/legacy/gb_customTracks/tp/utils/














