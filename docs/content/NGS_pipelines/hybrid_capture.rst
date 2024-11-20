Hybrid-Capture data analysis pipeline
===================================


Summary
^^^^^^^

For CRISPR editing experiments. Oligos were designed for each target region, approximately 5 oligos per region, from Twist Bio.

Pipeline Steps
^^^^^^^^^^^^

1. adapter trimming ``-a AGATCGGAAGAGC -A AGATCGGAAGAGC``

2. Rename fastq for later UMI analysis

3. FLASH merge R1 and R2. Unmerged reads are treated as individual molecule. 

4. UMI-deduplication for merged and unmerged reads using https://github.com/aryeelab/umi, this steps removes about 2% reads.

5. bwa mapping to intended genome

Input
^^^^^

fastq.tsv
---------

Use ``--guess_input`` to automatically generate this.

::

	Banana_R1.fastq.gz	Banana_R2.fastq.gz	Banana_lovers
	Orange_R1.fastq.gz	Orange_R2.fastq.gz	Orange_lovers


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	run_lsf.py -f fastq.tsv -p hybrid_capture -g hg38