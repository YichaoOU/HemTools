Cas Offinder
============

.. code:: bash

	module load conda3

	conda create -m Cas_Offinder

	# When asked ``Proceed ([y]/n)?``, type ``y``

	source activate Cas_Offinder

	conda install -c bioconda cas-offinder 

	# When asked ``Proceed ([y]/n)?``, type ``y``

For a test run

.. code:: bash
	
	cd /research/dept/hem/common/sequencing/temp

	cas-offinder test.cas_input C test.out


