check sample barcode frequency in index reads
======================

::

	barcode_frequency.py [Undertermined_R1.fastq.gz]


Usage
^^^^

::

	barcode_frequency.py Undertermined_R1.fastq.gz


Output
^^^^^^

1. Barcode_count_table.csv
----------

This is usually what we need. A sorted frequency table for each barcode pair.

2. Barcode_raw_table.csv
----------

Raw read names and barcode table.


Barcode frequency in 5'-end
==================

create a working dir and copy your ``Undetermined_S0_R1_001.fastq.gz`` here.

::

	gunzip Undetermined_S0_R1_001.fastq.gz

	module load homer/4.10

	homerTools barcodes 8 Undetermined_S0_R1_001.fastq -min 1

By default, homer checks the first 8bp frequency and output each 8bp to a file.