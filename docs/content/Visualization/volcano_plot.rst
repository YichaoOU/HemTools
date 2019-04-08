Volcano plot for logFC and P-value/FDR
======================================

.. argparse::
   :filename: ../bin/HemTools
   :func: main_parser
   :prog: HemTools
   :path: volcano_plot

Input file
^^^^^^^^^^

**INPUT: data table (-f option, required).**

This is a data table, could be csv (default) or tsv. Seperator is provided by user. Basically, two columns (provided by user) will be used to make volcano plot. 

Usage
^^^^^

.. code:: bash

    $ HemTools volcano_plot -f input_data

.. note:: EnhancedVolcano is installed on rhel7. This subcmd is not interative. Please wait for the job finished in order to see the figure.





















