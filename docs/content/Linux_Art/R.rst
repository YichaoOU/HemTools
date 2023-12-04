Things about R
==============





Install R packages locally
^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes I can't wait for HPCF to install R packages for me. This is how to install R packages locally.

**CREAT R lib path**

Create a dir specifically for R packages. Use R version to create another dir. Our HPC has many different R version. Each of them have somewhat different packages. This is also my experience that some packages can only be installed in some R version.

.. code:: bash
	
	mkdir R
	cd R
	mkdir 3.5.1


.. code:: bash

	liyc="/home/yli11/R/3.5.1"
	install.packages("BiocManager",lib=liyc)
	library(BiocManager,lib.loc=liyc)
	## DESEQ2 1.22 has error for no replicate count table
	## BiocManager::install("DESeq2",lib=liyc)
	BiocManager::install(lib=liyc,version = '3.7')
	BiocManager::install("DESeq2",lib=liyc, version = "3.7")
	BiocManager::install("edgeR",lib=liyc)
	BiocManager::install("apeglm",lib=liyc)
	library(DESeq2,lib.loc=liyc)
	library(apeglm,lib.loc=liyc)
	
.. code:: bash

	library(devtools)
	with_libpaths(new = "/usr/lib/R/site-library/", install_github('rCharts', 'ramnathv'))


BioManager version
^^^^^^
::

	Error: Bioconductor version '3.9' requires R version '3.6
	remove.packages("BiocVersion")
	install.packages("BiocManager")

How should I deal with “package 'xxx' is not available (for R version x.y.z)” warning?
^^^^^^^^^

::

	setRepositories()

select 1 2 3 4 5 6 


R package dependency errors
^^^^^^^^^^^^^^^^

::

	DESeq2’: objects ‘rowSums’, ‘colSums’, ‘rowMeans’, ‘colMeans’ are not exported by 'namespace:biocgenerics

Today when I try to load DESeq2, I got the above error and took me a while to fix it.

Reason: This is caused by package dependency. I remember I tried installing signac and then I manually installed a lot of latest other packages, including S4vectors, Biocgenerics, and GenomeInfoDB, etc, which are incompatible with my R base version. 

The Fix: I manually fixed the package version to all my R base version using Biocmanager. My previous signac is 1.9, now I downgraded to 1.5. I probably need to create another conda env for the latest single cell analysis.

