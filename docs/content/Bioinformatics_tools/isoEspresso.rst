long-read RNA-seq quantification using espresso
===============================


Summary
^^^^^^^

long-read RNA-seq quantification using espresso 1.6.0, this is a required step to run rMATs-long.

https://github.com/Xinglab/espresso

Input
^^^^^


Aligned bam files. Save as ``samples.tsv`` in your working dir. ALso need .bai in current dir. Abs path.

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

run rMATs-Long
^^^^^^^^^^^^^

``cd $jid/work_dir``

Prepare ``compare.tsv``, a 3-col tsv file, showing samples for group 1 (col1) and samples for group 2 (col), and a comparison name. 

The sample names must be the exact sample name you used for expresso analysis.

::

	CD34_P0_rep1,CD34_P0_rep2	CD34_P1_rep1,CD34_P1_rep2	P1_vs_P0
	CD34_P0_rep1,CD34_P0_rep2	CD34_P2_rep1,CD34_P2_rep2	P2_vs_P0



.. code:: bash

	hpcf_interactive.sh

	module load python/2.7.13

	# cd to your working dir

	run_lsf.py -f compare.tsv -p rmat_long





Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines












