Crispresso2 for Base editor
==========================


::

	usage: crispresso2_BE.py [-h] [-j JID] [-f INPUT_LIST]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        crispresso2_BE_yli11_2019-08-12)
	  -f INPUT_LIST, --input_list INPUT_LIST
	                        tsv 5 columns, R1.fastq, R2.fastq, amplicon_seq,
	                        gRNA_seq, output_name (default: None)


Summary
^^^^^^^

Running crispresso2 for base editor mode: https://github.com/pinellolab/CRISPResso2

The command is:

::
	CRISPResso -r1 ${COL1} 
		 -r2 ${COL2} 
		 --amplicon_seq ${COL3} 
		 --guide_seq ${COL4} 
		 --quantification_window_size 10 
		 --quantification_window_center -10
		 --base_editor_output -o {{jid}}/${COL5}

Input
^^^^^

A 5-column tsv file: R1.fastq, R2.fastq, amplicon_seq,  gRNA_seq, output_name

::

	12_S12_L001_R1_001.fastq.gz	12_S12_L001_R2_001.fastq.gz	Amplicon_seq	cttgaccaatagccttgaca	test1
	XXXX_L001_R1_001.fastq.gz	XXXX_L001_R2_001.fastq.gz	Amplicon_seq	cttgaccaatagccttgaca	Bababa

Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	crispresso2_BE.py -f input.list


Output
^^^^^^

Once the job is finished, you will receive a notification email with the result attached. Unzip the file and open the HTML file.


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



























