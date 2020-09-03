MinION Nanopore for sequence assembly and read mapping
=================================


::

	usage: MinION_mapping.py [-h] [-j JID] -o OUTPUT_LABEL -fa REF_FA -fq
	                         FASTQ_FILE
	                         [--ngmlr_addon_parameters NGMLR_ADDON_PARAMETERS]
	                         [--wtdbg2_addon_parameters WTDBG2_ADDON_PARAMETERS]
	                         [--wtpoa_cns_addon_parameters WTPOA_CNS_ADDON_PARAMETERS]
	                         [-m MEM] [-k KMER] [-s GENOME_SIZE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        MinION_mapping_yli11_2020-09-02)
	  -o OUTPUT_LABEL, --output_label OUTPUT_LABEL
	                        output_label (default: None)
	  -fa REF_FA, --ref_fa REF_FA
	                        reference fa (default: None)
	  -fq FASTQ_FILE, --fastq_file FASTQ_FILE
	                        MinION fastq file (default: None)
	  --ngmlr_addon_parameters NGMLR_ADDON_PARAMETERS
	                        MinION fastq file (default: None)
	  --wtdbg2_addon_parameters WTDBG2_ADDON_PARAMETERS
	                        MinION fastq file (default: None)
	  --wtpoa_cns_addon_parameters WTPOA_CNS_ADDON_PARAMETERS
	                        MinION fastq file (default: None)
	  -m MEM, --mem MEM     required mem in MB (default: 15000)
	  -k KMER, --kmer KMER  kmer size (default: 13)
	  -s GENOME_SIZE, --genome_size GENOME_SIZE
	                        Approximate genome size (k/m/g suffix allowed)
	                        (default: 0)




Summary
^^^^^

This pipeline performs sequence assembly using ``wtdbg2`` as well as read mapping using ``ngmlr``

If no ``-fa`` is specified, only sequence assembly will be performed.

https://github.com/ruanjue/wtdbg2

https://github.com/philres/ngmlr



Input
^^^^^

1. Fastq file from Nanopore ``-fq``

2. Output label ``-o``

3. Optional, a reference fasta sequence to perform read alignment ``-fa``

Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	MinION_mapping.py -fa Townes_build2.fa -fq all.fq.gz -o test


Output
^^^^^

Results are provided in the jid folder.

``*.ctg.fa`` assembled contig.

``*.fix.st.bam`` read mapping bam file.


Comments
^^^^^^^^

.. disqus::
	:disqus_identifier: NGS_pipelines




