Creating facet table for protein paint
===============


::


	usage: get_facet_table.py [-h] [-o OUTPUT] -s SAMPLE_LIST -f FEATURE_LIST -p
	                          PREFIX [-n NAME]

	optional arguments:
	  -h, --help            show this help message and exit
	  -o OUTPUT, --output OUTPUT
	                        output file (default: my_table.json)
	  -s SAMPLE_LIST, --sample_list SAMPLE_LIST
	                        table rows, a list of samples, these are supposed to
	                        be folder names, one column (default: None)
	  -f FEATURE_LIST, --feature_list FEATURE_LIST
	                        table columns, map file name to specific feature name,
	                        and file type, 3 columns (default: None)
	  -p PREFIX, --prefix PREFIX
	                        prefix to add to the file location (default: None)
	  -n NAME, --name NAME  facet name (default: my_table)



Facet Table (Please read)
^^^^^^

It's important to understand the specific format that protein paint requires.

The facet table is essentially a 2D table for user to select data. Each row is a sample, e.g., a specific cell type. Each column is a feature, e.g., a specific TF or histone, or ATAC-seq, or same TF data with different filters, such as rmdup.bw or rmdup.uq.bw or FE.bw


Input
^^^^^

This program assumes such input folder structure.

The current working dir (where you run this program) contains ``N`` sample folders, these N sample folder names are specified in ``samples.list``

::

	[yli11@nodecn202 per_dataset]$ head samples.list 
	AG10803-DS12374
	AoAF-DS13513
	CD19+-DS17186
	CD20+-DS18208
	GM06990-DS7748
	GM12865-DS12436
	H7-hESC-DS11909
	HA-h-DS15192
	HA-sp-DS14790
	HAEpiC-DS12663


In each sample folder, it has the bw files or bed files or (the following are not supported yet) hic files, bedpe files, etc. Files in each sample folder are better to use some shared names (not requred by the program, but it makes your ``features.tsv`` simpler). The ``features.tsv`` is a 3-col tsv file that contains feature_name, file_name and file_type. Example shown below:

:: 

	EXP_cut	interval.all.exp.bw	bw
	footprint_bp_pval_lnpval	interval.all.lnpval.bw	bw
	footprint_bp_pval_fpr	interval.all.fpr.bw	bw
	OBS_cut	interval.all.obs.bw	bw


Usage
^^^^^

::

	module load python/2.7.13

	cd /home/yli11/dirs/genome_browser/yli11/atac_footprint/public_DNase_data/per_dataset

	python get_facet_table.py -s samples.list -f features.tsv -p yli11/atac_footprint/public_DNase_data/per_dataset -n ENCODE_footprint


``-n`` is the facet table name

``-p`` is the prefix added to the file path (protein paint use a relative path)


