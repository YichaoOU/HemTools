Paired-end ChIP-seq
===================



Summary
^^^^^^^

The PE ChIP-seq pipeline maps the raw reads to the genome (``-g``) using BWA mem. Raw mapped reads are labeled as ``.markdup.bam``. De-duplicated reads are labeled as ``.rmdup.bam``. De-duplicated and uniquely mapped reads are labeled as ``.rmdup.uq.bam``. Duplicated and multi-mapped reads were removed using samtools (v0.17). ChIP-seq peaks were called using MACS2 (v2.1.1) with “-f BAMPE”. BigWiggle files were generated using DeepTools bamCoverage (v3.2.0) with "--centerReads". 

Code for this pipeline is provided in "https://github.com/YichaoOU/HemTools/blob/master/subcmd/". See ``chip_seq_pair.py`` and ``utils.py``.


Parameters
^^^^^^^^^^

.. argparse::
   :filename: ../bin/HemTools
   :func: main_parser
   :prog: HemTools
   :path: chip_seq_pair


Usage
^^^^^

Go to your data directory and type the following.

**Step 0: Load python version 2.7.13.**

.. code:: bash

    $ module load python/2.7.13

**Step 1: Prepare input files, generate fastq.tsv.**

.. code:: bash

    $ HemTools chip_seq_pair --guess_input

	Input fastq files preparation complete! ALL GOOD!
	Please check if you like the computer-generated labels in : fastq.tsv
	Input peakcall file preparation complete! File name: peakcall.tsv

.. note:: If you are preparing fastq.tsv and peakcall.tsv yourself, please make sure ``no space anywhere`` in the file. Note that the seperator is tab. Spaces in file name will cause errors.

**Step 2: Check the computer-generated input list (manually), make sure they are correct.**

.. code:: bash

    $ less fastq.tsv

    $ less peakcall.tsv

.. note:: a random string will be added to the generated files (e.g., fastq.94c049cbff1f.tsv) if they exist before running step 1.

**Step 3: Submit your job.**

.. code:: bash

    $ HemTools chip_seq_pair -f fastq.tsv -d peakcall.tsv

Sample input format
^^^^^^^^^^^^^^^^^^^

**fastq.tsv**

This is a tab-seperated-value format file. The 3 columns are: Read 1, Read 2, sample ID.

.. image:: ../../images/fastq.tsv.png

**peakcall.tsv**

This is also a tab-seperated-value format file. The 3 columns are: treatment sample ID, control/input sample ID, peakcall ID.

.. image:: ../../images/peakcall.tsv.png

Quality Control
^^^^^^^^^^^^^^^

The quality metrics are provided in the html report. For ChIP-seq data, we also provide strand cross-correlation metrics (i.e., those attached pdf files). 


+---------+-----------+
| Metrics | Threshold |
+---------+-----------+
| NRF     | >0.9      |
+---------+-----------+
| PBC1    | >0.9      |
+---------+-----------+
| PBC2    | >10       |
+---------+-----------+
| RSC     | >0.8      |
+---------+-----------+
| QTag    | >=1       |
+---------+-----------+


https://www.encodeproject.org/atac-seq/

https://www.encodeproject.org/chip-seq/transcription_factor/
https://www.encodeproject.org/chip-seq/histone/

https://github.com/crazyhottommy/ChIP-seq-analysis/blob/master/part0_quality_control.md




Report bug
^^^^^^^^^^

Once the job is finished, you will be notified by email with some attachments.  If no attachment can be found, it might be caused by an error. In such case, please go to the result directory (where the log_files folder is located) and type: 

.. code:: bash

    $ HemTools report_bug


Use different genome index
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    $ HemTools chip_seq_pair -f fastq.tsv -d peakcall.tsv -i YOUR_GENOME_INDEX



Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines






