long-read RNA-seq quantification
===============================


Summary
^^^^^^^

long-read RNA-seq quantification using isoQuant


Input
^^^^^


Fastq files. Need to have ``fastq`` in the filename. e.g., .fastq or .fastq.gz


Usage
^^^^^

Copy the ``*fastq*`` files into the working dir.

.. code:: bash

	hpcf_interactive.sh

	module load python/2.7.13

	# cd to your working dir

	run_lsf.py -p isoQuant

Output
^^^^^

In the jobID folder, see ``OUT.transcript_grouped_tpm.tsv`` or ``OUT.gene_grouped_tpm.tsv``

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines












