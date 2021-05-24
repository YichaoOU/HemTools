R1/R2 reads strand bias
===============



Motivation
^^^^^^^^^^

When we develop a new method, we found a strand bias in R1 and R2 at cut site. Suppose to be total random. 

Summary
^^^^^^^

This analysis aims to show barplot for R1+, R1-, R2+, and R2- counts.

Usage
^^^^^

.. code:: bash

	run_lsf.py -f input.tsv -p R1_R2_strand_bias


Input
^^^^^

two column tsv, abs or relative path to the file.

First column is bam file

Second column is target bed file (the region where R1 and R2 starts)

Output
^^^^^^

Barplot
