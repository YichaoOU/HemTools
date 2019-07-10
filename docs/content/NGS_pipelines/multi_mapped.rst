Inspection of multi-mapped reads
================================


Summary
^^^^^^^

If duplication rate is high, for example, if STAR mapping statistics show less than 75% uniquely mapped reads, you might want to check if you have too many rRNA or chrM. This program also checks the HBG region.

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



Output
^^^^^^

You can do ``head *.uniq.txt``. 

``*.flag256.uniq.txt`` is the total number of multi-mapped reads, same as the number reported in STAR.

``*.flag256.{region}.uniq.txt`` is the number of multi-mapped reads in the input region, which is ``HBG``, ``chrM``, or ``rRNA``.

Reference
^^^^^^^^^



Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines




































