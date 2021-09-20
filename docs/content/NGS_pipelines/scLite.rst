scJupyter for single cell integration, annotaiton, modeling and reporting
======================================


Tested in mouse scRNA-seq and CITE-seq data.

Current analysis steps
^^^^^^^^^^^^^^^

1. combine multiple 10x outputs

2. performance integration without Harmony batch correction
	
3. generate 2D and 3D PCA/UMAP.

	- user can check if batch correction is needed.

4. cell type annotation

	- scCatch

	- hscScore

	- clustifyr 

	- known marker

	- de novo marker

5. GO/pathway enrichment for de novo marker

6. pairwise DEG/DA analysis

7. cluster size differences


Future steps
^^^^^^^^^^^


gene network

velocity

Input
^^^^^^

The first input is a yaml file specifying all parameters.

input.yaml
----------

::

	[yli11@nodecn203 single_cell_rwu_2021-05-10]$ head -n 20 input.yaml 
	# global parameters
	outputLabel: rick_test2
	species: Mouse
	known_markers: /home/yli11/HemTools/share/misc/markers.tsv
	mouse_scRNA: /home/yli11/HemTools/share/misc/NicheData10x.rda
	cite_seq: FALSE
	sample_info: input.tsv

sample_input
----------

This is a 2-col tsv file. First column is sample name and the second name is the abs/relative path to 10x output.

::

	[yli11@nodecn203 single_cell_rwu_2021-05-10]$ head input.tsv 
	Root_no_diff	2175650_R2-69-3_S13_results/2175650_R2-69-3_S13/outs/filtered_feature_bc_matrix
	NT_gRNA_diff	2175649_R2-69-2_S12_results/2175649_R2-69-2_S12/outs/filtered_feature_bc_matrix
	mKLF1_gRNA_diff	2175648_R2-69-1_S11_results/2175648_R2-69-1_S11/outs/filtered_feature_bc_matrix



Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	# prepare the input and go do your working dir

	run_lsf.py -p scJupyter -m 40000



Output
^^^^^^

All output figures and tables are stored in ``scJupyter_[outputLabel]_[Data]`` folder. HPC log files are stored in the ``jid`` folder.


