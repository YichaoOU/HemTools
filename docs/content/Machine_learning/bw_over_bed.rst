Calculate average signal given bed file
======================================


::


	usage: bw_over_bed.py [-h] [--bw_files BW_FILES] [--bed_files BED_FILES]
	                      [--extend EXTEND] [-o OUTPUT]

	optional arguments:
	  -h, --help            show this help message and exit
	  --bw_files BW_FILES   input a list of bw files, use * to indicate all bw
	                        files in the current dir (default: *)
	  --bed_files BED_FILES
	                        input a list of bed/Peak files, use * to indicate all
	                        bed/Peak files in the current dir (default: *)
	  --extend EXTEND       extend bed file (default: 0)
	  -o OUTPUT, --output OUTPUT
	                        output prefix (default:
	                        yli11_2019-12-06_1952e43c5a3b.averageBW)

Usage
^^^^^

.. code:: bash

	hpcf_interative.sh
	module load python/2.7.13 ucsc/041619
	bw_over_bed.py

By default, this program will output a count table for each bed file in the current dir.

















