Generate indexed genome, chrom size, and res fragment bed for HicPro analysis
===========

::

	usage: hicpro_genome.py [-h] [-j JID] [--interactive] -g GENOME -f
	                        GENOME_FASTA [-e DIGESTED_ENZYME]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        hicpro_genome_yli11_2020-06-23)
	  --interactive         run pipeline interatively (default: False)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: None)
	  -f GENOME_FASTA, --genome_fasta GENOME_FASTA
	                        please use absolute path (default: None)
	  -e DIGESTED_ENZYME, --digested_enzyme DIGESTED_ENZYME
	                        digested_fragments (default: MboI)

Summary
^^^^^^^

Given any genome fasta file and a genome name, this program will create all the necessary inputs for HiC-Pro. 


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	hicpro_genome.py -g hg19_20copy -f /home/yli11/dirs/blood_regulome/chenggrp/Projects/hgcOPT_insulator/Data/hg19_new_genome/hg19_20copy.fa


Output
^^^^^^

Bowtie2 index, chrom size, and restriction enzyme bed file are inside $jid folder.


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines




