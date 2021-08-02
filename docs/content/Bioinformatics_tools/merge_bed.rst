Merge multiple bedfiles
===================================

::

	usage: merge_bed.py [-h] [-o OUTPUT] file [file ...]

	merge bedfiles into one

	positional arguments:
	  file

	optional arguments:
	  -h, --help            show this help message and exit
	  -o OUTPUT, --output OUTPUT
	                        output table name (default:
	                        yli11_2021-08-02_7eb6f211a2d1.bed)


Summary
^^^^^^^

Merge multiple bed files into one bed file, pattern matching for file name is allowed.


Usage
^^^^^

Copy the bed files into working dir.

.. code:: bash

	hpcf_interactive.sh

	module load python/2.7.13

	merge_bed.py -o union.bed *.bed


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines






