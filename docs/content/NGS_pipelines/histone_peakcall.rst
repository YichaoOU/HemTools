Paired-end histone ChIP-seq or CUT&RUN
======================================

.. argparse::
   :filename: ../bin/HemTools
   :func: main_parser
   :prog: HemTools
   :path: cut_run_histone


Usage
^^^^^

Go to your data directory and type the following.

**Step 0: Load python version 2.7.13.**

.. code:: bash

    $ module load python/2.7.13

**Step 1: Prepare input files, generate fastq.tsv.**

.. code:: bash

    $ HemTools cut_run_histone --guess_input

	Input fastq files preparation complete! ALL GOOD!
	Please check if you like the computer-generated labels in : fastq.tsv
	Input peakcall file preparation complete! File name: peakcall.tsv

.. note:: If you are preparing fastq.tsv and peakcall.tsv yourself, please make sure ``no space anywhere`` in the file. Note that the seperator is tab. Spaces in file name will cause errors.

**Step 2: Check the computer-generated input list (manually), make sure they are correct.**

.. code:: bash

    $ less fastq.tsv

    $ less peakcall.tsv

.. note:: a random string will be added to the generated files (e.g., fastq.94c049cbff1f.tsv) if they exist before running step 1.

**Step 3a: (Narrow Peak) Submit your job.**

.. code:: bash

    $ HemTools cut_run_histone -f fastq.tsv -d peakcall.tsv

**Step 3b: (Broad Peak) Submit your job.**

.. code:: bash

    $ HemTools cut_run_histone -f fastq.tsv -d peakcall.tsv --broad    

.. tip:: If you have both narrow peak histone and broad peak histone data in your fastq.tsv, then the simplest way to run is just run step3a and step3b at the same time. Or you can write those file names in different file. I think I won't do that, I will just run the narrow peak and broad peak pipeline for the same data, and peak the correct result later.

Sample input format
^^^^^^^^^^^^^^^^^^^

**fastq.tsv**

This is a tab-seperated-value format file. The 3 columns are: Read 1, Read 2, sample ID.

.. image:: ../../images/fastq.tsv.png

**peakcall.tsv**

This is also a tab-seperated-value format file. The 3 columns are: treatment sample ID, control/input sample ID, peakcall ID.

.. image:: ../../images/peakcall.tsv.png


Report bug
^^^^^^^^^^

Once the job is finished, you will be notified by email with some attachments.  If no attachment can be found, it might be caused by an error. In such case, please go to the result directory (where the log_files folder is located) and type: 

.. code:: bash

    $ HemTools report_bug


Use different genome index
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    $ HemTools cut_run -f fastq.tsv -d peakcall.tsv -i YOUR_GENOME_INDEX



Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines












