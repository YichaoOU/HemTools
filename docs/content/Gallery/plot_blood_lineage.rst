Plot hematopoiesis intensity, blood lineage
============================

::

	usage: plot_blood_lineage.py [-h] -f INPUT
	                             [--custom_color_scale CUSTOM_COLOR_SCALE]
	                             [--svg_template SVG_TEMPLATE] [-o OUTPUT]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT, --input INPUT
	                        2 column tsv, no header, the values for each cell type
	                        (default: None)
	  --custom_color_scale CUSTOM_COLOR_SCALE
	                        You can define your own color scheme (linear from
	                        lowest to highest) using hex color, separated by comma
	                        (default: #ffffff,#ff8000,#660000)
	  --svg_template SVG_TEMPLATE
	  -o OUTPUT, --output OUTPUT
	                        output file name (default:
	                        yli11_2019-10-11_c2041fc5d83c)


Summary
^^^^^^^

Plot a value intensity colored hematopoiesis figure. 


.. image:: ../../images/plot_blood_lineage.PNG
  :align: center
  :scale: 50 % 


Input
^^^^^

A 2-col tsv file where you only need to modify the second column with your own value.

There are 13 cell types in this figure, you have to give values for all of them. The first column is the keyword.

::

	HSC	4
	MPP	4
	LMPP	5
	CLP	4.5
	GMP	4
	MEP	-2
	CMP	0
	CD4	4
	CD8	4
	B	6
	NK	4
	Mono	5
	Ery	4

Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13 

	plot_blood_lineage.py -f input.tsv

Example
^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13 

	plot_blood_lineage.py -f ~/HemTools/share/misc/values.tsv


Output
^^^^^

A SVG figure and a colorbar pdf. They will be emailed to you as well.



