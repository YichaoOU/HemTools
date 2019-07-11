Inspection of multi-mapped reads
================================


Summary
^^^^^^^

Most programs will discard or ignore multi-mapped reads, such as cellRanger, featureCount (default), GATK, etc. Some programs considers multi-mapped reads such as kallisto, salmon, MACS2.

If duplication rate is high, for example, if STAR mapping statistics show less than 75% uniquely mapped reads, you might want to check if you have too many rRNA or chrM. 

This program also checks the HBG region.

In addition, this program will count number of reads mapped to hemoglobin genes.

.. note:: Currently, this pipeline only work on hg19.

Usage
^^^^^

Go to your data directory and type the following.

**Step 0: Load python version 2.7.13.**

.. code:: bash

    $ module load python/2.7.13

**Step 1: Prepare input files, generate fastq.tsv.**

.. code:: bash

    $ check_multi_mappers.py -f bam_list.tsv -g hg19


Sample input format
^^^^^^^^^^^^^^^^^^^

**bam_list.tsv**

This is a tab-seperated-value format file. The 2 columns are: bam file and output name.

::

	path_to_bam1	output_name1
	path_to_bam2	output_name2


Output
^^^^^^

Once the job is finished, you will receive an email with the statistics attached.

Basically, it shows the number (and percentage) of multi-mapped reads that are mapped to HBG, chrM, and rRNA. It also shows number of reads (including multi-mapped reads) mapped to hemoglobins.

``*.flag256.uniq.txt`` is the total number of multi-mapped reads, same as the number reported in STAR.

``*.flag256.{region}.uniq.txt`` is the number of multi-mapped reads in the input region, which is ``HBG``, ``chrM``, or ``rRNA``.

``flag256`` means ``secondary alignment``. For multi-mapped reads, only the first match will be set as ``primary alginment``. So this is a parameter to extract multi-mapped reads.

Number of mapped reads is shown in ``*.mapped.uniq.txt``.

Number of mapped reads in hemoglobin gene is shown in ``*.hem.uniq.txt``


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines




































