Plot Chromsome Ideogram
========================

::

	usage: plot_ideogram.py [-h] [-o OUTPUT] [--organism ORGANISM]
	                        [--assembly ASSEMBLY]
	                        file [file ...]

	positional arguments:
	  file                  input bed files, the first 3 columns should be chr,
	                        start, end, additional columns will be ignored.
	                        Multiple files should be separated by space, you can
	                        use *.bed to include all bed filess in the current
	                        dir.

	optional arguments:
	  -h, --help            show this help message and exit
	  -o OUTPUT, --output OUTPUT
	                        enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        plot_ideogram_yli11_2019-10-17.html)
	  --organism ORGANISM   possible choice: Human,Mouse,Arabidopsis thaliana
	                        (default: Human)
	  --assembly ASSEMBLY   GRCh38,GRCh37,GRCm38,MGSCv37,TAIR10 (default: GRCh38)

Summary
^^^^^^^

.. image:: ../../images/ideogram.PNG
	:align: center

Input
^^^^^

A bed file with the first 3 columns specifying chr, start, end. Additional columns are OK, but they are ignored.


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	plot_ideogram.py input.bed

Note that multiple bed files are accepted. They should be separated by space.


Output
^^^^^

An html will be emailed to you.

