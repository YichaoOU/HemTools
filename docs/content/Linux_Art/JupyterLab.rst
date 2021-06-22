Start JupyterLab in HPC
=========================


Previously I have setup a code to run ``jupyter notebook`` as below:

.. code:: bash

	export PATH=$PATH:"/home/yli11/HemTools/bin"
	
	module load python/2.7.13

	run_lsf.py -p jupyter --memory 20000

	You will receive an email with the link to the jupyter notebook.


Here, jupyter lab is the next generation of jupyter notebook. Here is the usage:


.. code:: bash

	export PATH=$PATH:"/home/yli11/HemTools/bin"
	
	module load python/2.7.13

	run_lsf.py -p jupyterlab --memory 20000

	You will receive an email with the link to the jupyter notebook.

Set up env (my notes for installation)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	module load conda3/202011
	conda create -n captureC -c bioconda bioconductor-chicago
	source activate captureC
	conda install -c anaconda jupyter_client
	conda install -c conda-forge jupyterlab
	conda install -c r r-pbdzmq
	conda install -c conda-forge nodejs
	conda install -c cheng_lab easy_prime # to install some python libraries
	jupyter labextension install @techrah/text-shortcuts
	export XDG_RUNTIME_DIR=""
	export JUPYTER_RUNTIME_DIR=/tmp
	jupyter lab --ip='*' --NotebookApp.token='' --NotebookApp.password='' --no-browser --port 9865

in R

::

	install.packages('IRkernel')
	IRkernel::installspec()

