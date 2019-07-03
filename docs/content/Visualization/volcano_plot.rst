Volcano plot for logFC and P-value/FDR
======================================

.. argparse::
   :filename: ../bin/HemTools
   :func: main_parser
   :prog: HemTools
   :path: volcano_plot

.. image:: ../../images/volcano.png
	:align: center

Input file
^^^^^^^^^^

**INPUT: data table (-f option, required).**

This is a data table, could be csv (default) or tsv. Seperator is provided by user. Basically, two columns (provided by user) will be used to make volcano plot. 

Usage
^^^^^

.. code:: bash

    HemTools volcano_plot -f diffPeaks_output.txt -s "\t" --LFC_column logFC --FDR_column adj.P.Val

.. note:: Once the figure is made, it will be emailed to you.

Report bug
^^^^^^^^^^

Once the job is finished, you will be notified by email with some attachments.  If no attachment can be found, it might be caused by an error. In such case, please go to the result directory (where the log_files folder is located) and type: 

.. code:: bash

    HemTools report_bug


R code
^^^^^^

If you are not satisfied with the figure (figsize, dpi, point size, etc), here's the source code for you to customize your figure. 

.. literalinclude:: ../../../subcmd/volcano_plot.R
   :language: R
   :linenos:



















