long-read RNA-seq quantification using isoQuant
===============================


Summary
^^^^^^^

long-read RNA-seq quantification using isoQuant 3.5.0

https://github.com/ablab/IsoQuant

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

	# use gencode v47 canonical gtf, one transcript per gene, for novel transcript identification, see tequial_seq_all folder
	run_lsf.py -p isoQuant

	# only this run below is for nanopore, others are for Pacbio data. use gencode v47 canonical gtf
	run_lsf.py -p isoQuant_nanopore

	# copy all the bam files (minimap aligned) to a working dir and start from bam, this pipeline uses ISO_Tequila_JJ_all.gtf based on v47
	run_lsf.py -p isoQuant_bam


Output
^^^^^

In the jobID folder, see ``OUT.transcript_grouped_tpm.tsv`` or ``OUT.gene_grouped_tpm.tsv``

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines












