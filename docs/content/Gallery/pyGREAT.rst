Peak Annotation using GREAT 
===========================

**Step 1**

.. highlight:: none

:: 

	hpcf_interactive -q standard -R "rusage[mem=2000]"

**Step 2**

.. code:: bash

	module purge

	module load conda3

	source activate /home/yli11/.conda/envs/share_url

**Step 3**

.. code:: bash

	pyGREAT.py -f [your narrowpeak or bed file] --email


.. note:: Click on the URL in the email. You may need to wait for 1 minute to see the result.

.. tip:: The default genome is hg19. You can change it using ``-g`` option.


.. code:: bash

	usage: pyGREAT.py [-h] [--email] -f INPUT [-g GENOME]

	optional arguments:
	  -h, --help            show this help message and exit
	  --email               send email (default: False)
	  -f INPUT, --input INPUT
	                        input bed file (default: None)
	  -g GENOME, --genome GENOME
	                        No hg38. Please choose from hg19, mm9 or mm10.
	                        (default: hg19)















