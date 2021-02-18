Blood data inquiry
==================

::


	usage: blood_data_inquiry.py [-h] [-j JID] -f BED_FILE [-o OUTPUT]
	                             [--bam_file_list BAM_FILE_LIST]
	                             [--bw_list BW_LIST] (--on_bw | --on_bam)

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        blood_data_inquiry_yli11_2019-10-03)
	  -f BED_FILE, --bed_file BED_FILE
	                        input bed file for featureCount (default: None)
	  -o OUTPUT, --output OUTPUT
	                        output file name (default: featureCount)
	  --bam_file_list BAM_FILE_LIST
	                        HemTools blood collection (default:
	                        /home/yli11/HemTools/config/blood_ATAC.data)
	  --bw_list BW_LIST     HemTools blood collection (default:
	                        /home/yli11/HemTools/config/blood_ATAC.bw.list)
	  --on_bw               extract values based on bw files (default: False)
	  --on_bam              extract values based on bam files (default: False)

Summary
^^^^^^^

This is a suite of tools for users to query specific regions or genes among public blood datasets.

Output read counts over given bed. ``featureCount.tsv``. Each row is one region from the input bed file. Each column is the bw/bam file name.

Input
^^^^^

Input format varies by different usage. 

Bed format 
-------------------

Additional columns are OK. The first 3 columns have to be chr, start, end.

::

	chr11	4167364	4167385
	chr11	4167366	4167387
	chr11	4167367	4167388
	chr11	4167370	4167391

Usage
^^^^^

Signal values (bw) over input bed
----------------------------

.. code:: bash

	blood_data_inquiry.py -f input.bed --on_bw

You can also input your own list of bw files by ``--bw_list`` option.

Read counts (bam) over input bed
----------------------------

.. code:: bash

	blood_data_inquiry.py -f input.bed --on_bam

You can also input your own list of bam files by ``--bam_file_list`` option.

This output format is from ``featureCounts``, the first 5 columns are: id, chr, start, end, strand


