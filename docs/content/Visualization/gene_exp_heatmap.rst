Gene expression heatmap
=======================

::

	usage: plot_gene_exp_heatmap.py [-h] -f INPUT --sort_by SORT_BY
	                                [--remove_cols REMOVE_COLS] [-o OUTPUT] [-pdf]
	                                -W WIDTH -H HEIGHT [--log2_transform]

	plot heatmap given dataframe.

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT, --input INPUT
	                        data table input (default: None)
	  --sort_by SORT_BY     usually this column should be logFC (default: None)
	  --remove_cols REMOVE_COLS
	  -o OUTPUT, --output OUTPUT
	                        output table name (default:
	                        gene_exp_heatmap.yli11_2019-10-09)
	  -pdf                  plot pdf instead of png, can be slower for large
	                        dataset (default: False)
	  -W WIDTH, --width WIDTH
	                        Figure width, maximal use 200, usually 8 to 20
	                        (default: None)
	  -H HEIGHT, --height HEIGHT
	                        Figure height, maximal use 200, usually 10 to 50
	                        (default: None)
	  --log2_transform      input values will be log2 transformed (default: False)


Summary
^^^^^^^

This program won't do clustering on genes or samples, purely put your input to a heatmap where each gene's expression values across different samples are z-normalized. When the number of genes is less than 100, it will show the gene name. Otherwise, just a heatmap.



::

	hpcf_interactive

	module load python/2.7.13

	plot_gene_exp_heatmap.py -f fdr01.csv --remove_cols AveExpr,t,P.Value,adj.P.Val,B --sort_by logFC -W 8 -H 25 -pdf -o test_heatmap



