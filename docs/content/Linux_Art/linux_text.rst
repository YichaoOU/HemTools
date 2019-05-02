Linux text file operations
==========================



Remove the first line from a file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	sed -i '1d' file.txt



Column operations
^^^^^^^^^^^^^^^^^

.. code:: bash

	awk -F "\t" '{print $2"\t"$3"\t"$4"\t"$1}' tmp.out > tmp.out.bed










