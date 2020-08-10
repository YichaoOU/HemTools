Visualize genomic loci (overview)
===================================



Summary
^^^^^^^

We are using this R library.

https://cran.r-project.org/web/packages/chromoMap/vignettes/chromoMap.html


Input
^^^^^

1. chrom size bed

::

	chr1	0	249250621
	chr2	0	243199373
	chr3	0	198022430
	chr4	0	191154276
	chr5	0	180915260
	chr6	0	171115067
	chr7	0	159138663


2. annotation bed

::

unique_label1	chr1	123456789	123456790	value_or_label
unique_label2	chr2	start	end	value_or_label
unique_label3	chr3	zz	aa	value_or_label
unique_label4	chr4	cc	dd	value_or_label

The plot resolution is about 3MB per locus, so if two loci are less than 3MB distance, it will only plot one locus.


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load conda3

	source activate /home/yli11/.conda/r_env

	to_chromoMap.R hg19_main.chrom_sizes.bed annot.bed


Output
^^^^^^

``chromoMAP_output.pdf`` and ``chromoMAP_output.html``


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines

