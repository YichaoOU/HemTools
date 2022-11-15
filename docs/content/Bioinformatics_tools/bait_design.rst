General bait design
======================


::

	usage: bait_design.py [-h] [-j JID] -f INPUT_BED [-l BAIT_LENGTH] [--src SRC]
	                      [-g GENOME] [--genome_fasta GENOME_FASTA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        bait_design_yli11_2022-03-08)
	  -f INPUT_BED, --input_bed INPUT_BED
	                        bed file 4 column (default: None)
	  -l BAIT_LENGTH, --bait_length BAIT_LENGTH
	                        bait_length (default: 120)
	  --src SRC             bait_length (default:
	                        /home/yli11/Programs/BaitsTools/bin/baitstools)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10, custom. By
	                        default, specifying a genome version will
	                        automatically update index file, black list, chrom
	                        size and effectiveGenomeSize, unless a user explicitly
	                        sets those options. (default: hg19)
	  --genome_fasta GENOME_FASTA
	                        genome fasta file (default:
	                        /home/yli11/Data/Human/hg19/fasta/hg19.fa)



Summary
^^^^^^^

Input a bed file to look for baits. Steps include: (1) general all 120bp baits with stepsize of 50. (2) BLAT all baits to check multi-hits (3) baittools to check for GC and melting TM.


Input
^^^^^

::

	chr11	5271034	5271266	HBG1
	chr11	5248167	5248406	HBB


Output
^^^^^^


::



Usage
^^^^^


::

	module load python/2.7.13
	bait_design.py -f rick.bed


