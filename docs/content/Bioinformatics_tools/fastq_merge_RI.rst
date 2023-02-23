Merge fastq I1 I2 R1 R2 reads into R1 and R2
======================


::

	usage: fastq_merge_RI.py [-h] -o1 O1 -o2 O2 -r1 R1 -r2 R2 -i1 I1 -i2 I2

	optional arguments:
	  -h, --help  show this help message and exit
	  -o1 O1      output R1 fastq file name (default: None)
	  -o2 O2      output R2 fastq file name (default: None)
	  -r1 R1      read1 fastq (default: None)
	  -r2 R2      read2 fastq (default: None)
	  -i1 I1      index1 fastq (default: None)
	  -i2 I2      index2 fastq (default: None)



Summary
^^^^^^^

Add I1 and I2 into R1 and R2. So the output fastq is like:

::

	@VH00889:7:AACKJGLM5:1:1101:18269:1000 1:N:0:ACAGTGAT+AGATCTCG
	AGGAATAGCATTAAATCTGCAGATAGCTTTGGGCAGTATGATCATTTTCA
	+
	CCCCCCCCCCCC;CCCCCCCCCCCCCCC--CCCCCC;CCCCCCCCCCCCC

Input
^^^^^

You need to specify I1, I2, R1 and R2 fastq file.

Output
^^^^^^

You need to specify the output R1 and R2 fastq file name.


Usage
^^^^^

.. code:: bash

	hpcf_interactive.sh

	module load python/2.7.13

	fastq_merge_RI.py -r1 2544979_GM_RNA1_S6_L001_R1_001.fastq.gz -r2 2544979_GM_RNA1_S6_L001_R3_001.fastq.gz -i1 2544979_GM_RNA1_S6_L001_I1_001.fastq.gz -i2 2544979_GM_RNA1_S6_L001_R2_001.fastq.gz -o1 GM_RNA1_S6_R1.fastq.gz -o2 GM_RNA1_S6_R2.fastq.gz







