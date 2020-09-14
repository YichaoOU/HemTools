Convert BCL basecall files to FASTQ files
=========================================

.. tip:: For demultiplexing, you must provide ``SampleSheet.csv``; otherwise, all fastq.gz files will be named as ``Undetermined``.

.. note:: Please note that there should be no spaces (i.e., only spaces and _ is allowed) in sample_ID (e.g., see some incorrect examples below). A unique sample_ID is also preferred. 

.. image:: ../../images/no_space_bcl2fastq.PNG
	:align: center
	
**Step 1**

.. highlight:: none

:: 

	hpcf_interactive -q standard -R "rusage[mem=32000]"

**Step 2**

.. code:: bash

	module load bcl2fastq

**Step 3**

.. code:: bash

	bcl2fastq --no-lane-splitting -o fastq_files

Once finished, you should be able to see the fastq files in folder `fastq_files`.

.. tip:: By default, one mismatch is allowed for demultiplexing. If you want to allow for two mismatches, type the command below:

.. code:: bash

	bcl2fastq --no-lane-splitting -o fastq_files --barcode-mismatches 2


Manually reverse complement R2 index
^^^^^^^^^^^^^^^^^^^^^^^^

In some cases, (possible sequencer differences?), users have to manually get revcomp seq of R2 index. So in this case, you can use http://arep.med.harvard.edu/labgc/adnan/projects/Utilities/revcomp.html to get a list of revcomp sequences and copy and replace old index. Upload new sample sheet csv to HPC and run:

.. code:: bash

	bcl2fastq --sample-sheet SampleSheet2.csv --no-lane-splitting -o fastq_files2


Wierd special char in your samplesheet.csv
^^^^^^^^^^^^^^^^^

<U+FEFF> character showing up in files. How to remove them?

https://gist.github.com/szydan/b225749445b3602083ed

::


	1) In your terminal, open the file using vim:

	vim file_name
	2) Remove all BOM characters:

	:set nobomb
	3) Save the file:

	:wq



Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines

