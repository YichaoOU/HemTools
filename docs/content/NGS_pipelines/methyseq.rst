DNA methylation (Bisulfite-Sequencing) analysis pipeline using nf-core 
===================


::

	usage: methylseq.py [-h] [-j JID] -f INPUT [-q QUEUE] -fa FASTA

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        Methyl_seq_yli11_2022-08-11)
	  -f INPUT, --input INPUT
	                        fastq_tsv (default: None)
	  -q QUEUE, --queue QUEUE
	                        submit queue (default: standard)
	  -fa FASTA, --fasta FASTA
	                        only map to a small region (default: None)




Summary
^^^^^^^

bwa-meth mapping + MethylDackel calling

See https://nf-co.re/methylseq/1.6.1/parameters


Input
^^^^^

Copy paired-end fastq files to a working dir


Usage
^^^^^

This example only uses chr11 sequence for faster computation.

::

	hpcf_interactive

	# cd to your workng dir

	module load python/2.7.13

	run_lsf.py --guess_input

	methylseq.py -f fastq.tsv -fa /home/yli11/test/chr11.fa

You will see the following message indicating the job is submitted.
::

	2022-08-11 15:42:03,451 - INFO - main - The job id is: Methyl_seq_yli11_2022-08-11
	Job <166956652> is submitted to queue <standard>.
	Job <166956653> is submitted to queue <standard>.
	Job <166956654> is submitted to queue <standard>.
	Job <166956656> is submitted to queue <standard>.
	Job <166956657> is submitted to queue <standard>.



Output
^^^^^^

In the jobID folder ``Methyl_seq_yli11_2022-08-11``, you will find results for each sample. The coverage track (``.bedGraph`` file) is inside ``MethylDackel`` folder.

