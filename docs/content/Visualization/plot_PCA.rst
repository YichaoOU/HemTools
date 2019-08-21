Visualizing high-dimentional data using PCA or UMAP
=================================

::

	usage: plot_PCA.py [-h] [-j JID] [--remove_zero] [--index] [--transpose] -f
	                   INPUT [--index_using INDEX_USING] [-s SEP]
	                   [--xlabel XLABEL] [--ylabel YLABEL]
	                   [--remove_cols REMOVE_COLS]
	                   [--color_by_a_col COLOR_BY_A_COL]
	                   [--color_by_a_feature COLOR_BY_A_FEATURE]
	                   [--UMAP_min_dist UMAP_MIN_DIST] [--UMAP_metric UMAP_METRIC]
	                   [--UMAP_n_neighbors UMAP_N_NEIGHBORS] [--title TITLE]
	                   [--label_by_first_element] [--label_by_meaningful_name]
	                   [--UMAP] [--save_projection_df] [--continous_color]
	                   [--figure_type FIGURE_TYPE] [-o OUTPUT] [--header]
	                   [--no_col_names] [--no_row_names] [-W WIDTH] [-H HEIGHT]
	                   [--just_default] [--log2_transform] [--just_plot]

	plot heatmap given dataframe.

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        plot_PCA_yli11_2019-08-16)
	  --remove_zero         remove all rows or cols that are zero (default: False)
	  --index               index is false (default: False)
	  --transpose           df transpose (default: False)
	  -f INPUT, --input INPUT
	                        data table input (default: None)
	  --index_using INDEX_USING
	                        Sometimes we want to show a different label for the
	                        indices, then use this option. For example, gene id is
	                        unique, however, gene name can be different, it also
	                        has upper or lower case problem, in such case, we want
	                        to use gene id for data processing and use gene name
	                        for visualization. (default: )
	  -s SEP, --sep SEP     separator (default: )
	  --xlabel XLABEL
	  --ylabel YLABEL
	  --remove_cols REMOVE_COLS
	  --color_by_a_col COLOR_BY_A_COL
	  --color_by_a_feature COLOR_BY_A_FEATURE
	  --UMAP_min_dist UMAP_MIN_DIST
	  --UMAP_metric UMAP_METRIC
	  --UMAP_n_neighbors UMAP_N_NEIGHBORS
	  --title TITLE
	  --label_by_first_element
	  --label_by_meaningful_name
	  --UMAP
	  --save_projection_df
	  --continous_color
	  --figure_type FIGURE_TYPE
	                        pdf,png,jpeg (default: png)
	  -o OUTPUT, --output OUTPUT
	                        output table name (default: yli11_2019-08-16)
	  --header              input table has header (default: False)
	  --no_col_names        Don't show column names in the heatmap (default:
	                        False)
	  --no_row_names        Don't show row names in the heatmap (default: False)
	  -W WIDTH, --width WIDTH
	                        Figure width, by default, w=N_row/4, if given, will
	                        replace the default value (default: 500)
	  -H HEIGHT, --height HEIGHT
	                        Figure height, by default, w=N_col/4, if given, will
	                        replace the default value (default: 500)
	  --just_default        just plot using default seaborn parameters (default:
	                        False)
	  --log2_transform      input values will be log2 transformed (default: False)
	  --just_plot           with this option, no filters will be applied. This
	                        program will just plot a heatmap based on the input
	                        dataframe (default: False)


Summary
^^^^^^^

Given a dataframe, make a PCA or UMAP plot. 

Example
^^^^^^^

.. image:: ../../images/pca_plot.png
	:align: center


Input
^^^^^

Data table, tsv (default) or csv (``-s ,``). If data table contains both row names and column names, use ``--index --header``

Usage
^^^^^

.. code:: bash

    hpcf_interactive -q standard -R "rusage[mem=10000]"

    module load conda3

    source activate /home/yli11/.conda/envs/py2/

**Example usage**

.. code:: bash

	plot_PCA.py -f /home/yli11/HemPortal/RNA_seq/erythopoesis_expr.transcript.tpm --index --header --transpose --label_by_first_element


Note that ``--index --header`` specifies that the input data has column names and row names. 

In the input, we assume columns are used as features and rows are used as samples, in other words, the number of dots in the output figure is equal to the row names. (This is a general machine learning format.)

In the input example, the rows are actually the features, so I need to do a matrix transpose, use ``--transpose``.

In the input example, we don't have a label column, and we just want to use the row names as the label, use ``--label_by_first_element``.


Usage-UMAP
^^^^^

**Example usage**

.. code:: bash

	plot_PCA.py -f /home/yli11/HemPortal/RNA_seq/blood/combined_gene_exp/merged_gene_exp.tsv --UMAP --index --header --transpose 

Or try different parameters:

.. code:: bash
	plot_PCA.py -f merged_gene_exp.tsv --index --header --transpose --UMAP --label_by_meaningful_name --UMAP_min_dist 0.7 --UMAP_n_neighbors 7


Output
^^^^^^

This is an interactive figure, please open the html file.


Data exploration for machine learning projects
^^^^^^

**Input**

Standard ML format uses row for individual samples/instances and column for individual features/predictors. There is another column for the labels if it is supervised learning.

**Aim**

Visualze the sample distribution given selected features.

**Usage**

.. code:: bash

	hpcf_interactive -q standard -R "rusage[mem=10000]"

	module load conda3

	source activate /home/yli11/.conda/envs/py2/

	plot_PCA.py -f input.csv --color_by_a_col label --header -s , --UMAP

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines















































