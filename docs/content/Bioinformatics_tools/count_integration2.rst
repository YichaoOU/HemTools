Count indel integration pipeline  (simplified version)
=====================


Summary
^^^^^^^

This pipeline simplifies the usage of count indel integration pipeline: :doc:`here <count_integration>` but it can only processes one gRNA per run. 

Input
^^^^^


1. gRNA bed file
----------------

gRNA_bed_file is a tab separated file, it should have 6 columns: chr, start, end, name, value (can be anything), strand

The coordinates for gRNA need to include the PAM sequence.

g34 has two occurrences in the genome, so its bed file look like below

::

	chr11	5249956	5249975	HBG1	1	+
	chr11	5254880	5254899	HBG2	2	+


Output
^^^^^^

When the job is finished, you will be notified by an email with QC report and a ``summary.csv`` for indel frequecies and different indel types.


Usage
^^^^^

Create a new working dir, put the fastq files in it (e.g., ``ln -s``) and run the following.

Step 0: Login to a compute node.

::

	hpcf_interactive

Step 1: generate input file ``fastq.tsv`` using ``--guess_input``

::

	module load python/2.7.13

	export PATH=$PATH:"/home/yli11/HemTools/bin"

	# cd to your working dir

	run_lsf.py --guess_input

Step 2: submit job

::

	run_lsf.py -p count_integration2 -f fastq.tsv --gRNA_bed gRNA.bed

