Upload your bw and bed files to protein paint
=============================================

Summary
^^^^^^^

An easy way to visualizing your data. This program will upload all ``.bw``, ``.bed``, and ``Peak`` files to protein paint. Note that protein paint genome browser is only accessible inside stjude network. 


.. image:: ../../gallery/ppr.png
	:align: center


Usage
^^^^^

**Step 1**

.. code:: bash

	module purge

	module load python/2.7.13 htslib

**Step 2**

.. code:: bash

	create_tracks.py -h

	usage: create_tracks.py [-h] [-j JID] [-g GENOME] [--current_dir]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     a folder name, used to upload tracks (default:
	                        create_tracks_yli11_2019-06-28)
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. (default: hg19)
	  --current_dir         Upload .bed .narrowPeak .broadPeak and .bw files
	                        (default: False)

.. code:: bash

	create_tracks.py --current_dir -g hg19

When finished, it will print out an url, similar like below:

.. code:: bash

	2019-06-28 14:41:43,232 - INFO - upload_bed_bw - connecting to server
	2019-06-28 14:41:43,625 - INFO - upload_bed_bw - creating user's dir
	2019-06-28 14:41:53,804 - INFO - upload_bed_bw - generating json file
	2019-06-28 14:41:56,213 - INFO - upload_bed_bw - transfering file
	Please copy the following url to your genome browser. Note that protein paint genome browser is only accessible inside stjude network.
	https://ppr.stjude.org/?study=HemPipelines/yli11/create_tracks_yli11_2019-06-283a1f4cad5f47/tracks.json








