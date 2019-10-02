Blood data inquiry
==================

::


Summary
^^^^^^^

This is a suite of tools for users to query specific regions or genes among public blood datasets.


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











