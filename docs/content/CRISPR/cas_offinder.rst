Find number of off-targets
==========================


::

	usage: cas_offinder.py [-h] [-j JID] -f INPUT [-n NUM_MISMATCHES] [--add_PAM]
	                       [--remove_first_G] [--PAM_seq PAM_SEQ] [-g GENOME]
	                       [--chr_fa CHR_FA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        cas_offinder_yli11_2020-03-24)
	  -f INPUT, --input INPUT
	                        a list of gRNA sequences (default: None)
	  -n NUM_MISMATCHES, --num_mismatches NUM_MISMATCHES
	                        Number of allowed mis-matches in the gRNA, excluding
	                        PAM sequence (default: 2)
	  --add_PAM             if PAM sequence is not included in your gRNA, please
	                        add this option. (default: False)
	  --remove_first_G      remove first letter G in the input gRNA list (default:
	                        False)
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


Latest updates:

1. To allow mismatches in the PAM sequence, use ``--add_PAM --allow_PAM_mis --PAM_seq NGG``, for example:

::

	cas_offinder.py -f hg38 --add_PAM --allow_PAM_mis --PAM_seq NGG -f input2.list -j mis_4_GA -n 4

2. To allow G-A mismatch in the protospacer sequence, change G to R in the protospacer sequence:

for example ACTGGGAGACACCTCCCAGT becomes ACT``R````R````R``A``R``ACACCTCCCA``R``T



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

To find gRNA locations
----------

This program can also be helpful to find gRNA coordinates in the genome.

Now, my gRNA list doesn't have PAM and actually contains G in the beginning of every gRNA. my command will be:

.. code:: bash

	cas_offinder.py -f VPR.gRNA.list -n 0 --add_PAM --remove_first_G
	
	2020-03-24 14:49:45,002 - INFO - main - The job id is: cas_offinder_yli11_2020-03-24
	2020-03-24 14:49:45,154 - INFO - submit_pipeline_jobs - cas has been submitted; JobID: 99715775

Output
^^^^^^

Once the job is finished, you will receive a notification email with the result attached.

In the JobID folder:

match.bed cas-offinder otput bed file (not standard format) showing the matches

match.bed.sorted: sorted standard bed format that are ready to use.


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



























