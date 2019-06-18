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


