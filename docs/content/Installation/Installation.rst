Installation
============

Most APIs are free of installation. Just type the following:

.. code:: bash

	$ /research/dept/hem/common/sequencing/chenggrp/pipelines/bin/add_env.sh



Installation for running MethyMotifs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	$ module load conda3
	$ conda create -n julia
	$ source activate julia
	$ conda install -c conda-forge julia=0.6.1
	$ conda install -c bioconda weblogo
	$ source deactivate

Other tools installation

.. toctree::
   :maxdepth: 1
   :glob:

   *