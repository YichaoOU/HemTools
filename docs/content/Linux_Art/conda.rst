conda cheatsheet
================

You may want to create a Conda environment to share with all your group members. In this case you will need to create the environment in a new location. You can do this with the --prefix command. For example:

conda create --prefix $SCRATCH/../conda/envs/<environment_name>
This will create the environment in the root of your group's scratch directory. To activate this environment requires a little more typing since it's not in the standard location for Conda environments

source activate /panfs/pfs.local/scratch/<your_group>/conda/envs/<environment_name>

.. code:: bash

	jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password=''

Start a jupyter notebook on HPC
^^^

.. code:: bash

	export PATH=$PATH:"/home/yli11/HemTools/bin"
	
	module load python/2.7.13

	run_lsf.py -p jupyter --memory 20000

You will receive an email with the link to the jupyter notebook. Use ``--memory`` to control the requested memory.

5/4/2021, notebook only support python3.


Commonly used python libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	import pandas as pd
	import numpy as np
	import scipy.stats as sts
	import gzip as gz
	import pysam
	import pandas as pd
	import seaborn as sns
	import matplotlib.pyplot as plt
	import numpy as np
	import scipy
	import glob
	from joblib import Parallel, delayed
	import sys
	import argparse
	import plotly.express as px
	import plotly.io as pio
	import os
	from Bio.Seq import Seq
	from Bio import SeqIO
	import swifter
	import sys
	import plotly.express as px
	from Levenshtein import distance
	pd.options.display.max_columns = 100
	pd.options.display.max_rows = 100
	import matplotlib
	matplotlib.rcParams['pdf.fonttype'] = 42
	matplotlib.rcParams['ps.fonttype'] = 42
	import warnings
	warnings.filterwarnings("ignore")


Ignore python warning

export PYTHONWARNINGS="ignore"


Save fig
^^^^^^

::

	plt.figure(figsize=(10,10))
	df2['nfix'] = df2.Nfix_raw
	sns.scatterplot(data = df2,x="tSNE_1",y="tSNE_2",
	                hue="ident",palette=color_dict,
	                size="nfix",linewidth=0,sizes=(5, 200))
	plt.legend(ncol=4,loc='upper center',bbox_to_anchor=(0.5,1.2 ))
	plt.savefig("Nfix_scRNA_seq.pdf",bbox_inches='tight')

	df2['nfix'] = df2.Nfix_raw
	f, ax = plt.subplots(figsize=(10,10))
	df2 = df2.sort_values("nfix",ascending=True)
	points = ax.scatter(df2.tSNE_1, df2.tSNE_2,c=df2.nfix, s=20, cmap="magma_r",alpha=0.8,linewidth=0)
	f.colorbar(points)
	plt.savefig("Nfix_scRNA_seq_exp.pdf",bbox_inches='tight')

Create package
^^^^^^^^^^^

I recently created a pip package and it can be easily converted to a conda package.

The package name is ``unique_color``. However, when upload it to pypi, its name becomes ``unique-color``. And when conda-build trying to download the package, from this url: https://files.pythonhosted.org/packages/source/u/unique_color/unique-color-3.0.tar.gz. This url is not exist, which should be ``https://files.pythonhosted.org/packages/source/u/unique-color/unique_color-3.0.tar.gz``. Apparently, the package name could be ``-`` or ``_``, but the file name can only be the one you specified in setup.py.

So the steps are:

1. pypi

If you want to update package description, you have to create a new release.

::

	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

2. conda

I found "activate a conda env and then conda build" leads to a conda package missing dependencies.

::

	conda skeleton pypi unique-color
	cd unique-color
	conda-build .
	anaconda upload /home/yli11/conda-bld/linux-64/unique_color-3.0-py36_0.tar.bz2

conda-build is slow, for changeseq, it took 20min to finish.

``conda skeleton pypi unique-color`` will create meta.yaml in ``unique-color`` folder. To enforce a specific python version, you can create a file called ``conda_build_config.yaml``, and put:

::

	python:
	  - 2.7

To add any dependencies, edit ``meta.yaml`` file, add specific libraries (which can be installed through conda or pip).

::

	requirements:
	  host:
	    - pip
	    - python
	  run:
	    - python
	    - bwa=0.7.17
	    - htseq
	    - matplotlib
	    - numpy


Example
^^^^^^

::

	module load conda3/201903
	source activate changeseq_101220
	conda skeleton pypi changeseq
	conda-build .
	anaconda upload -u tsailabSJ /home/yli11/conda-bld/linux-64/changeseq-1.2.9-py27_0.tar.bz2
	conda-build --py 2.7 .
	conda convert --platform all /home/yli11/conda-bld/linux-64/guide_seq-1.0.2-py37_0.tar.bz2 -o py3_all
	for i in py3_all/*/*;do anaconda upload --force $i;done


## For my Macbook

/Users/yli11/opt/anaconda3/bin/anaconda

Contribute to bioconda
^^^^^^^^^^^

https://bioconda.github.io/contributor/setup.html



ref:

https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs-skeleton.html

https://stackoverflow.com/questions/30438216/how-do-i-upload-a-universal-python-wheel-for-python-2-and-3

https://anaconda.org/liyc1989/unique_color


How to use other installed conda (other people's conda)
^^^^^^^^^^^^^^^^^^^^^^


::

	export PATH=$PATH:/rgs01/project_space/tsaigrp/Genomics/common/anaconda3/condabin/
	eval "$(conda shell.bash hook)"
	conda activate /rgs01/project_space/tsaigrp/Genomics/common/anaconda3/envs/changeseq/

	module load bwa
	module load samtools/1.7
	module load homer/4.10
	python ~/dirs/changeseq/changeseq/changeseq.py parallel -m 10062018_Tn5_hg38_chr_only.yaml

::


	export PATH=$PATH:/rgs01/project_space/tsaigrp/Genomics/common/anaconda3/condabin/
	eval "$(conda shell.bash hook)"
	conda activate /rgs01/project_space/tsaigrp/Genomics/common/anaconda3/envs/changeseq_py3/

Use Helvetica
^^^^^

http://fowlerlab.org/2019/01/03/changing-the-sans-serif-font-to-helvetica/




