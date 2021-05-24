single-cell RNA-seq analysis
============================







projection
^^^^^^^^^^

This is quite simple that 

https://www.nature.com/articles/nmeth.4644.pdf

we carried out a form of k-nearest
-neighbor classification with only cosine similarity. >0.5. three nearest neighbors


For the
number of features, we used the top 100, 200, 500, 1,000, 2,000,
5,000, or all genes. We calculated similarities by using the cosine
similarity and Pearson and Spearman correlations, which are
restricted to the interval [−1, 1] and are thus insensitive to differences in scale between data sets. We required that at least two
of the similarities be in agreement, and that at least one be >0.7.
If these criteria were not met, then c was labeled as “unassigned”
to indicate that it did not correspond to any cell type present
in the reference. For the approximate nearest neighbor search,
which we refer to as scmap-cell, we carried out a form of k-nearest
-neighbor classification with only cosine similarity. For a cell type
to be assigned, we required that the three nearest neighbors have
the same cell type and that the highest similarity among them
be >0.5.


A list of python repos
^^^^^^^^^^^^^^^^^^^^^^

**QC**

https://github.com/parklab/PaSDqc

**Data cleaning**

https://github.com/theislab/dca


**differential analysis**

https://github.com/theislab/diffxpy

**trajectory**

https://github.com/theislab/scvelo


**Integration**

https://github.com/mukamel-lab/SingleCellFusion

**not sure**

https://github.com/lingxuez/URSM

https://github.com/seandavi/awesome-single-cell

https://github.com/logstar/scedar



Seurat installation
^^^^^^^^^^^^^

::
	conda create -n single_cell
	conda activate single_cell
	conda install -c bioconda r-seurat
	conda install -c anaconda libopenblas


Another installation: https://github.com/satijalab/seurat/issues/1619

Seurat does not return batch-corrected expression values (if we did, we would not be able to compare expression values over different conditions, as these would be subtracted).

https://github.com/satijalab/seurat/issues/283


get batch corrected gene distance

https://github.com/satijalab/seurat/issues/1118







