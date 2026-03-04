Start JupyterLab in HPC
=========================


.. code:: bash

	hpcf_interactive

	export PATH=$PATH:"/home/yli11/HemTools/bin"
	
	module load python/2.7.13

	run_lsf.py -p jupyterlab --memory 20000

You will receive an email with the link to the jupyter notebook within 5 minutes.



Start JupyterLab-AI in HPC
=========================


.. code:: bash

	hpcf_interactive

	export PATH=$PATH:"/home/yli11/HemTools/bin"
	
	module load python/2.7.13

	run_lsf.py -p run_jupyterai --memory 20000

You will receive an email with the link to the jupyter notebook within 5 minutes.

first go to jid folder ``tail litellm.log`` to find the port for AI server. 

Then go to jupyternaut setting, set ``openai/gpt-5`` and ``http://localhost:48219``

Model used is ``llama3.3-70b-instruct-vllm``, not gpt-5: ``gpt-oss-120b-16bit-vllm``, because of speed. But I still name it as ``openai/gpt-5``.


Open a jupyter notebook and set

::
	
	%reload_ext jupyter_ai_magic_commands

	%config AiMagics.initial_language_model = "openai/gpt-5"

	%%ai -f code
	A function that computes the lowest common multiples of two integers, and
	a function that runs 5 test cases of the lowest common multiple function

You can also use the chat box

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


OLD
^^^

Previously I have setup a code to run ``jupyter notebook`` as below:

.. code:: bash

	export PATH=$PATH:"/home/yli11/HemTools/bin"
	
	module load python/2.7.13

	run_lsf.py -p jupyter --memory 20000

	You will receive an email with the link to the jupyter notebook.

