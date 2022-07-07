install tensorlfow on stjude HPC
================================





Keras2+Tensorflow2
^^^^^^^^^^^^^^^^^^^

.. code:: bash

	module load conda3/202011
	conda create -n keras python=3.9
	module load cuda11/toolkit/11.3
	module load cudnn/8.2.0.53
	nvidia-smi # check GPU usage
	echo $CONDA_PREFIX # check conda dir
	
	mkdir -p $CONDA_PREFIX/etc/conda/activate.d
	echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/

	pip install tensorflow
	python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
	python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
	conda install -c conda-forge jupyterlab
	conda install -c conda-forge swifter
	conda install -c anaconda seaborn
	# run jupyter lab

	export XDG_RUNTIME_DIR=""
	mkdir /scratch_space/yli11/68985
	export JUPYTER_RUNTIME_DIR=/scratch_space/yli11/68985
	jupyter lab --ip='*' --NotebookApp.token='' --NotebookApp.password='' --no-browser --port 44444



	# install janggu
	# pysam install has an error in my system, so I used conda to install it
	pip install --no-deps janggu[tf2_gpu] 
	# install those dependences manually

	vim ~/.conda/envs/keras/lib/python3.9/site-packages/janggu/layers.py
	# change from keras.layers.wrappers import Wrapper to 
	# from tensorflow.keras.layers import Wrapper


Submit GPU job

::


	#BSUB -P run_jupyte
	#BSUB -o keras_%J_%I.out -e keras_%J_%I.err
	#BSUB -n 1
	#BSUB -q gpu
	#BSUB -R "span[hosts=1] rusage[mem=60000]"
	#BSUB -J "keras"

	module purge

	ncore=1
	mem=60000
	q=gpu
	echo $PATH
	PATH=/home/yli11/HemTools/bin:/hpcf/lsf/lsf_prod/10.1/linux3.10-glibc2.17-x86_64/etc:/hpcf/lsf/lsf_prod/10.1/linux3.10-glibc2.17-x86_64/bin:/usr/lpp/mmfs/bin:/usr/lpp/mmfs/lib:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/ibutils/bin:/sbin:/cm/local/apps/environment-modules/3.2.10/bin:/opt/puppetlabs/bin:/home/yli11/Programs/HiC-Pro-2.11.1/bin/utils:/research/dept/hem/common/sequencing/chenggrp/pipelines/bin
	echo $PATH
	module load conda3/202011
	source activate /home/yli11/.conda/envs/keras
	module load cuda11/toolkit/11.3
	module load cudnn/8.2.0.53
	module load texlive/20190410
	echo $PATH
	echo `which python`
	export XDG_RUNTIME_DIR=""
	mkdir /scratch_space/yli11/$$
	export JUPYTER_RUNTIME_DIR=/scratch_space/yli11/$$
	cp /home/yli11/HemTools/share/misc/Introduction_6_21_2021_v2.ipynb run_jupyterlab_gpu_yli11_2022-07-07/
	cp /home/yli11/HemTools/share/tutorial/* run_jupyterlab_gpu_yli11_2022-07-07/
	yes | cp -rf /research/rgs01/home/clusterHome/yli11/.local/share/jupyter/kernels/ ~/.local/share/jupyter/
	jupyterlab.py run_jupyterlab_gpu_yli11_2022-07-07/Introduction_6_21_2021_v2.ipynb


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



