Merge fastq files for L001 L002 L003 L004 
===================================

::

	usage: merge_lanes_fastq.py [-h] [--run] file [file ...]

	merge input dataframes using row index. Assume input tables contain both row
	names and column names.

	positional arguments:
	  file

	optional arguments:
	  -h, --help  show this help message and exit
	  --run       perform the actual merge fastq (default: False)

Summary
^^^^^^^

Merge fastq files from different lanes.

Input
^^^^^

Input the locations for the fastq files.

Example
------

I have fastq files inside many folders. See below

::
	
	ls *

	2-1199356:
	1921110_BANANA_L001_R1_001.fastq.gz  1921110_BANANA_L001_R2_001.fastq.gz  1921110_BANANA_L002_R1_001.fastq.gz  1921110_BANANA_L002_R2_001.fastq.gz

	2-1199357:
	1921111_APPLE_L001_R1_001.fastq.gz  1921111_APPLE_L001_R2_001.fastq.gz  1921111_APPLE_L002_R1_001.fastq.gz  1921111_APPLE_L002_R2_001.fastq.gz

	2-1199358:
	1921112_ORANGE_L001_R1_001.fastq.gz  1921112_ORANGE_L001_R2_001.fastq.gz  1921112_ORANGE_L002_R1_001.fastq.gz  1921112_ORANGE_L002_R2_001.fastq.gz

	2-1199359:
	1921113_KIWI_L001_R1_001.fastq.gz  1921113_KIWI_L001_R2_001.fastq.gz  1921113_KIWI_L002_R1_001.fastq.gz  1921113_KIWI_L002_R2_001.fastq.gz

Then the input is ``*/*.gz``

Usage
^^^^^


.. code:: bash

	hpcf_interactive.sh

	module load python/2.7.13

	merge_lanes_fastq.py */*.gz

	merge_lanes_fastq.py */*.gz --run

``--run`` option will ask the program to do the merging. Without it, the program will just output the merging command (for you if see if they look correct, because the merge groups are infered by the program, there could be an error.)

In case the fastq files locations are hard to specify, use the following command, it will search all .gz file in the current dir:

.. code:: bash

	merge_lanes_fastq.py `find . -name "*.gz"`

Output
^^^^^^

Merged fastq files in the current dir.

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines






