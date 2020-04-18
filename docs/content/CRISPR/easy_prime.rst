Easy-Prime: pegRNA design
==================

::

	usage: easy_prime.py [-h] [-j JID] -f INPUT [--PAM_seq PAM_SEQ] [-e EXTEND]
	                     [-l SGRNA_LENGTH] [-o OUTPUT] [-g GENOME]
	                     [--genome_fasta GENOME_FASTA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        easy_prime_yli11_2020-04-17)
	  -f INPUT, --input INPUT
	                        a list of variants 5 columns chr, pos, name, ref, alt
	                        (default: None)
	  --PAM_seq PAM_SEQ     specify the PAM sequence, e.g., NGG. (default: NGG)
	  -e EXTEND, --extend EXTEND
	                        Define a region to look for gRNAs, extend search area
	                        to left and right (default: 200)
	  -l SGRNA_LENGTH, --sgRNA_length SGRNA_LENGTH
	                        sgRNA_length (default: 20)
	  -o OUTPUT, --output OUTPUT
	                        output file name (default: yli11_2020-04-17)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. currently, only
	                        hg19 is available (default: hg19)
	  --genome_fasta GENOME_FASTA
	                        genome version: hs, mm (default:
	                        /home/yli11/Data/Human/hg19/fasta/hg19.fa)


Summary
^^^^^


This tool can help you design pegRNAs given a list of variants (vcf format) 


https://github.com/YichaoOU/easy_prime

Method
^^^^^

.. only:: html

   .. figure:: ../../images/easy_prime_method.gif



Input
^^^^^

::

	chr11	5248232	HBB	A	T
	chr15	72638920	HEXA	G	GGATA


Usage
^^^^^

::

	hpcf_interactive

	easy_prime.py -f input.vcf 

Output
^^^^^

Inside the {{jobID}} folder.



Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines









