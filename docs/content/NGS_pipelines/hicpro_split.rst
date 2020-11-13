Analysis of Hi-C and capture-C data using HiC-Pro
==========================

::

	usage: hicpro_batch.py [-h] [-j JID] [--queue QUEUE]
	                       (-f FASTQ_TSV | --guess_input) [-g GENOME]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        hicpro_batch_yli11_2020-06-26)
	  --queue QUEUE
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



Summary
^^^^^^^

This program provides Hi-C or Capture-C data analysis paired-end samples, split the fastq files and run HiC-Pro.

Total input reads is splited to 100M reads per file. So a 1.5B reads will generate 15 splited files, each will be submited to HPC. Mapping takes about 20 hours for 100M PE reads. Combining the reads and remove duplicates are much faster, about 3 hours. ice takes about 3 hours. hicpro2juicer takes about 50 hours. So together, you should have the results within a week.

Tested in hg38. hg19 should work. mm9 or mm10 will not work.

This program is updated for processing multiple fastq files. See old hicpro_split.py usage in the very bottom of this page.

Currently, ``hicpro_batch.py`` only support standard HiC analysis. ``hicpro_split.py`` provides options to keep duplicated and multi-mapped reads and capture-C data analysis.

Note: Homer has a problem converting working with ``--keep_dup`` option. Usually, we don't keep duplicates, we only did it for 20copy project.

For HiC data visualization, see: 

Usage
^^^^^

Go to your fastq files folder and do the following:

.. code:: bash
	
	hpcf_interactive

	module load python/2.7.13

	hicpro_batch.py --guess_input

	hicpro_batch.py -f fastq.tsv -g hg19


Output
^^^^^^

Same output as described in :doc:`hic_hichiper pipeline <hic_hichiper>`

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

hicpro_split.py
^^^^^^

::

	usage: hicpro_split.py [-h] [-j JID] [--split_fastq] [--queue QUEUE]
	                       [--hicpro_config HICPRO_CONFIG]
	                       [--hichipper_config HICHIPPER_CONFIG]
	                       [--MAPS_config MAPS_CONFIG] [-a ANCHOR]
	                       [--cutsite CUTSITE] -r1 R1 -r2 R2 -s SAMPLE_ID
	                       [--interactive] [-g GENOME] [-i INDEX_FILE]
	                       [--bwa_index BWA_INDEX] [--chrom_size CHROM_SIZE]
	                       [--genomic_feat_filepath GENOMIC_FEAT_FILEPATH]
	                       [-e DIGESTED_ENZYME] [--chr_count CHR_COUNT]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        hicpro_split_yli11_2020-06-16)
	  --split_fastq         only run hicpro (default: False)
	  --queue QUEUE
	  --hicpro_config HICPRO_CONFIG
	  --hichipper_config HICHIPPER_CONFIG
	  --MAPS_config MAPS_CONFIG
	  -a ANCHOR, --anchor ANCHOR
	                        anchor list to search for interactions, if given, MAPS
	                        will be run as well (default: None)
	  --cutsite CUTSITE     Mbol cut site (default: GATC)
	  -r1 R1                fastq R1 (default: None)
	  -r2 R2                fastq R2 (default: None)
	  -s SAMPLE_ID, --sample_id SAMPLE_ID
	                        sample ID (default: None)
	  --interactive         run pipeline interatively (default: False)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -i INDEX_FILE, --index_file INDEX_FILE
	                        bowtie2 index file (default:
	                        /home/yli11/Data/Human/hg19/index/bowtie2_index/hg19)
	  --bwa_index BWA_INDEX
	                        bwa index file (default: /home/yli11/Data/Human/hg19/i
	                        ndex/bwa_16a_index/hg19.fa)
	  --chrom_size CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Human/hg19/anno
	                        tations/hg19_main.chrom.sizes)
	  --genomic_feat_filepath GENOMIC_FEAT_FILEPATH
	                        MAPS genomic_feat_filepath (default: /home/yli11/HemTo
	                        ols/share/misc/MAPS/MAPS_data_files/hg19/genomic_featu
	                        res/F_GC_M_MboI_10Kb_el.hg19.txt)
	  -e DIGESTED_ENZYME, --digested_enzyme DIGESTED_ENZYME
	                        digested_fragments hg19_MboI (default: MboI)
	  --chr_count CHR_COUNT
	                        chr_count (default: 22)

Go to your fastq files folder and do the following:

.. code:: bash
	
	hpcf_interactive

	module load python/2.7.13

	bsub -P hicpro -q priority -R rusage[mem=8000] hicpro_split.py -r1 Tcell_HiC_2_3_4_R1.fastq.gz -r2 Tcell_HiC_2_3_4_R2.fastq.gz -s Tcell_HiC_2_3_4 -g hg38


Rerun failed exp
^^^^^^

::

	hicpro_split.py -r1 Jurkat_20copy.R1.fastq.gz -r2 Jurkat_20copy.R2.fastq.gz --sample_id Jurkat_20copy --jid hicpro_batch_yli11_2020-07-06_Jurkat_20copy -g hg19_20copy --rerun



Use ``--rerun`` option, match sample id, jid and genome.



captureC
^^^^^^

Use ``-t`` option, with absolute path.

The target.bed should have at least 4 columns: chr, start, end, name

::

	hicpro_split.py -r1 ${COL1} -r2 ${COL2} --sample_id ${COL3} -t /research/rgs01/project_space/chenggrp/blood_regulome/chenggrp/Sequencing_runs/rwu_data/newCaptureC/target.bed -g HBG1 -j ${COL3}_hicpro_captureC


if you want to keep duplicated reads and multi-mapped reads, use ``--keep_dup``.

We have pre-defined custom hg19 genomes: e.g., HBG1, hg19_copy


::

	hicpro_split.py -r1 Jurkat_20copy_cassette_captureC_combine_R1.fastq.gz -r2 Jurkat_20copy_cassette_captureC_combine_R2.fastq.gz -s jurkat_20copy -g hg19_20copy -t hg19_20copy_cassette_bait.bed --keep_dup




Fastq read order
^^^^^^^^^^^^^^

This pipeline requires the read names in the same order. If not, use:


::

	$i=test.fastq
	fastq-sort -i $i > $i.st.fastq










