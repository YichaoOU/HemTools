Blood data enrichment test
==================

Summary
^^^^^^^

This is a suite of tools for users to do an enrichment test given a list of bed files.

Input
^^^^^

A list of bed files. The first 3 columns of bed file should be chr, start, end.

Bed format 
-------------------

Additional columns are OK. The first 3 columns have to be chr, start, end.

::

	chr11	4167364	4167385	chr11:4167374-4167375
	chr11	4167366	4167387	chr11:4167376-4167377
	chr11	4167367	4167388	chr11:4167377-4167378
	chr11	4167370	4167391	chr11:4167380-4167381

Output
^^^^^^^

Blood traits variants/SNPs enrichment heatmap
----------------------------

.. image:: ../../images/enrichment_heatmap.png
	:align: center



Usage
^^^^^

Blood traits variants/SNPs enrichment
----------------------------

::

	usage: GREGOR.py [-h] [-j JID] [-s SNP_LIST] -f BED_LIST
	                 [--template_config TEMPLATE_CONFIG]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        GREGOR_yli11_2019-10-25)
	  -s SNP_LIST, --SNP_list SNP_LIST
	                        Please provide absolute path (default: /home/yli11/Hem
	                        Tools/config/blood_variants_VJ2019.list)
	  -f BED_LIST, --bed_list BED_LIST
	                        absolute or relative path (default: None)


.. code:: bash

	GREGOR.py -f bed.list

