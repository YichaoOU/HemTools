Genome-wide CRISPR Screening
============================


.. argparse::
   :filename: ../bin/HemTools
   :func: main_parser
   :prog: HemTools
   :path: crispr_seq

Input file
^^^^^^^^^^

0. fastq files.

`No options to input a list of fastq files`. All *.fastq.gz files in the current directory will be used.

In you don't want to use all fastq files, please create a new directory, cd to that directory, and create soft links for the files you need. A soft link is similar to file shortcut used in Windows.

The command to create a sotf link is:

.. code:: bash

    $ ln -s [original filename] [link name]

1. Design matrix (-d option, required).

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


.. tip:: Comparison name should be unique. Control & treatment in the 2nd column are keywords, misspelling can cause error. 

2. gRNA library csv file (--gRNA_library option, required).

This file specifies your gRNA library. It is a csv file where the columns are sgRNA, sgRNA sequence, and the targeted gene. An example file is shown below.

.. code:: bash

	sgRNA,Sequence,Gene
	chr11:4167629-AAATTTCCTCAGCAGATTAC,AAATTTCCTCAGCAGATTAC,Gene1
	Please_no_space_anywhere,ACAAGCAACAGTTGACCAAC,Gene1
	could_be_anything,ACATGAGACTGGAAACCGCC,positive_control

3. control gRNA list (--control_gRNAs option, optional).

The file specifies a list of control gRNA names. The names should match to the gRNA library file. Each line is a control gRNA name.

.. tip:: control gRNAs are optional. If provided, normalization will be performed based on these controls, instead of median normalization.

4. Genomic coordinate bed file of gRNA (--bed option, optional).

Genomic coordinates for gRNAs (Format: chr, start, end, name). If provided, raw counts, logFC, logFDR will be uploaded to protein paint for visualization. An example file is shown below.

.. code:: bash
	chr11	4167629	4167649	sgRNA1_gene1

.. tip:: gRNAs locations are optional. If provided, raw counts, logFC, logFDR will be uploaded to protein paint for visualization.

Usage
^^^^^

Go to your data directory and type the following.

Step 0: Load python version 2.7.13.

.. code:: bash

    $ module load python/2.7.13

Step 1: Prepare the input files, see the format above. 

Step 3: Submit your job.

.. code:: bash

    $ HemTools crispr_seq -d design_matrix.tsv --gRNA_library my_gRNAs.csv

OR:

.. code:: bash

    $ HemTools crispr_seq -d design_matrix.tsv --gRNA_library my_gRNAs.csv --control_gRNAs my_controls.list --bed my_gRNAs.bed


Report bug
^^^^^^^^^^

Once the job is finished, you will be notified by email with some attachments.  If no attachment can be found, it might be caused by an error. In such case, please go to the result directory (where the log_files folder is located) and type: 

.. code:: bash

    $ HemTools report_bug


TODO
^^^^

The HPC doesn't have the latest version of Mageck. A request has been submitted.






















