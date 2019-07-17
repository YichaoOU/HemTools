Detecting allele-specific effects on ChIP-seq or ATAC-seq
=========================================================

::

	usage: general_variant_calling.py [-h] [-j JID]
	                                  [--pipeline_type PIPELINE_TYPE]
	                                  [-d DEPTH_FILTER] -f BAM_LIST
	                                  [--mpileup_addon_parameters MPILEUP_ADDON_PARAMETERS]
	                                  [--help_dir HELP_DIR] [-g GENOME]
	                                  [--samtools_fa_index SAMTOOLS_FA_INDEX]

	General variant calling method using samtools mpileup, useful for ChIP-seq or
	ATAC-seq to find allele-specific binding or chromatin accessibility.

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        general_variant_calling_yli11_2019-07-17)
	  --pipeline_type PIPELINE_TYPE
	                        Not for end-user. (default: general_variant_calling)
	  -d DEPTH_FILTER, --depth_filter DEPTH_FILTER
	                        filter variants by raw read depth (this depth contains
	                        unfiltered reads) (default: 5)
	  -f BAM_LIST, --bam_list BAM_LIST
	                        tab delimited 2 columns (tsv file): path_to_bam_file,
	                        sample ID (default: None)
	  --mpileup_addon_parameters MPILEUP_ADDON_PARAMETERS
	                        if you have a specific region to search for, you can
	                        do -l path_to_bed (default: None)
	  --help_dir HELP_DIR   not for end-user (default:
	                        /home/yli11/HemTools/share/helper_scripts)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19. Only working for hg19 (default:
	                        hg19)
	  --samtools_fa_index SAMTOOLS_FA_INDEX
	                        samtools fa index (default:
	                        /home/yli11/Data/Human/hg19/fasta/samtools/hg19.fa)

Summary
^^^^^^^

This is a general variant calling pipeline using samtools mpileup, which could be applied, in theory, on any NGS data.

Currently, this pipeline only works on hg19. Additional reference data need to be generated for other genomes.

Input
^^^^^

**bam.list**

A tsv file with 2 columns: path to bam file and a sample ID.

::

	1659315_cell1_treat1_ATAC_S13_L001.rmdup.uq.bam	1659315_cell1_treat1
	1659316_cell1_control_ATAC_S14_L001.rmdup.uq.bam	1659316_cell1_control
	1659317_cell2_treat1_ATAC_S15_L001.rmdup.uq.bam	1659317_cell2_treat1
	1659318_cell2_control_ATAC_S16_L001.rmdup.uq.bam	1659318_cell2_control
	1659315_cell1_treat1_ATAC_S13_L002.rmdup.uq.bam	1659315_cell1_treat1_2
	1659316_cell1_control_ATAC_S14_L002.rmdup.uq.bam	1659316_cell1_control_2
	1659317_cell2_treat1_ATAC_S15_L002.rmdup.uq.bam	1659317_cell2_treat1_2
	1659318_cell2_control_ATAC_S16_L002.rmdup.uq.bam	1659318_cell2_control_2

Usage
^^^^^

.. code:: bash

    module load python/2.7.13

    general_variant_calling.py -f bam.list

If you only want to focus on a small region, you can prepare a bed file (3 columns) and supply it as additional parameters for samtools mpileup. For example:

.. code:: bash

    general_variant_calling.py -f bam.list --mpileup_addon_parameters " -l regions_for_genotyping/candidate.bed"


Output
^^^^^^

Once the job is finished, you will be notified by email.

``*.final.vcf`` contains the called variants. We calculated empirical allele frequency (EAF) and filtered read depth (FDP)using ``AD`` tag outputed by samtools.

``ppr_vis`` contains the tabix-ed vcf files that can be directly uploaded to Stjude PPR genome browser. 


Report bug
^^^^^^^^^^

.. code:: bash

    $ HemTools report_bug

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines








