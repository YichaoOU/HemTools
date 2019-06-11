Peak Annotation using GREAT 
===========================

**Step 1**

.. highlight:: none

:: 

	hpcf_interactive -q standard -R "rusage[mem=2000]"

**Step 2**

.. code:: bash

	module load conda3

	source activate /home/yli11/.conda/envs/share_url

**Step 3**

.. code:: bash

	pyGREAT.py [your narrowpeak or bed file] --email


.. note:: Click on the URL in the email. You may need to wait for 1 minute to see the result.



















