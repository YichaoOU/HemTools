Filter out reads mapped to specific sequences
=============

Input
^^^^^

1. fastq.tsv
------

3 columns: R1, R2, sample_name

You can prepare your fastq.tsv using ``run_lsf.py --guess_input``

2. your fasta file
----------------

standard fasta file

::

	>chrM
	AAAAAAAAAAAAAAAAA


Usage
^^^^^

::

	# login to a compute node
	hpcf_interactive.sh

	run_lsf.py -f fastq.tsv -p filter_reads --my_fasta test.fa

Output
^^^^^^

Newly generated fastq files without those unwanted reads are stored in the ``jid`` folder (e.g., filter_reads_yli11_2022-05-13).





