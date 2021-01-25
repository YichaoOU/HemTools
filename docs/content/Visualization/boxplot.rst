Boxplot
=======


Input
^^^^^^


list of values, each list is a separate file, with just numerical values, no header. "%" is OK.




Boxplots of two list with statistical significance
^^^^^^^^^^^^^^^^^^^

::

	boxplot_two_list.py -l1 A.list -l2 B.list

Boxplots of any number of lists
^^^^^^^^^^^^^^^^^^^^^

This script use dynamic arguments with argparse, user define the parameters, such as ``--regular``, and then the "regular" will be the label for the given input list.

::

	box_plot_any_num_list.py --regular control.list --CHANGE_seq_01212021 CHANGE_seq_01212021.list --CHANGE_seq_11142020 CHANGE_seq_11142020.list  --ylabel "%chrM"






