Distribution of outward reads overlaps
================


Motivation
^^^^^^^^^^

For CHANGE-seq debug purposes

Summary
^^^^^^^

This analysis aims to generate a histogram for the number of overlap bases in outward reads.

Usage
^^^^^

.. code:: bash

	run_lsf.py -f input.tsv -p outward_overlap_dist

.. code:: bash

	run_lsf.py -f input.tsv -p outward_overlap_dist --target target.bed

with ``--target target.bed`` option, the histogram will only focus on reads mapped to the bed file.

Input
^^^^^

two column tsv, abs or relative path to the file.

First column is bam file

Second column is target bed file (the region where R1 and R2 starts)

Output
^^^^^^

histogram

Note
^^^^

bedtools bamtobed only works for inward reads

