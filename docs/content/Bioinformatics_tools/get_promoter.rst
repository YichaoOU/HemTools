Extract user-defined gene promoter from refseq TSS database
===========================================================

::

	usage: get_promoter.py [-h] -f INPUT_LIST [-u U] [-d D] [-o OUTPUT]
	                       [-g GENOME] [--refseq_TSS REFSEQ_TSS]
	                       [--gene_name_db GENE_NAME_DB]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT_LIST, --input_list INPUT_LIST
	                        gene list, any type of Entrez ID, Ensemble Gene ID,
	                        Ensemble Transcript ID, gene name (default: None)
	  -u U                  upstream bp (default: 1000)
	  -d D                  downstream bp (default: 200)
	  -o OUTPUT, --output OUTPUT
	                        output bed file name (default:
	                        get_promoter_yli11_2019-12-10.bed)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  --refseq_TSS REFSEQ_TSS
	                        refseq_TSS (default: /home/yli11/Data/Human/hg19/annot
	                        ations/hg19.tss.refseq.bed.gz)
	  --gene_name_db GENE_NAME_DB
	                        gene_name_db (default: /home/yli11/Data/Human/hg19/ann
	                        otations/gene_id_name_all.conversion)


Summary
^^^^^^^

Currently only work in hg19.


Input
^^^^^

A list of gene names.

::

	HBB
	TP53

Parameters
^^^^^^^^^^

``-u`` number of bp extending from the upstream of TSS

``-d`` number of bp extending from the downstream of TSS


Output
^^^^^^

Output file name is ``get_promoter_USER_DATE.bed``

::

	==> get_promoter_yli11_2019-12-10.bed <==
	chr11	5248101	5249301	HBB	0	-


Usage
^^^^^

by default ``-u 1000 -d 200``

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	module load bedtools

	get_promoter.py -f genes.list












