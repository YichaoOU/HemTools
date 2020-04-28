Data table operations
=====================



Subset tables or remove rows with all zeros
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	usage: dataframe.py [-h] [--remove_zero] [--row] [--col] [--index] [-f INPUT]
	                    [--merge MERGE] [--subset SUBSET] [-s SEP] [-o OUTPUT]
	                    [--header]

	optional arguments:
	  -h, --help            show this help message and exit
	  --remove_zero         remove all rows or cols that are zero (default: False)
	  --row                 results on rows. This is to the opposite of pandas row
	                        and col, which is operations on rows or cols. For
	                        example, operations (e.g., find zeros) on cols will
	                        result in removing rows. (default: False)
	  --col                 results on cols (default: False)
	  --index               index is false (default: False)
	  -f INPUT, --input INPUT
	                        data table input (default: None)
	  --merge MERGE         merge with a data frame (default: )
	  --subset SUBSET       subset a data frame with a list (default: None)
	  -s SEP, --sep SEP     separator (default: )
	  -o OUTPUT, --output OUTPUT
	                        output table name (default:
	                        yli11_2020-04-28_fa0d37b6dfaa.csv)
	  --header              input table has header (default: False)



**Example: subset csv given a list**

::

	==> df1.txt <==
	x,sd1,sd2
	a,454,23
	b,5.3,sd2

	==> list.txt <==
	sd2


.. code:: bash

	dataframe.py -f df1.txt -s "," --subset list.txt -o output.csv

If your input is bed file, use ``-s "\t"``

::

	==> output.csv <==
	x,sd1,sd2
	b,5.3,sd2


**Example: remove all zeros**

::

	==> df1.txt <==
	x,sd1,sd2
	1,4,5
	0,0,0


.. code:: bash

	dataframe.py -f df1.txt -s "," --remove_zero -o output.csv --header

If your input is bed file, use ``-s "\t"``

::

	==> output.csv <==
	x,sd1,sd2
	1,4,5







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
























