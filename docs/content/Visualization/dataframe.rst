Data table operations
=====================


Merge tables by row names (Any number)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	usage: dataframe_merge.py [-h] [-s SEP] [--index_col INDEX_COL] [--glob GLOB]
	                          [--header_list HEADER_LIST] [--drop DROP]
	                          [--name_col_with_filename NAME_COL_WITH_FILENAME]
	                          [--rename_col_with_filename] [--intersection]
	                          [-o OUTPUT]
	                          file [file ...]

	merge input dataframes using row index. Assume input tables contain both row
	names and column names.

	positional arguments:
	  file

	optional arguments:
	  -h, --help            show this help message and exit
	  -s SEP, --sep SEP     this program can infer separator automatically, but it
	                        may fail. Use auto if the input tables contain
	                        different separators. (default: auto)
	  --index_col INDEX_COL
	                        which col to use as index (default: 0)
	  --glob GLOB           glob the current dir with file name match to given
	                        string (default: None)
	  --header_list HEADER_LIST
	                        sep by , define your own colum names (default: None)
	  --drop DROP           try drop this column(s), seperated by , (default:
	                        None)
	  --name_col_with_filename NAME_COL_WITH_FILENAME
	  --rename_col_with_filename
	  --intersection        merge dataframes only on overlapping row names
	                        (default: False)
	  -o OUTPUT, --output OUTPUT
	                        output table name (default:
	                        yli11_2019-10-08_c88dbe184e44.tsv)


.. note:: This program assumes input tables contain both row names and column names.


**Example: Merge one csv and one tsv**

::

	==> df1.txt <==
	x,sd1,sd2
	a,454,23
	b,5.3,4.5

	==> df2.txt <==
	x	ff4	yy6
	a	34	77
	c	33	23

The program can guess the file format (only for csv or tsv). If you only need the overlapping rows, use ``--intersection``

.. code:: bash

	dataframe_merge.py df1.txt df2.txt --intersection

	df1.txt shape: 2 X 2
	df2.txt shape: 2 X 2
	Merged table shape: 1 X 4
	Output to table: yli11_2019-08-05_c060b1dec3db.tsv

::

	==> yli11_2019-08-05_c060b1dec3db.tsv <==
	x	sd1	sd2	ff4	yy6
	a	454.0	23.0	34	77
























