convert dataframe to html
======================


::

	usage: dataframe_to_html.py [-h] -f INPUT [-o OUTPUT] [-s SEP] [-w WIDTH]
	                            [-H HEIGHT] [--sort SORT] [--motif]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT, --input INPUT
	                        dataframe (default: None)
	  -o OUTPUT, --output OUTPUT
	                        output name (default: output.html)
	  -s SEP, --sep SEP     output name (default: )
	  -w WIDTH, --width WIDTH
	                        output name (default: 200)
	  -H HEIGHT, --height HEIGHT
	                        output name (default: 200)
	  --sort SORT           sort by column name (default: None)
	  --motif               generate motif html (default: False)



Summary
^^^^^^^

Convert a dataframe to html table. This html table can be further converted to pdf table.

Input
^^^^^

A data frame

Output
^^^^^^

html


Usage
^^^^^

Suppose all your bam files are in the current working dir.

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	dataframe_to_html.py -f input.csv -s , 

The following is specific to generate motif table.

.. code:: bash	

	dataframe_to_html.py -f motif_report.csv -s , -w 100 -H 50 --sort "Motif p_value" --motif


Convert html to pdf:

.. code:: bash

	pandoc output.html -t latex -o test.pdf -V geometry:a3paper


