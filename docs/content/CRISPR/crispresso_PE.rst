Crispresso2 for Prime Editor
==========================


::

	usage: crispresso2_PE.py [-h] [-j JID] [-s SCAFFOLD_SEQUENCE] -f PE_INPUT
	                         [-g GENOME] [--genome_fasta GENOME_FASTA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        crispresso2_PE_yli11_2020-09-05)
	  -s SCAFFOLD_SEQUENCE, --scaffold_sequence SCAFFOLD_SEQUENCE
	  -f PE_INPUT, --PE_input PE_INPUT
	                        input list (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  --genome_fasta GENOME_FASTA
	                        genome fasta file (default:
	                        /home/yli11/Data/Human/hg19/fasta/hg19.fa)




Summary
^^^^^^^

Running crispresso2 for prime editor mode: https://github.com/pinellolab/CRISPResso2

The command is:

.. code:: bash

	CRISPResso -r1 ${COL1} -r2 ${COL2} 
	--amplicon_seq $amplicon 
	--prime_editing_pegRNA_spacer_seq ${COL6} 
	--prime_editing_pegRNA_extension_seq ${COL7} 
	--prime_editing_nicking_guide_seq ${COL8} 
	--prime_editing_pegRNA_scaffold_seq {{scaffold_sequence}} 
	--write_cleaned_report 
	-o {{jid}}/${COL3} 


Input
^^^^^

A 8-column tsv file.

::

	Read1	Read2	Output_Name	Forward primer	Reverse primer	pegRNA spacer sequence	pegRNA extesion sequence	ngRNA sequence


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	crispresso2_PE.py -f input.list


Output
^^^^^^

Once the job is finished, you will receive a notification email. 


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines






















