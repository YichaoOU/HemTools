Count indel integration pipeline
=====================


Summary
^^^^^^^

This pipeline performs the following analysis in order:

1. trimmomatic PE 

2. flash

3. bwa mem

4. count_indels_integrations.py


Input
^^^^^

Input file is a 4-col tsv file: R1 read, R2 read, output_name, user_input_bed_file

::

	CRL1403_S1_R1_001.fastq.gz	CRL1403_S1_R2_001.fastq.gz	CRL1403_S1	CTLA4_site_9.bed


The first 3 columns can be automatically generated using ``--guess_input`` option. Users have to fill in the last column.


Output
^^^^^^

Inside the Job ID folder, you can find individual result folder for each line specified in the input.


Usage
^^^^^

Create a new working dir, put the fastq files in (e.g., ``ln -s``) and run the following.

Step 1: generate input file ``fastq.tsv`` using ``--guess_input``

::

	hpcf_interactive

	module load python/2.7.13

	export PATH=$PATH:"/home/yli11/HemTools/bin"

	run_lsf.py --guess_input


Step 2: manually add the bed file as the 4th column


Step 3: submit job

::

	run_lsf.py -p count_integration -f fastq.tsv