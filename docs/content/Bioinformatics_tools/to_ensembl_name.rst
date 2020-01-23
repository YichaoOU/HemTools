Extract Ensembl Gene Name and IDs given IDs or names from any databases
===========================================================

::

	usage: to_ensembl_gene_name.py [-h] -f INPUT [-o OUTPUT] [-g GENOME]
	                               [--gene_db_UCSC GENE_DB_UCSC]
	                               [--gene_db_HGNC GENE_DB_HGNC]
	                               [--gene_name_db GENE_NAME_DB]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT, --input INPUT
	                        a list of gene ids or gene names (default: None)
	  -o OUTPUT, --output OUTPUT
	                        output bed file name (default:
	                        to_ensembl_gene_name_yli11_2020-01-23)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  --gene_db_UCSC GENE_DB_UCSC
	                        gene_name_db (default: /home/yli11/Data/Human/hg19/UCS
	                        C_table_browser/complete)
	  --gene_db_HGNC GENE_DB_HGNC
	                        gene_name_db (default: /home/yli11/Data/Human/hg19/UCS
	                        C_table_browser/HGNC_complete)
	  --gene_name_db GENE_NAME_DB
	                        gene_name_db (default: /home/yli11/Data/Human/hg19/ann
	                        otations/hg19.ensembl_v75.gene_name.db)


Summary
^^^^^^^

Currently only work for hg19. Interesting find: SMIM11 gene has definitions in both hg19 and hg38. But SMIM11B is only defined in hg38.

``This program could take a long time!``

Since our program searchs matches in multiple databases, it may take some time to get your results.


Input
^^^^^

A list of gene names or gene ids from any databases (e.g., HGNC, NCBI Entrez, etc.).

::

	HBB
	TP53

Parameters
^^^^^^^^^^

No parameters.


Output
^^^^^^

Output file name is ``to_ensembl_gene_name_USER_DATE.list``

::

	==> to_ensembl_gene_name_yli11_2020-01-23.for_get_promoter_py.list <==
	C12orf5

	==> to_ensembl_gene_name_yli11_2020-01-23.gene_id_name_mapping.csv <==
	query_name,Ensembl_id,Ensembl_name
	SMIM11B,ENSG00000273590,
	TIGAR,ENSG00000078237,C12orf5
	TIGAR,ENST00000179259,C12orf5

	==> to_ensembl_gene_name_yli11_2020-01-23.not_found.list <==
	SMIM11B


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	to_ensembl_gene_name.py -f input.list




