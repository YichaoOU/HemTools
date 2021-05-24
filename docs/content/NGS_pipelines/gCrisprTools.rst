gCrisprTools: Genome-wide CRISPR Screening
============================

::

	usage: crispr_seq.py [-h] [-j JID] [--interative] [-d DESIGN_MATRIX]
	                     [-l GRNA_LIBRARY] [-c CONTROL_GRNA_GROUP]
	                     [--min_read_count MIN_READ_COUNT] [-b BED]
	                     (-f FASTQ_TSV | --guess_input) [-g GENOME]

	analysis of crispr gRNA deep sequencing data

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        crispr_seq_yli11_2020-06-04)
	  --interative          run pipeline interatively (default: False)
	  -d DESIGN_MATRIX, --design_matrix DESIGN_MATRIX
	                        (Required) tsv 3 columns: group 1 , group 2,
	                        comparison name. The second group is used as control.
	                        (default: None)
	  -l GRNA_LIBRARY, --gRNA_library GRNA_LIBRARY
	                        (Required) 3 columns csv, with header: id,seq,gene
	                        (default: None)
	  -c CONTROL_GRNA_GROUP, --control_gRNA_group CONTROL_GRNA_GROUP
	                        (Required) mageck format (default: None)
	  --min_read_count MIN_READ_COUNT
	                        filter sgRNAs using read count, sgRNAs with less than
	                        the given value will be filtered out (default: 10)
	  -b BED, --bed BED     Genomic coordinates for gRNAs (Format: chr, start,
	                        end, name). If provided, raw counts, logFC, logFDR
	                        will be uploaded to protein paint for visualization.
	                        (default: None)
	  -f FASTQ_TSV, --fastq_tsv FASTQ_TSV
	                        tab delimited 3 columns (tsv file): Read 1 fastq,
	                        Sample ID, group ID (default: None)
	  --guess_input         Let the program generate the fastq.tsv and design.tsv
	                        files for you. (default: False)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)

Summary
^^^^^^

sgRNA were counted using ``Mageck``, then the significance of gRNA enrichment or depletion is evaluated using ``gCrisprTool``


Usage
^^^^^

Go to your data directory and type the following.

**Step 0: Load python version 2.7.13.**

.. code:: bash

    module load python/2.7.13

**Step 1: Prepare input files, generate fastq.tsv and design_matrix.tsv**

.. code:: bash

    crispr_seq.py --guess_input

.. note:: pairwise comparison is specified in design_matrix.tsv, please make sure these computer generated files are correct.

**Step 2: Submit your job.**

You have to prepare a gRNA library file, see the next section for more details.

.. code:: bash

    crispr_seq.py -f fastq.tsv -d design_matrix.tsv -l inhibation.gRNA.csv -c NON-TARGETING --interative


Input file
^^^^^^^^^^

fastq.tsv & design_matrix.tsv
-------

::


	==> design_matrix.tsv <==
	REP_DIFF_D5_BAND3HIGH	REP_DIFF_D5_BAND3LOW	REP_DIFF_D5_BAND3HIGH.vs.REP_DIFF_D5_BAND3LOW
	REP_DIFF_D5_BAND3HIGH	REP_DIFF_D3_BAND3LOW	REP_DIFF_D5_BAND3HIGH.vs.REP_DIFF_D3_BAND3LOW
	REP_DIFF_D5_BAND3HIGH	REP_DIFF_D3_BAND3HIGH	REP_DIFF_D5_BAND3HIGH.vs.REP_DIFF_D3_BAND3HIGH
	REP_DIFF_D5_BAND3HIGH	REP_D2_EXP	REP_DIFF_D5_BAND3HIGH.vs.REP_D2_EXP
	REP_DIFF_D5_BAND3HIGH	REP_D8_EXP	REP_DIFF_D5_BAND3HIGH.vs.REP_D8_EXP
	REP_DIFF_D5_BAND3HIGH	REP_D0_EXP	REP_DIFF_D5_BAND3HIGH.vs.REP_D0_EXP
	REP_DIFF_D5_BAND3HIGH	REP_D5_EXP	REP_DIFF_D5_BAND3HIGH.vs.REP_D5_EXP
	REP_DIFF_D5_BAND3LOW	REP_DIFF_D3_BAND3LOW	REP_DIFF_D5_BAND3LOW.vs.REP_DIFF_D3_BAND3LOW
	REP_DIFF_D5_BAND3LOW	REP_DIFF_D3_BAND3HIGH	REP_DIFF_D5_BAND3LOW.vs.REP_DIFF_D3_BAND3HIGH
	REP_DIFF_D5_BAND3LOW	REP_D2_EXP	REP_DIFF_D5_BAND3LOW.vs.REP_D2_EXP

	==> fastq.tsv <==
	REP_DIFF_D5_BAND3HIGH_R3_C7.fastq.gz	REP_DIFF_D5_BAND3HIGH_R3_C7	REP_DIFF_D5_BAND3HIGH
	REP_DIFF_D5_BAND3LOW_R3_C11.fastq.gz	REP_DIFF_D5_BAND3LOW_R3_C11	REP_DIFF_D5_BAND3LOW
	REP_DIFF_D3_BAND3LOW_R1_B9.fastq.gz	REP_DIFF_D3_BAND3LOW_R1_B9	REP_DIFF_D3_BAND3LOW
	REP_DIFF_D5_BAND3LOW_R2_C10.fastq.gz	REP_DIFF_D5_BAND3LOW_R2_C10	REP_DIFF_D5_BAND3LOW
	REP_DIFF_D5_BAND3LOW_R1_C9.fastq.gz	REP_DIFF_D5_BAND3LOW_R1_C9	REP_DIFF_D5_BAND3LOW
	REP_DIFF_D3_BAND3HIGH_R3_B7.fastq.gz	REP_DIFF_D3_BAND3HIGH_R3_B7	REP_DIFF_D3_BAND3HIGH
	REP_DIFF_D3_BAND3LOW_R3_B11.fastq.gz	REP_DIFF_D3_BAND3LOW_R3_B11	REP_DIFF_D3_BAND3LOW
	REP_DIFF_D3_BAND3HIGH_R4_B8.fastq.gz	REP_DIFF_D3_BAND3HIGH_R4_B8	REP_DIFF_D3_BAND3HIGH
	REP_DIFF_D3_BAND3HIGH_R1_B5.fastq.gz	REP_DIFF_D3_BAND3HIGH_R1_B5	REP_DIFF_D3_BAND3HIGH
	REP_DIFF_D3_BAND3HIGH_R2_B6.fastq.gz	REP_DIFF_D3_BAND3HIGH_R2_B6	REP_DIFF_D3_BAND3HIGH


gRNA library file
--------------

gRNA library csv file (--gRNA_library option, required)

This file specifies your gRNA library. It is a csv file where the columns are sgRNA id, sgRNA sequence, and the targeted gene. An example file is shown below.

.. code:: bash

	id,seq,Gene
	chr11:4167629-AAATTTCCTCAGCAGATTAC,AAATTTCCTCAGCAGATTAC,Gene1
	Please_no_space_anywhere,ACAAGCAACAGTTGACCAAC,Gene1
	could_be_anything,ACATGAGACTGGAAACCGCC,control


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines




















