Assigning features to a bed file.
=============


::

	usage: assign_targets_multi.py [-h] -q QUERY_BED [-tss TSS_BED]
	                               --epi_file_list EPI_FILE_LIST [-d1 D1] [-d2 D2]
	                               [-d3 D3] [-o OUTPUT] [--label LABEL]

	optional arguments:
	  -h, --help            show this help message and exit
	  -q QUERY_BED, --query_bed QUERY_BED
	                        3 column bed file, additional columns are OK, but will
	                        be ignored (default: None)
	  -tss TSS_BED, --tss_bed TSS_BED
	                        4 column bed file, the 4th column should be gene name,
	                        should match to the gene name in DEG file (if
	                        supplied). Additional columns are OK, but will be
	                        ignored (default: None)
	  --epi_file_list EPI_FILE_LIST
	  -d1 D1                extend query bed for intersection (default: 0)
	  -d2 D2                extending tss for intersection (default: 2000)
	  -d3 D3                extending epi for intersection (default: 0)
	  -o OUTPUT, --output OUTPUT
	                        output intermediate file (default: output)
	  --label LABEL         prefix for the file (default: TFBS)



Summary
^^^^^


This is one of the tools in the target gene assignment workflow, see :doc:`tf_target_finder pipeline <tf_target_finder>` for more details.

Assigned targets will be appended as new columns to the input bed file.

Ref: https://github.com/YichaoOU/TF_target_finder


Input
^^^^^

1. query bed file

A bed file with any number of columns. But the first 3 columns should be chr, start, end.

2. TSS annotation bed file

hg19: /home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed 

3. a list of features (bed format: chr, start, end, feature_name)

Use case 1: assigning target genes
^^^^^

For promoter capture HiC data, see :doc:`hg19 pc-HiC <../Data/catureC_pcHiC>`.


.. code:: bash

	hpcf_interative.sh

	module load conda3

	source activate /home/yli11/.conda/envs/py2

	assign_targets_multi.py -q input.bed -tss /home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed --epi_file_list pcHIC.list -o input.bed.assigned_targets.bed

Use case 2: assigning motifs
^^^^^

.. code:: bash

	hpcf_interative.sh

	module load conda3

	source activate /home/yli11/.conda/envs/py2

	assign_targets_multi.py -q input.bed -tss /home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed --epi_file_list /path/to/motif.list -o input.bed.assigned_targets.bed



For hg19, please use: 

.. code:: bash

	assign_targets_multi.py -q input.bed -tss /home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed --epi_file_list /home/yli11/Data/Human/hg19/motif_mapping/motif.list -o input.bed.assigned_targets.bed


For hg38, please use: ``--epi_file_list /path/to/motif.list``

.. code:: bash

	assign_targets_multi.py -q input.bed -tss /home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed --epi_file_list /home/yli11/Data/Human/hg19/motif_mapping/motif.list -o input.bed.assigned_targets.bed


For mm9, please use: ``--epi_file_list /path/to/motif.list``

.. code:: bash

	assign_targets_multi.py -q input.bed -tss /home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed --epi_file_list /home/yli11/Data/Human/hg19/motif_mapping/motif.list -o input.bed.assigned_targets.bed




Output
^^^^^

``-o input.bed.assigned_targets.bed``


Comments
^^^^^^^^

.. disqus::
	:disqus_identifier: NGS_pipelines



