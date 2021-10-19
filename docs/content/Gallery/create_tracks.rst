Upload your bw and bed files to protein paint
=============================================

REF
^^^

https://docs.google.com/document/d/1e0JVdcf1yQDZst3j77Xeoj_hDN72B6XZ1bo_cAd2rss/edit#

Follow this to use the new track collection version.

Example: https://ppr.stjude.org/?genome=hg19&block=1&tkjsonfile=yli11/rick/test3.json

Summary
^^^^^^^

An easy way to visualizing your data. This program will upload all ``.bw``, ``.bed``, and ``Peak`` (newly added, ``.bedpe`` and ``.mango``) files to protein paint. Note that protein paint genome browser is only accessible inside stjude network. 


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
	                        genome version: hg19, hg38, mm9, mm10, hgvirus. (default: hg19)
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



Add gene track to custom genome
^^^^^^^^^^^^^^^^^^^


1. download gene annotation gtf file

2. using lift over bed, to lift over gtf file

3. using Xin's tool to convert gtf to bedj

nodejs version >= 2.10

default node mem is 1.5G, increase it to 8G

.. code:: bash

	module load conda3

	source activate /home/yli11/.conda/envs/npm

	export NODE_OPTIONS=--max-old-space-size=8192

	node gtf2bedj.js hg19_20copy.gtf > out.bedjs

	sort -k1,1 -k2,2n out.bedjs > hg19_20copy.st.bedj

	module load htslib
	bgzip hg19_20copy.st.bedj 
	tabix -p bed hg19_20copy.st.bedj.gz


Put this json:

::

	{
	"type":"bedj",
	"name":"Ensembl v87 genes",
	"file":"yli11/hgcOPT/20copy_data/hg19_20copy.st.bedj.gz",
	"stackheight":14,
	"stackspace":1
	}



automatically generate json file given all files in current_dir
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	cd /home/yli11/dirs/genome_browser/yli11/Jingjing
	ppr_json.py -d yli11/Jingjing -o tracks.json -g mm10















