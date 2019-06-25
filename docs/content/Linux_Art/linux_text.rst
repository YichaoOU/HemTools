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
	awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$4}' tmp.out > tmp.out.bed
	awk -F "\t" '{print $1"\t"$2"\t"$3}' tmp.out > tmp.out.bed


Calculating read average length in a Fastq file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash
	awk '{if(NR%4==2) {count++; bases += length} } END{print bases/count}' <fastq_file>



http://www.filiphusnik.com/content/bioinformatics-one-liners


Remove path and file ending suffix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	for i in ../*; do echo $(basename $i .narrowPeak);done
	