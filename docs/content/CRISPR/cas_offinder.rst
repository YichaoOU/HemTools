Find number of off-targets
==========================


::

	usage: cas_offinder.py [-h] [-j JID] -f INPUT [-n NUM_MISMATCHES] [--add_PAM]
	                       [--PAM_seq PAM_SEQ] [-g GENOME] [--chr_fa CHR_FA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        cas_offinder_yli11_2019-07-17)
	  -f INPUT, --input INPUT
	                        a list of gRNA sequences (default: None)
	  -n NUM_MISMATCHES, --num_mismatches NUM_MISMATCHES
	                        Number of allowed mis-matches in the gRNA, excluding
	                        PAM sequence (default: 2)
	  --add_PAM             if PAM sequence is not included in your gRNA, please
	                        add this option. (default: False)
	  --PAM_seq PAM_SEQ     specify the PAM sequence, e.g., NGG. (default: NGG)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. currently, only
	                        hg19 is available (default: hg19)
	  --chr_fa CHR_FA       This will be automatically changed with -g option
	                        (default: /home/yli11/Data/Human/hg19/fasta/chr)

Summary
^^^^^^^

Given a list of gRNA sequences and number of allowed mismatches (excluding PAM), with or without PAM sequences, output number of off-targets (i.e., number of matches up to maximal mismatches) for each gRNA.


Output example
^^^^^^^^^^^^^^

::

	ACTGGGAGACACCTCCCAGTAGG	4058
	TGGGAGACACCTCCCAGTAGGGG	4011
	CTGGGAGACACCTCCCAGTAGGG	3998
	AGGTGTCTGTCGGCCCCTACTGG	3262
	GGTGTCTGTCGGCCCCTACTGGG	3208
	TCAGGAATTCGAGACCAGCAGGG	3146
	GTCTGTCGGCCCCTACTGGGAGG	1687
	CAGGAATTCGAGACCAGCAGGGG	919
	CTCTCTCCTTGGCCTGCAGATGG	832
	GTCAGGAATTCGAGACCAGCAGG	509	


Input
^^^^^

A list of gRNAs:

::

	ACGACCTTGGCGCCACCACCTGG
	TTATCTTTAACACCCCCTGCTGG
	AGCTCTCGCACCGCCACTAGAGG
	TTACAGGAGAGACCAGATGATGG
	CACCGGTGGAATCCAGTAGGGGG
	AGTGAGAGGAGGTGCCAGCAGGG
	AGCCAGGTGCCGCCCTCCTGAGG
	TGGGGGCCTGGGTGTCCACCAGG
	GAGCCTTCAGCTACCTCATGTGG
	TAGCAGCTGGGAACCAGCAGAGG

.. note:: if no PAM sequences in the gRNA input, please add ``--add_PAM`` option.


Usage
^^^^^

**Step 0: Load python version 2.7.13.**

.. code:: bash

    module load python/2.7.13

**Step 1: Run the command**

Example command 1: with ``--add_PAM`` option.

.. code:: bash

	cas_offinder.py -f gRNA.list2 --add_PAM 

	2019-07-17 11:09:04,293 - INFO - main - The job id is: cas_offinder_yli11_2019-07-17
	2019-07-17 11:09:04,649 - INFO - submit_pipeline_jobs - cas has been submitted; JobID: 83786440

Example command 2: if input gRNA sequences contain PAM, then just run the following command.

.. code:: bash

	cas_offinder.py -f gRNA.list 

	2019-07-17 11:09:24,777 - WARNING - main - The input job id is not available!
	2019-07-17 11:09:24,777 - INFO - main - The new job id is: cas_offinder_yli11_2019-07-17_f0811dd87951
	2019-07-17 11:09:24,890 - INFO - submit_pipeline_jobs - cas has been submitted; JobID: 83786441

.. note:: By default, maximal allowed mismatches is 2. You can control this by ``-n`` option.

Output
^^^^^^

Once the job is finished, you will receive a notification email with the result attached.


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



























