DESEQ2 for differential peak analysis
=====================================

::

	usage: diffPeak.py [-h] [-b BAMS] [-d DESIGN_MATRIX] [-p PEAKS] [-x DRY_RUN]
	                [-z SUBMIT_JOB] [-r FLAG] [--include_unmapped_reads] [-s]
	                [-j JID]

	optional arguments:
	  -h, --help            show this help message and exit
	  -b BAMS, --bams BAMS  list of bam files (include path to file)
	  -d DESIGN_MATRIX, --design_matrix DESIGN_MATRIX
	                        Each line is a group. Every group will be compared
	                        against the 'control' group. So you have to specify a
	                        control group in your input. The format for each line
	                        is: group_id:file_name_1,file_name_2. Just need file
	                        name, no need for the path to file.
	  -p PEAKS, --peaks PEAKS
	                        list of narrowPeak files (include path to file), need
	                        the last line to be empty (i.e. so as to have the
	                        newline character).
	  -x DRY_RUN, --dry_run DRY_RUN
	                        1 or 0. 1: dry run, to check system commands
	  -z SUBMIT_JOB, --submit_job SUBMIT_JOB
	                        1 or 0. 1: submit this job to HPC
	  -r FLAG, --flag FLAG  1 or 0. 1: run this job in terminal. 0: submit this
	                        job.
	  --include_unmapped_reads
	                        Expecting global change, need normalization by total
	                        reads
	  -s, --single          run featureCount in single-end mode
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder.

Summary
^^^^^^^

This program performs differential peak analysis by taking the union of input peaks (i.e., bedtools merge), counting number of reads (for pair-end, it is number of fragments), then running DESEQ2. At the last step, peaks will be divided into gain or loss, each of which will be used to perform motif discovery using homer. 

.. note:: By default, DESEQ2 normalization is performed on total reads in peaks. You can also do it on raw total reads (i.e., sequencing depth), by using ``--include_unmapped_reads``.




Flowchart
^^^^^^^^^

.. image:: ../../images/deseq_diffpeak.png


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.12

	dos2unix bams.list
	dos2unix design_matrix
	dos2unix peaks.list

	diffPeak.py -b bams.list -d design_matrix -p peaks.list -z 1 

``-z 1 `` tells the program to submit this job to HPC. Otherwise, diffPeak will just run interactively.

If you want to include all reads for DESEQ normalization, please add ``--include_unmapped_reads`` option.

If you are using single-end bam, please add ``-s`` option.


Input
^^^^^

Sample input examples are shown here: https://benchling.com/s/etr-FHkOZSXjFTUTDROQ2xu2











