Genome-wide CRISPR Screening
============================


.. argparse::
   :filename: ../bin/HemTools
   :func: main_parser
   :prog: HemTools
   :path: crispr_seq

Input file
^^^^^^^^^^

**INPUT 0. fastq files.**

``No options to input a list of fastq files``. All *.fastq.gz files in the current directory will be used.

Inf you don't want to use all fastq files, please create a new directory, cd to that directory, and create soft links for the files you need. A soft link is similar to file shortcut used in Windows.

The command to create a soft link is:

.. code:: bash

    $ ln -s [original filename] [link name]

**INPUT 1. Design matrix (-d option, required).**

This file specifies a list of pairwise comparisons. Each comparison has a comparison name, a list of control group files, and a list of treatment group files. The format is a 3-column tsv file. An example file is shown below.

.. code:: bash
	
	APC	control	CRM-APC-Negative-rep1_S10_L001_R1_001.fastq.gz,CRM-APC-Negative-rep2_S11_L001_R1_001.fastq.gz
	APC	treatment	CRM-APC-positive-rep1_S4_L001_R1_001.fastq.gz,CRM-APC-positive-rep2_S5_L001_R1_001.fastq.gz
	GFP	control	CRM-GFP-Negative-rep1_S7_L001_R1_001.fastq.gz,CRM-GFP-Negative-rep2_S8_L001_R1_001.fastq.gz
	GFP	treatment	CRM-GFP-Positive-rep1_S1_L001_R1_001.fastq.gz,CRM-GFP-Positive-rep2_S2_L001_R1_001.fastq.gz
	APC_neg_vs_plasmid	control plasmid.fastq.gz
	APC_neg_vs_plasmid	treatment CRM-APC-Negative-rep1_S10_L001_R1_001.fastq.gz,CRM-APC-Negative-rep2_S11_L001_R1_001.fastq.gz
	APC_pos_vs_plasmid	control plasmid.fastq.gz
	APC_pos_vs_plasmid	treatment CRM-APC-positive-rep1_S4_L001_R1_001.fastq.gz,CRM-APC-positive-rep2_S5_L001_R1_001.fastq.gz


.. note:: Comparison names (column 1) should be unique. ``control`` & ``treatment`` (column 2) are keywords, misspelling can cause error. 

**INPUT 2. gRNA library csv file (--gRNA_library option, required).**

This file specifies your gRNA library. It is a csv file where the columns are sgRNA, sgRNA sequence, and the targeted gene. This file must end with .csv. An example file is shown below.

.. code:: bash

	sgRNA,Sequence,Gene
	chr11:4167629-AAATTTCCTCAGCAGATTAC,AAATTTCCTCAGCAGATTAC,Gene1
	Please_no_space_anywhere,ACAAGCAACAGTTGACCAAC,Gene1
	could_be_anything,ACATGAGACTGGAAACCGCC,positive_control

**INPUT 3. control gRNA list (--control_gRNAs option, optional).**

The file specifies a list of control gRNA names. The names should match to the gRNA library file. Each line is a control gRNA name.

.. tip:: control gRNAs are optional. If provided, normalization will be performed based on these controls, instead of median normalization.

**INPUT 4. Genomic coordinate bed file of gRNA (--bed option, optional).**

Genomic coordinates for gRNAs (at least 4 columns: format: chr, start, end, name). If provided, raw counts, logFC, logFDR will be uploaded to protein paint for visualization. An example file is shown below. The last column name should be either gRNA id (i.e., the 1st column in the gRNA lib file.)

.. code:: bash

	chr11	4167629	4167649	sgRNA1_id

.. tip:: gRNAs locations are optional. If provided, raw counts, logFC, logFDR will be uploaded to protein paint for visualization. gRNA strand info is not required.

Usage
^^^^^

Go to your data directory and type the following.

**Step 0: Load python version 2.7.13.**

.. code:: bash

    $ module load python/2.7.13

**Step 1: Prepare the input files, see the format above. **

.. note:: Please make sure there is ``no space anywhere`` in file name, sgRNA names, and gene names. 

**Step 2: Submit your job.**

.. code:: bash

    $ HemTools crispr_seq -d design_matrix.tsv --gRNA_library my_gRNAs.csv --control_gRNAs my_controls.list

OR:

.. code:: bash

    $ HemTools crispr_seq -d design_matrix.tsv --gRNA_library my_gRNAs.csv --control_gRNAs my_controls.list --bed my_gRNAs.bed

OR you can perform MaGeCK RRA paired test by add ``--paired`` option:

.. note:: Paired test is only available for MaGeCK RRA method, not available for the MLE method.

.. note:: In paired mode, the number of control samples must be the same as the number of treatment samples.

.. code:: bash

    $ HemTools crispr_seq -d design_matrix.tsv --gRNA_library my_gRNAs.csv --control_gRNAs my_controls.list --bed my_gRNAs.bed --paired



Increase mapping rate
-------------------

If you have different length of gRNAs in your library, automatic determination may decrease the gRNA mapping rate. In these cases, you may want to fix the gRNA search positions, such as ``--trim_5 40,41,42,43,44,45,46``

trim position depends on your library preparation. In Cheng lab, it is mostly at 43.

The complete command is:


.. code:: bash

    $ HemTools crispr_seq -d design_matrix.tsv --gRNA_library my_gRNAs.csv --control_gRNAs my_controls.list --bed my_gRNAs.bed --trim_5 40,41,42,43,44,45,46


Output files
^^^^^^^^^^^^

QC
---

In the email attachment, you can find Mageck count report, example shown below.

.. image:: ../../images/count_report.png
	:align: center

Here you can check mapping rate, number of sgRNAs with zero count, and gini index for eveness (<0.2 is good).



Report bug
^^^^^^^^^^

Once the job is finished, you will be notified by email with some attachments.  If no attachment can be found, it might be caused by an error. In such case, please go to the result directory (where the log_files folder is located) and type: 

.. code:: bash

    $ HemTools report_bug


TODO
^^^^

HPC doesn't have the latest version of Mageck. A request has been submitted.


For the insulator project
^^^^^^^

add ``--kallisto`` option to use kallisto to map R1 read to 250bp fasta library and count reads, generates Mageck format count table so that we can use Mageck to gengerate visualizations and comparisons.


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines




















