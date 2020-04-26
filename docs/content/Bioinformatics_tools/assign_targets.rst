Identify direct targets and co-binding factors
=============


::



Summary
^^^^^

Assigning target genes using promoter capture HiC data. For pc-HiC data, see :doc:`hg19 pc-HiC <../Data/captureC_pcHiC>`. For target gene assignment workflow, see :doc:`tf_target_finder pipeline <tf_target_finder>`.

Assigned targets will be appended as new columns to the input bed file.

Ref: https://github.com/YichaoOU/TF_target_finder


Input
^^^^^

1. query bed file

A bed file with any number of columns. But the first 3 columns should be chr, start, end.

2. TSS annotation bed file

hg19: /home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed 

3. a list of promoter capture HiC bed file.

see :doc:`hg19 pc-HiC <../Data/captureC_pcHiC>`

``--epi_file_list pcHIC.list ``


Usage
^^^^^

.. code:: bash

	hpcf_interative

	module load conda3

	source activate /home/yli11/.conda/envs/py2

	assign_targets_multi.py -q input.bed -tss /home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed --epi_file_list pcHIC.list -o input.bed.assigned_targets.bed



Output
^^^^^

``-o input.bed.assigned_targets.bed``


Comments
^^^^^^^^

.. disqus::
	:disqus_identifier: NGS_pipelines


