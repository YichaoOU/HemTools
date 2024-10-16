Analysis of Hi-C or HiChIP data
==========================

This pipeline is out-dated for HiC analysis, please use ``hicpro_batch.py`` instead.


::

	usage: hic_hichip.py [-h] [-j JID] [--hicpro] [--hicpro_config HICPRO_CONFIG]
	                     [--hichipper_config HICHIPPER_CONFIG]
	                     [--MAPS_config MAPS_CONFIG] [-a ANCHOR]
	                     (-f FASTQ_TSV | --guess_input) [-g GENOME]
	                     [-i INDEX_FILE] [-s CHROM_SIZE]
	                     [--genomic_feat_filepath GENOMIC_FEAT_FILEPATH]
	                     [-e DIGESTED_ENZYME] [--chr_count CHR_COUNT]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        hic_hichip_yli11_2019-08-27)
	  --hicpro              only run hicpro (default: False)
	  --hicpro_config HICPRO_CONFIG
	  --hichipper_config HICHIPPER_CONFIG
	  --MAPS_config MAPS_CONFIG
	  -a ANCHOR, --anchor ANCHOR
	                        anchor list to search for interactions, if given, MAPS
	                        will be run as well (default: None)
	  -f FASTQ_TSV, --fastq_tsv FASTQ_TSV
	                        tab delimited 3 columns (tsv file): Read 1 fastq, Read
	                        2 fastq, sample ID (default: None)
	  --guess_input         Let the program generate the input files for you.
	                        (default: False)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -i INDEX_FILE, --index_file INDEX_FILE
	                        bowtie2 index file (default:
	                        /home/yli11/Data/Human/hg19/index/bowtie2_index)
	  -s CHROM_SIZE, --chrom_size CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Human/hg19/anno
	                        tations/hg19.chrom.sizes)
	  --genomic_feat_filepath GENOMIC_FEAT_FILEPATH
	                        MAPS genomic_feat_filepath (default: /home/yli11/HemTo
	                        ols/share/misc/MAPS/MAPS_data_files/hg19/genomic_featu
	                        res/F_GC_M_MboI_10Kb_el.hg19.txt)
	  -e DIGESTED_ENZYME, --digested_enzyme DIGESTED_ENZYME
	                        digested_fragments hg19_MboI (default: MboI)
	  --chr_count CHR_COUNT
	                        chr_count (default: 22)


Summary
^^^^^^^

This program provides Hi-C or HiChIP data analysis. Currently, this program only works on hg19. Digestive enzyme can be Mbo1 or HindIII.

HiC uses ``HiCPro``

HiChIP uses ``HiCPro+Hichipper`` and ``MAPS``

FitHiC results added after HiCPro, results locate at ``hic_results/matrix``

Usage
^^^^^

Go to your fastq files folder and do the following:

.. code:: bash
	
	hpcf_interactive

	module load python/2.7.13

	hic_hichip.py --guess_input

You will get the following message if everything goes as expected.

::

	2019-08-27 17:49:37,043 - INFO - main - preparing input files
	2019-08-27 17:49:37,044 - INFO - prepare_paired_end_input - Input fastq files preparation complete! ALL GOOD!
	2019-08-27 17:49:37,044 - INFO - prepare_paired_end_input - Please check if you like the computer-generated labels in : fastq.tsv


**run HiC analysis only**

.. code:: bash

	hic_hichip.py -f fastq.tsv --hicpro

**run HiChIP analysis (Hichipper only)**

.. code:: bash

	hic_hichip.py -f fastq.tsv

**run HiChIP analysis (Hichipper + MAPS)**

.. code:: bash

	hic_hichip.py -f fastq.tsv -a anchor.bed


Output
^^^^^^

Once finished, you will be notified by email. All generated bw files are located in the job ID folder.

Each line in the fastq.tsv file will have a result folder in the jobID folder.

In each result folder (named using the third column in your fastq.tsv), you will see:

HiC analysis result: hicpro_results

HiChIP anallysis (HiChipper): hichipper_results. See: https://hichipper.readthedocs.io/en/latest/content/Output.html?highlight=output for output description.

HiChIP anallysis (MAPS): MAPS_output, feather_output. (not updated, very likely to be failed)

QC report
^^^^^^^^^

Multi-QC HTML report
--------------------

You should be able to find ``multiqc_report.html`` in the hicpro_results folder.


.. image:: ../../images/hicpro-multiqc-report.png
	:align: center


HicPro QC figures
-----------------

They are in ``hicpro_results/hic_results/pic/``

There is a known bug that the labels in `plotMapping.pdf` are wrong: https://github.com/nservant/HiC-Pro/issues/290.


FAQ
^^^

Out of memory error
-------------------

We requested 160G memory, but it may not be enough. In case that your data is partly processed, you can continue from where it stopped using the following commands:


.. code:: bash

	cd /home/yli11/dirs/blood_regulome/chenggrp/Projects/tcells/HiC/HiC_2_3/hic_hichip_qqi_2020-02-24/Tcell_HiC_2_3/hicpro_results
	time HiC-Pro -c hicpro.config.txt -i bowtie_results/bwt2 -o . -s proc_hic
	time HiC-Pro -c hicpro.config.txt -i bowtie_results/bwt2 -o . -s quality_checks
	time HiC-Pro -c hicpro.config.txt -i hic_results/data/ -o . -s merge_persample
	time HiC-Pro -c hicpro.config.txt -i hic_results/data/ -o . -s build_contact_maps
	time HiC-Pro -c hicpro.config.txt -i hic_results/matrix/ -o . -s ice_norm
	source activate /home/yli11/.conda/envs/multiQC/
	export LC_ALL=en_US.utf-8
	export LANG=en_US.utf-8
	multiqc .






























