Plot bw file correlation
========================

::

	usage: plot_bw_corr.py [-h] [-j JID] [-f BW_FILES] [-b BIN_SIZE] [-r REGION]
	                       [-o OUTPUT] [--addon_parameter ADDON_PARAMETER]

	plot correlation for all bw files in the current dir

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        plot_bw_corr_yli11_2019-09-18)
	  -f BW_FILES, --bw_files BW_FILES
	                        input file or use all bw files in the current dir
	                        (default: None)
	  -b BIN_SIZE, --bin_size BIN_SIZE
	  -r REGION, --region REGION
	                        Could be chr11:5267561-5277281, HBG region (default:
	                        None)
	  -o OUTPUT, --output OUTPUT
	  --addon_parameter ADDON_PARAMETER

Summary
^^^^^^^

Plot spearman correlation given all bw files in the current dir. By default, bin size is 10kb.

Input
^^^^^

No specific input files are needed because all bw files in the current dir will be automatically used.

You can definitely control the input files using ``-f`` option. Files have to be quoted and separated by space, i.e., ``"file1.bw file2.bw file3.bw"``

Output
^^^^^^

.. image:: ../../images/bw_corr.png
	:align: center


Usage
^^^^^

Go to your data directory and type the following.

**Step 0: Load python version 2.7.13.**

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

**Step 1: Run the program**

.. code:: bash

	plot_bw_corr.py 

	2019-10-18 14:40:49,646 - INFO - main - The job id is: plot_bw_corr_yli11_2019-10-18
	2019-10-18 14:40:49,763 - INFO - submit_pipeline_jobs - cor has been submitted; JobID: 88117190


.. note:: You can also control the bin size and a specific region to use when calculating correlations. See the example below.

.. code:: bash

	plot_bw_corr.py -b 150 -r chr11:5267561-5277281


Re-order labels
^^^^^^^^^^^^

Once the program is finish and you are not satistified with the order of columns and rows, you can re-order the figure using the following commands.

Input is the ``plotCorrelation.tab`` in your result folder.


Details are also provided in: :doc:`plot_corr_reorder <plot_corr_reorder>`


Example --- compare your ATAC-seq to public blood lineage ATAC-seq
^^^^^

Save the bw file list in :doc:`blood_data <../Data/blood_data>` as input.list.

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	for i in `cat input.list`;do ln -s $i;done

	## ln -s your own bw files here

	plot_bw_corr.py




