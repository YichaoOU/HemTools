Subsample fastq to the same sequencing depth
========================================



Input
^^^^^^

1. Fastq read list. You can get it using ``ls *fastq.gz > input.list``

2. Desired sequencing depth. You first need to count the reads and find the minimal reads in your fastq list.

Usage
^^^^^

::

	hpcf_interactive -q priority

	module load python/2.7.13

	ls *fastq.gz > input.list

	run_lsf.py -f se.list -p subsample_fastq --seqtk_sample_number 30000000











