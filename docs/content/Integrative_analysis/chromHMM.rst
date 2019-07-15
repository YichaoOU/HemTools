Chromatin State Discovery
=========================


::



Summary
^^^^^^^

Perform chromatin state discovery given a list of fastq files. Single-end fastq is given using ``-se`` option. Paired-end fastq is given using ``-pe`` option. These input files are similar to ``fastq.tsv``, as used in other HemTools programs. One can use either one or both input types. Design matrix is given as ``-d1`` or ``-d2`` options. ``-d1`` input format is similar to ``peakcall.tsv``, where the first two columns are UIDs (treatment vs control), and the third column is a label. This label has to be a meanfully label, such as H3K4me3 (Case insensitive). These labels are used to compare to known chromHMM annotations (see the second figure below). Still, chromatin state annotations are subjective, there's no ground rules, this comparison is just to help you define the learned model.

.. note:: In theory, you can input any fastq data, such as RNA-seq, Hi-C, or TF CHIP-seq data. However, I haven't seen papers using RNA-seq or Hi-C for chromatin state discovery. There are few papers using Pol-II, CTCF, or NANOG. You can definitely try everything.


Flowchart
^^^^^^^^^


Chromatin states known associations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: ../../images/chromatin_states_known_associations.png
	:align: center


Input
^^^^^

See ``Summary`` above for how these inputs are used.

**-se: similar to fastq.tsv for single-end data**

2 columns: file_location (with path if not in the current dir), UID.

**-pe: similar to fastq.tsv for paired-end data**

3 columns: file_location for R1.fastq.gz, file_location for R2.fastq.gz, UID.

**-d1: similar to peakcall.tsv for chip-seq data**

For ChIP-seq data, usually you have an input control. For that, you want to use ``-d1``. 

Here, you want to compare everything to control, which could be input chip or IgG.

3 columns: UID, UID, label. 

**-d2: give your input files a label**

For ATAC-seq data, you don't have control. Then, use ``-d2``.

Here, you want to state the label for your input files.

2 columns: UID, label. 


Usage
^^^^^

Go to your data directory and type the following.

**Step 0: Load python version 2.7.13.**

.. code:: bash

    module load python/2.7.13

**Step 1: Prepare input parameters**

.. code:: bash

    chromHMM.py -pe PE_list -d1 design_matrix_1 -d2 design_matrix_2 -n 4 --d1_bin_bam_addon " -paired" --d2_bin_bam_addon " -paired"


Output
^^^^^^

Once the job is finished, you will receive a notification email. 

``learned_states`` contains the chromatin state discovery results, look at ``webpage_{{number_states}}.html`` file.


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines




















