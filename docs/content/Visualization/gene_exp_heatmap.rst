Gene expression heatmap
=======================

::

	usage: plot_gene_exp_heatmap.py [-h] -f INPUT --sort_by SORT_BY
	                                [-c1 VALUE_CUTOFF_MAX] [-c2 VALUE_CUTOFF_MIN]
	                                [--index_by INDEX_BY]
	                                [--remove_cols REMOVE_COLS] [-o OUTPUT] [-pdf]
	                                -W WIDTH -H HEIGHT [--fontsize FONTSIZE]
	                                [--linewidths LINEWIDTHS] [--log2_transform]
	                                [--show_name]

	plot heatmap given dataframe.

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT, --input INPUT
	                        data table input (default: None)
	  --sort_by SORT_BY     usually this column should be logFC (default: None)
	  -c1 VALUE_CUTOFF_MAX, --value_cutoff_max VALUE_CUTOFF_MAX
	                        subset genes by filtering out values above the cutoff,
	                        usually it should be p-value, input should be:
	                        column_name,value (default: None)
	  -c2 VALUE_CUTOFF_MIN, --value_cutoff_min VALUE_CUTOFF_MIN
	                        subset genes by filtering out values below the cutoff,
	                        usually it should be log p-value, input should be:
	                        column_name,value (default: None)
	  --index_by INDEX_BY   if the first column is not the correct index, which
	                        one? (default: None)
	  --remove_cols REMOVE_COLS
	  -o OUTPUT, --output OUTPUT
	                        output table name (default:
	                        gene_exp_heatmap.yli11_2020-08-26)
	  -pdf                  plot pdf instead of png, can be slower for large
	                        dataset (default: False)
	  -W WIDTH, --width WIDTH
	                        Figure width, maximal use 200, usually 8 to 20
	                        (default: None)
	  -H HEIGHT, --height HEIGHT
	                        Figure height, maximal use 200, usually 10 to 50
	                        (default: None)
	  --fontsize FONTSIZE   you can choose from 8 to 20 (default: 10)
	  --linewidths LINEWIDTHS
	                        you can choose from 0, 0.1 (default: 0.1)
	  --log2_transform      input values will be log2 transformed (default: False)
	  --show_name           by default, >100 genes, name will not be shown, this
	                        option enforce to show name (default: False)



Summary
^^^^^^^

This program won't do clustering on genes or samples, purely put your input to a heatmap where each gene's expression values across different samples are z-normalized. When the number of genes is less than 100, it will show the gene name. Otherwise, just a heatmap.



Input
^^^^^

The input file can be csv or tsv, the separator will be automatically inferred by the program.

The first column should be gene name or any sort of unique IDs.

The first row should be column names.

The other columns should be gene expression values. Non-relevant columns can be removed by ``--remove_cols`` option.


::

	gene	logFC	AveExpr	t	P.Value	adj.P.Val	B	WT_1_log2CPM	WT_2_log2CPM	WT_3_log2CPM	KO_1_log2CPM	KO_2_log2CPM	KO_3_log2CPM
	D17H6S56E-5	-3.083	9.3418	-97.669	2.2768E-15	3.5976E-11	25.102	10.888	10.91210.85	7.7671	7.8119	7.8218
	Scd1	-2.2133	6.106	-50.068	1.1512E-12	9.0952E-09	19.799	7.2574	7.1911	7.192	5.0828	4.9264	4.9864
	Coro2a	-1.4558	7.9154	-46.998	2.0739E-12	1.0923E-08	19.285	8.6433	8.6614	8.62567.1924	7.2202	7.1495


Usage
^^^^^

Using the above example, we want to remove columns ``--remove_cols AveExpr,t,P.Value,adj.P.Val,B``. 

We also want to sort our data matrix by ``--sort_by logFC``. Note that this option will also remove this column.

Depending on your data matrix size,in my example, I have 2004 genes and 6 samples, I'm using the figure size ``-W 8 -H 25``.

::

	hpcf_interactive

	module load python/2.7.13

	plot_gene_exp_heatmap.py -f fdr01.csv --remove_cols AveExpr,t,P.Value,adj.P.Val,B --sort_by logFC -W 8 -H 25 -pdf -o test_heatmap

You can control font size using ``--fontsize`` option.


plot top diff genes after diff gene pipeline:


::

	hpcf_interactive

	module load python/2.7.13

	plot_gene_exp_heatmap.py -f e6e7_vs_control.gene.final.combined.tpm.csv --index_by ext_gene -c1 qval,0.001 --sort_by logFC --remove_cols pval,num_aggregated_transcripts,X,treatment_mean,control_mean -W 5 -H 20 --show_name

	OR:

	for i in *.csv;do plot_gene_exp_heatmap.py -f $i --index_by ext_gene -c1 qval,0.001 --sort_by logFC --remove_cols pval,num_aggregated_transcripts,X,treatment_mean,control_mean -W 5 -H 20 --show_name -o $i;done


