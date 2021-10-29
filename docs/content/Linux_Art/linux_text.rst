Linux text file operations
==========================



Remove the first line from a file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	sed -i '1d' file.txt

Remove the first 5 lines from a file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	sed -i '1,5d' gencode.v38.annotation.gtf


If you need the first 100 characters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

	cat file |colrm 101 


Replace string in file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	sed -i 's/original/new/g' file.txt

Add string to the beginning of each line in a file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	sed -i -e 's/^/prefix/' file
	## for example, add hg_ to each line
	# head gencode.v38.annotation.gtf | sed -e 's/^/hg_/' - 
	sed -e 's/^/hg_/' gencode.v38.annotation.gtf > hg_gencode.v38.annotation.gtf
	sed -e 's/^/mm_/' gencode.vM27.annotation.gtf > hg_gencode.vM27.annotation.gtf

Column operations
^^^^^^^^^^^^^^^^^

.. code:: bash

	awk -F "\t" '{print $2"\t"$3"\t"$4"\t"$1}' tmp.out > tmp.out.bed
	awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$4}' tmp.out > tmp.out.bed
	awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$4"\t"$8}' tmp.out > tmp.out.bed
	awk -F "\t" '{print $1"\t"$2"\t"$3}' tmp.out > tmp.out.bed
	awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$1":"$2"-"$3}' test.bed > test2.bed
	awk -F "\t" '{print ($1"\t"($2-2000<0?0:$2-2000)"\t"$3+2000"\t"$5)}' hg19.wgEncodeGencodeBasicV27lift37.all.tss.bed > gencodeV27.all.tss2kb.bed

Select lines based on a column value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	awk -F"\t" '$5 == 0 { print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6 }' matches.bed.sorted > matches.bed


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


https://askubuntu.com/questions/50170/how-to-convert-pdf-to-image

set attr
^^^^^^

::

	[yli11@splprhpc05 learned_model_6]$ attr -s test -V 123 webpage_6.html
	Attribute "test" set to a 3 byte value for webpage_6.html:
	123
	[yli11@splprhpc05 learned_model_6]$ ls webpage_6.html
	webpage_6.html
	[yli11@splprhpc05 learned_model_6]$ ll -rht webpage_6.html
	-rwxr-xr-x 1 yli11 chenggrp 2.0K Oct 11  2019 webpage_6.html
	[yli11@splprhpc05 learned_model_6]$ getfa
	getfacl   getfattr
	[yli11@splprhpc05 learned_model_6]$ getfa
	getfacl   getfattr
	[yli11@splprhpc05 learned_model_6]$ getfattr -d webpage_6.html
	# file: webpage_6.html
	user.test="123"

combine figures
^^^^^^^^^

::

	convert *rev.png -append control_combined_rev.png
