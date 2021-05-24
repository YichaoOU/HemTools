install tensorlfow on stjude HPC
================================



Tensorflow
^^^^^^^

Currently, our GPU nodes only have cuda8.0, and for this, the latest TF version you can use is 1.3

.. code:: bash

	ssh nodegpu121

	module load conda3

	conda create -n janggu3

	conda activate janggu3

	conda install -c anaconda tensorflow-gpu=1.3



To test GPU, see: https://www.tensorflow.org/beta/guide/using_gpu

Janggu
^^^^^

Not sure about the TF version this package used. Need to test.

.. code:: bash

	conda install -c bioconda pybigwig

	python -m pip install janggu

Test your code, should be finished within 5 min, since we are using GPU:

.. code:: bash

	git clone https://github.com/BIMSBbioinfo/janggu

	cd janggu	

	python ./src/examples/classify_fasta.py single



