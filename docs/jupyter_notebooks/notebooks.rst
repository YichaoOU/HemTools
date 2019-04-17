A collection of Jupyter Notebooks
=================================

.. toctree::
   :maxdepth: 1
   :glob:

   *


Use R and Python in Jupyter Notebook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, create a conda environment: 

.. code:: bash

	conda create -n Rplot

Then, activate this envrionment: 

.. code:: bash

	(Windows OS) conda activate Rplot

	(Linux / Mac) source activate Rplot

Then, do the following:

.. code:: bash

	conda install -c bioconda r-pheatmap

	conda install -c r r-irkernel

	conda install -c anaconda jupyter

	conda install -c anaconda pandas

	conda install -c anaconda seaborn

Last, type ``jupyter notebook`` and you should be able to run R and Python in the same jupyter notebook.

FAQ
^^^

**1. no 'R' in jupyter notebook**

These could due to many reason.

One note: on the same computer, just within 2 week, `conda install -c r r-irkernel` worked for me. But now, after I reinstalled conda, it didn't. 

First, check if you can see ir in `jupyter kernelspec list`? For me, I can't see it. Then I did: R -> `install.packages('IRkernel')` -> `IRkernel::installspec(user = FALSE)`

ref: https://github.com/IRkernel/IRkernel/issues/163
https://irkernel.github.io/installation/

**2. add python2 to a jupyter notebook (python3)**

Can't use conda install. Tried but permission denied. Should do the following:

`python2 -m pip install ipykernel`

`python2 -m ipykernel install --user`

Then reinstall pandas, seaborn for python2.

`python2 -m pip install pandas`

`python2 -m pip install seaborn`

**3. add your conda env python to jupyter notebook**

sometime python will be installed on your local conda env when you specifying python version. and jupyter notebook won't add this python automatically.

`python -m pip install ipykernel`

`python -m ipykernel install --user --name myenv --display-name "Python (myenv)"`

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: notebooks











