Merge multiple bedfiles
===================================

::

	usage: merge_bed.py [-h] [-o OUTPUT] [-e EXTEND] [--cut3] [--keep_info]
	                    file [file ...]

	merge bedfiles into one

	positional arguments:
	  file

	optional arguments:
	  -h, --help            show this help message and exit
	  -o OUTPUT, --output OUTPUT
	                        output table name (default:
	                        yli11_2023-09-12_ef80e2e7efe1.bed)
	  -e EXTEND, --extend EXTEND
	                        get peak center and extend by (default: 0)
	  --cut3                only use first 3 columns (default: False)
	  --keep_info           merge a bed6 file and randomly keep 4,5,6 columns if
	                        there is overlap (default: False)


Summary
^^^^^^^

Merge multiple bed files into one bed file, pattern matching for file name is allowed.

9/12/2023 updates
^^^^^^^

Added ``--extend`` parameter so user can control output region size. If the value > 0, then the program will calculate the peak center and extend by the given length up and downstream.

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






