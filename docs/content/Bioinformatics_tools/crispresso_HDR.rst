Crispresso2 for HDR
==========================


Summary
^^^^^^^

Run CRISPRESSO HDR mode.

Input
^^^^^


A 6-column tsv file: R1.fastq, R2.fastq, output_name, gRNA_seq, unedited amplicon, edited amplicon

::

	12_S12_L001_R1_001.fastq.gz	12_S12_L001_R2_001.fastq.gz	test1		cttgaccaatagccttgaca		Amplicon_seq1		Amplicon_seq2
	xxx_R1_001.fastq.gz	xxx_R2_001.fastq.gz	test1		cttgaccaatagccttgaca		Amplicon_seq1		Amplicon_seq2


.. image:: ../../images/HDR_example_input.PNG
	:align: center



Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	run_lsf.py -f input.tsv -p crispresso_PE_HDR

	## specific parameter for Azusa

	run_lsf.py -f input.tsv -p crispresso_PE_HDR --HDR_parameters " --exclude_bp_from_left 1 --exclude_bp_from_right 1 --quantification_window_coordinates 20-128"


Output
^^^^^^

Once the job is finished, you will receive a notification email.

Inside the jobID folder, you can look at the crispresso2 result. The html file is inside in each sub-folder.


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



























