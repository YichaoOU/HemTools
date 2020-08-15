Count indel integration pipeline
=====================

Input
^^^^^

Input file is a 4-col tsv file: R1 read, R2 read, output_name, user_input_bed_file

::

	CRL1403_S1_R1_001.fastq.gz	CRL1403_S1_R2_001.fastq.gz	CRL1403_S1	CTLA4_site_9.bed


Output
^^^^^^


Usage
^^^^^

Step 1: --guess_input


Step 2: manually add the bed file as the 4th column


Step 3: submit job


run_lsf.py -p count_integration -f fastq.tsv