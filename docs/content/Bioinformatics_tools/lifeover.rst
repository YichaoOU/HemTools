Lift Over Bed or bigWiggle files
===================

::

	usage: liftover.py [-h] -f BED [-o OUTPUT] [-g GENOME] [-c CHAIN_FILE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f BED, --bed BED     bed file for liftover (default: None)
	  -o OUTPUT, --output OUTPUT
	                        output file for liftover (default: liftover.bed)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        Target genome version: hg19, mm10, mm9, hg38 (default:
	                        mm9)
	  -c CHAIN_FILE, --chain_file CHAIN_FILE
	                        genome version: hg19, mm10, mm9, hg38 (default: /home/
	                        yli11/Data/Mouse/chain_files/mm10ToMm9.over.chain.gz)



Summary
^^^^^^^

Given a bed or a bw file, convert the genomic coordinates to a target genome version.

Note that ``-g`` is the **target genome version**. For example, ``-g mm9`` means covert ``mm10`` to ``mm9``.

``--bw`` still has some errors.


Input
^^^^^

Bed or BW file.

Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13 

	liftover.py --bw GSM1708658_Scl_416B.bw -o GSM1708658_Scl_416B.mm9.bw -g mm9

	liftover.py --bed GSM1708658_Scl_416B.bed -o GSM1708658_Scl_416B.mm9.bed -g mm9






























