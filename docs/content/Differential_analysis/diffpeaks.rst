Differential Peaks
==================




Summary
^^^^^^^

Still under development.







Input
^^^^^

**1. bam file list**

A tsv file containing two columns. The first column is the file name. If the file is not in the current directory, please include absolute path. The second column is the group name, which will be used in the design matrix.

.. code:: bash

	file1.bam	group1
	file2.bam	group1
	file3.bam	group2

**2. design matrix**

A tsv file containing three columns. The first two columns are group comparisons. For example, if you want to compare group1 with group2, then put group1 to the first column, because gain/loss or up/down will be respect to the second column. The third column is output file name (prefix).


.. code:: bash

	group1	group2	grandPa_favorites
	group3	group2	grandMa_favorites


**(Optional) 3. genomic region .bed**

A bed file (could be any number of columns, but the first three columns should always be chr, start, end) containing regions of interest. If provided, differential peaks will only be called on these regions.


Tools
^^^^^

Parameter: with/w.o. replicates

::
	Baseline – unique peaks
	macs2 bdgdiff
	DESEQ2, edgeR-robust
	MAnorm
	ODIN (is replaced by THOR)
	Homer
	Epic2
	THOR
	MultiGPS
	RSEG

The following tools are only applicable with replicates:
::
	diffBind
	Csaw
	ChIPComp

Not tested
::
	GenoGAM
	diffReps



Output
^^^^^^

An ensemble of different tools. 

A venn diagram showing similarities.

User can peak the results that make the most sense.










