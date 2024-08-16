long-read RNA-seq quantification using espresso
===============================


Summary
^^^^^^^

long-read RNA-seq quantification using espresso 1.4

https://github.com/Xinglab/espresso

Input
^^^^^


Aligned bam files. Save as ``samples.tsv`` in your working dir. ALso need .bai in current dir.

::


	/path/to/first.sorted.bam	first_sample_name
	/path/to/second.sorted.bam	second_sample_name


Usage
^^^^^

.. code:: bash

	hpcf_interactive.sh

	module load python/2.7.13

	# cd to your working dir

	run_lsf.py -p pacbio_expresso

Output
^^^^^

In the jobID folder, see esp file

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines












