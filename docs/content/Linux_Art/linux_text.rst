Linux text file operations
==========================



Remove the first line from a file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	sed -i '1d' file.txt


Replace string in file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	sed -i 's/original/new/g' file.txt

Column operations
^^^^^^^^^^^^^^^^^

.. code:: bash

	awk -F "\t" '{print $2"\t"$3"\t"$4"\t"$1}' tmp.out > tmp.out.bed
	awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$4}' tmp.out > tmp.out.bed
	awk -F "\t" '{print $1"\t"$2"\t"$3}' tmp.out > tmp.out.bed
	awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$1":"$2"-"$3}' test.bed > test2.bed

Calculating read average length in a Fastq file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash
	awk '{if(NR%4==2) {count++; bases += length} } END{print bases/count}' <fastq_file>



http://www.filiphusnik.com/content/bioinformatics-one-liners


Remove path and file ending suffix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	for i in ../*; do echo $(basename $i .narrowPeak);done

Delete files/dir based on dates
^^^^^^^^^^^^^^^^^^^^^^

https://stackoverflow.com/questions/17945538/delete-directory-based-on-date

::
	python -m ipykernel install --user --name dash_env --display-name "Python (dash_env)"
