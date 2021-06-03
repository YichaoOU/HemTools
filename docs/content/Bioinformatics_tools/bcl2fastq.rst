Convert BCL basecall files to FASTQ files
=========================================

.. tip:: For demultiplexing, you must provide ``SampleSheet.csv``; otherwise, all fastq.gz files will be named as ``Undetermined``. You have to upload ``SampleSheet.csv`` to the dir that conatins BCL files on HPC. Below is what this dir should look like (and the files and subfolders it should contain, not including fastq_files folder):

.. image:: ../../images/BCL2fastq_dir.PNG
	:align: center

See this for SampleSheet format details: https://www.illumina.com/content/dam/illumina-marketing/documents/products/technotes/sequencing-sheet-format-specifications-technical-note-970-2017-004.pdf

You can download an example SampleSheet.csv here: https://github.com/YichaoOU/HemTools/tree/master/docs/gallery/SampleSheet.csv

.. note:: Please note that there should be no spaces (i.e., only _ is allowed, for special char) in sample_ID (e.g., see some incorrect examples below). A unique sample_ID is also preferred. 


.. note:: We found that for Miniseq and Nextseq, your R2 index in samplesheet.csv have to be reverse complemented. For Miseq, everything is normal.

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

In some sequencer, e.g., miniseq or Nextseq, users have to manually get revcomp seq of R2 index. So in this case, you can use http://arep.med.harvard.edu/labgc/adnan/projects/Utilities/revcomp.html to get a list of revcomp sequences and copy and replace old index. Upload new sample sheet csv to HPC and run:

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


Mising bcl
^^^^^^^^^


Question: "I have a pair-end 150bp sequencing run that stopped in the middle at about 150cycles. I think that it should contain the data that I need for the analysis. But when I do bcl files to fastq files, it showed error "Unable to find BCL file for 's_1_1102' in"

Solution: Add ``--ignore-missing-bcls`` option. 

For example: ``bcl2fastq --no-lane-splitting -o fastq_files --ignore-missing-bcls``


Which delmultiplexing pipeline I should use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


https://support.illumina.com/bulletins/2016/04/adapter-trimming-why-are-adapter-sequences-trimmed-from-only-the--ends-of-reads.html


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines

